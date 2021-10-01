from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from flaam_api.utils.paginations import CustomLimitOffsetPagination
from flaam_api.utils.permissions import IsOwnerOrReadOnly

from .models import Idea
from .serializers import IdeaSerializer, MilestoneSerializer

UserModel = get_user_model()


class IdeaDetailView(RetrieveAPIView):
    """
    Retrieve a single idea.
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = IdeaSerializer
    queryset = Idea.objects.all().prefetch_related(
        "milestones", "upvotes", "downvotes", "views"
    )

    @swagger_auto_schema(
        tags=("ideas",),
        operation_summary="Get idea details",
        responses={
            200: IdeaSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def get(self, request: Request, pk: int, *args, **kwargs) -> Response:
        self.get_object().views.add(request.user)
        return super().get(request, pk, *args, **kwargs)

    @swagger_auto_schema(
        tags=("ideas",),
        operation_summary="Update idea details",
        request_body=IdeaSerializer,
        responses={
            200: IdeaSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def put(self, request: Request, pk: int, *args, **kwargs) -> Response:
        idea = self.get_queryset().get(pk=pk)
        serializer = self.get_serializer(
            idea, data=request.data, context={"request": request}, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            idea = serializer.save(owner=request.user)
            milestones = request.data.get("milestones", [])
            if milestones:
                milestone_serializer = MilestoneSerializer(
                    data=milestones,
                    many=True,
                    context={"idea": idea},
                )
                if milestone_serializer.is_valid():
                    milestone_serializer.save()
                else:
                    raise ValidationError(serializer.errors)
        return Response(data=self.get_serializer(idea).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=("ideas",),
        operation_summary="Delete idea",
        request_body=IdeaSerializer,
        responses={
            200: IdeaSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def delete(self, request, *args, **kwargs):
        raise APIException("Not Implemented")


class IdeaListView(ListCreateAPIView):
    """
    List all ideas or create a new one.
    """

    permission_classes = (IsAuthenticated,)
    pagination_class = CustomLimitOffsetPagination
    serializer_class = IdeaSerializer

    def get_queryset(self):
        ideas = (
            Idea.objects.all()
            .prefetch_related(
                "milestones",
                "upvotes",
                "downvotes",
                "views",
                "tags",
                "implementations",
            )
            .select_related("owner")
        )
        owner_id = self.request.query_params.get("owner_id")
        if owner_id:
            user = get_object_or_404(UserModel, pk=owner_id)
            return (
                user.ideas.all()
                .prefetch_related(
                    "milestones",
                    "upvotes",
                    "downvotes",
                    "views",
                    "tags",
                    "implementations",
                )
                .select_related("owner")
            )
        bookmarked_by = self.request.query_params.get("bookmarked_by")
        if bookmarked_by:
            user = get_object_or_404(UserModel, pk=bookmarked_by)
            return (
                user.bookmarked_ideas.all()
                .prefetch_related(
                    "milestones",
                    "upvotes",
                    "downvotes",
                    "views",
                    "tags",
                    "implementations",
                )
                .select_related("owner")
            )
        return ideas

    @swagger_auto_schema(
        tags=("ideas",),
        operation_summary="Get ideas",
        manual_parameters=(
            openapi.Parameter(
                "owner_id",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Get user's ideas",
            ),
            openapi.Parameter(
                "bookmarked_by",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Get user's bookmarked ideas",
            ),
        ),
        responses={
            200: IdeaSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("ideas",),
        operation_summary="Create new Idea",
        request_body=IdeaSerializer,
        responses={
            200: IdeaSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(
            data=request.data, context={"request": request}, partial=True
        )
        if serializer.is_valid(raise_exception=True):
            idea = serializer.save(owner=request.user)
            milestones = request.data.get("milestones", [])
            if milestones:
                milestone_serializer = MilestoneSerializer(
                    data=milestones,
                    many=True,
                    context={"idea": idea},
                )
                if milestone_serializer.is_valid():
                    milestone_serializer.save()
                else:
                    idea.delete()
                    raise ValidationError(serializer.errors)
        return Response(
            data=self.get_serializer(idea).data, status=status.HTTP_201_CREATED
        )


class BookmarkIdeaView(APIView):
    """
    Bookmark an idea.
    """

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=("ideas",),
        operation_id="bookmark_idea_add",
        operation_summary="Add an idea to users bookmark",
        responses={
            200: "Success.",
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def post(self, request: Request, pk: int, *args, **kwargs) -> Response:
        idea = get_object_or_404(Idea, pk=pk)
        idea.bookmarked_by.add(request.user)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=("ideas",),
        operation_id="bookmark_idea_remove",
        operation_summary="Remove an idea from users bookmark",
        responses={
            200: "Success.",
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def delete(self, request: Request, pk: int, *args, **kwargs) -> Response:
        idea = get_object_or_404(Idea, pk=pk)
        idea.bookmarked_by.remove(request.user)
        return Response(status=status.HTTP_200_OK)
