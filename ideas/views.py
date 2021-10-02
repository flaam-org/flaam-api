from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import APIException, ParseError, ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from flaam_api.utils.paginations import CustomLimitOffsetPagination
from flaam_api.utils.permissions import IsOwnerOrReadOnly

from .models import Idea
from .serializers import IdeaSerializer

UserModel = get_user_model()


class IdeaDetailView(RetrieveUpdateAPIView):
    """
    Retrieve a single idea.
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = IdeaSerializer
    queryset = (
        Idea.objects.all()
        .select_related("owner")
        .prefetch_related(
            "upvotes",
            "downvotes",
            "views",
            "tags",
            "implementations",
        )
        .annotate(
            upvote_count=Count("upvotes"),
            downvote_count=Count("downvotes"),
            view_count=Count("views"),
            implementation_count=Count("implementations"),
        )
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
        # increment view count
        self.get_object().views.add(request.user)
        return super().get(request, pk, *args, **kwargs)

    @swagger_auto_schema(
        tags=("ideas",),
        operation_summary="Replace idea",
        request_body=IdeaSerializer,
        responses={
            200: IdeaSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        return super().put(request, *args, **kwargs)

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
    def patch(self, request: Request, *args, **kwargs) -> Response:
        return super().patch(request, *args, **kwargs)

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
        ideas = Idea.objects.all()

        bookmarked_by = self.request.query_params.get("bookmarked_by")
        owner_id = self.request.query_params.get("owner_id")
        if owner_id:
            user = get_object_or_404(UserModel, pk=owner_id)
            ideas = ideas.filter(owner=user)
        elif bookmarked_by:
            user = get_object_or_404(UserModel, pk=bookmarked_by)
            ideas = user.bookmarked_ideas.all()

        return (
            ideas.select_related("owner")
            .prefetch_related(
                "upvotes",
                "downvotes",
                "views",
                "tags",
                "implementations",
            )
            .annotate(
                upvote_count=Count("upvotes"),
                downvote_count=Count("downvotes"),
                view_count=Count("views"),
                implementation_count=Count("implementations"),
            )
        )

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
            200: IdeaSerializer(many=True),
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
        return super().post(request, *args, **kwargs)


class VoteIdeaView(APIView):
    """Vote on an idea."""

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=("ideas",),
        operation_summary="Vote on an idea",
        manual_parameters=(
            openapi.Parameter(
                "value",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Vote, possible values: [-1, 0, 1]",
            ),
        ),
        responses={
            204: "Success.",
            400: "Bad request.",
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def post(self, request: Request, pk: int) -> Response:

        idea = get_object_or_404(Idea, pk=pk)

        value = request.query_params.get("value")
        if value == "0":
            idea.downvotes.remove(request.user)
            idea.upvotes.remove(request.user)
        elif value == "1":
            idea.upvotes.add(request.user)
            idea.downvotes.remove(request.user)
        elif value == "-1":
            idea.downvotes.add(request.user)
            idea.upvotes.remove(request.user)
        else:
            raise ParseError("Invalid vote value.")

        return Response(status=status.HTTP_204_NO_CONTENT)


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
            204: "Success.",
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def post(self, request: Request, pk: int, *args, **kwargs) -> Response:
        idea = get_object_or_404(Idea, pk=pk)
        idea.bookmarked_by.add(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        tags=("ideas",),
        operation_id="bookmark_idea_remove",
        operation_summary="Remove an idea from users bookmark",
        responses={
            204: "Success.",
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def delete(self, request: Request, pk: int, *args, **kwargs) -> Response:
        idea = get_object_or_404(Idea, pk=pk)
        idea.bookmarked_by.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
