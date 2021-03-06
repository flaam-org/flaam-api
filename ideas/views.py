from django.db.models import Count
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ParseError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from flaam_api.utils.permissions import IsOwnerOrReadOnly

from .filters import IdeaFilterSet
from .models import Idea
from .serializers import IdeaSerializer


class IdeaListView(ListCreateAPIView):
    """
    List all ideas or create a new one.
    """

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
    ordering = ("-created_at",)
    filterset_class = IdeaFilterSet
    search_fields = (
        "@title",
        "@description",
    )
    ordering_fields = (
        "upvote_count",
        "downvote_count",
        "view_count",
        "implementation_count",
        "created_at",
        "updated_at",
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(
        tags=("ideas",),
        operation_summary="Get ideas",
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


class IdeaDetailView(RetrieveUpdateAPIView):
    """
    Retrieve, update or delete an idea instance.
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
        idea = self.get_object()
        if idea.implementations.count() > 0:
            idea.archived = True
            idea.save()
            resp_msg = "Idea archived."
        else:
            idea.delete()
            resp_msg = "Idea deleted."
        return Response({"detail": resp_msg}, status=status.HTTP_200_OK)


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
