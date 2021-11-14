from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from flaam_api.utils.permissions import IsOwnerOrReadOnly

from .filters import DiscussionCommentFilterSet, DiscussionFilterSet
from .models import Discussion, DiscussionComment
from .serializers import DiscussionCommentSerializer, DiscussionSerializer

UserModel = get_user_model()


class DiscussionListView(ListCreateAPIView):
    """
    List all discussions, or create a new discussion.
    """

    serializer_class = DiscussionSerializer
    queryset = (
        Discussion.objects.all()
        .select_related("owner")
        .prefetch_related(
            "upvotes",
            "downvotes",
            "views",
            "comments",
        )
        .annotate(
            upvote_count=Count("upvotes"),
            downvote_count=Count("downvotes"),
            view_count=Count("views"),
            comments_count=Count("comments"),
        )
    )
    ordering = ("-created_at",)
    filterset_class = DiscussionFilterSet

    search_fields = ("title", "description", "idea__title")
    ordering_fields = (
        "upvote_count",
        "downvote_count",
        "view_count",
        "comments_count",
        "created_at",
        "updated_at",
    )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(
        tags=("discussions",),
        operation_summary="Get discussions list",
        responses={
            200: DiscussionSerializer(many=True),
            401: "Unauthorized.",
        },
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("discussions",),
        operation_summary="Create discussion",
        request_body=DiscussionSerializer,
        responses={
            201: DiscussionSerializer,
            401: "Unauthorized.",
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class DiscussionDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a discussion instance.
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = DiscussionSerializer
    queryset = (
        Discussion.objects.all()
        .select_related("owner")
        .prefetch_related(
            "upvotes",
            "downvotes",
            "views",
            "comments",
        )
        .annotate(
            upvote_count=Count("upvotes"),
            downvote_count=Count("downvotes"),
            view_count=Count("views"),
            comments_count=Count("comments"),
        )
    )

    @swagger_auto_schema(
        tags=("discussions",),
        operation_summary="Get discussion",
        responses={
            200: DiscussionSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        self.get_object().views.add(request.user)
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("discussions",),
        operation_summary="Update discussion",
        request_body=DiscussionSerializer,
        responses={
            200: DiscussionSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("discussions",),
        operation_summary="Update discussion",
        request_body=DiscussionSerializer,
        responses={
            200: DiscussionSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def patch(self, request: Request, *args, **kwargs) -> Response:
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("discussions",),
        operation_summary="Delete discussion",
        responses={
            204: "No content.",
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        return super().delete(request, *args, **kwargs)


class DiscussionCommentListView(ListCreateAPIView):
    """
    List all discussion comments, or create a new discussion comment.
    """

    serializer_class = DiscussionCommentSerializer
    queryset = DiscussionComment.objects.all().select_related("owner")
    ordering = ("-created_at",)
    filterset_class = DiscussionCommentFilterSet
    search_fields = ("body",)
    ordering_fields = ("created_at", "updated_at")

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @swagger_auto_schema(
        tags=("discussion-comments",),
        operation_summary="Get discussion comments list",
        responses={
            200: DiscussionCommentSerializer(many=True),
            401: "Unauthorized.",
        },
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("discussion-comments",),
        operation_summary="Create discussion comment",
        request_body=DiscussionCommentSerializer,
        responses={
            201: DiscussionCommentSerializer,
            401: "Unauthorized.",
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class DiscussionCommentDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a discussion comment instance.
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = DiscussionCommentSerializer
    queryset = DiscussionComment.objects.all().select_related("owner")

    @swagger_auto_schema(
        tags=("discussion-comments",),
        operation_summary="Get discussion comment",
        responses={
            200: DiscussionCommentSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("discussion-comments",),
        operation_summary="Update discussion comment",
        request_body=DiscussionCommentSerializer,
        responses={
            200: DiscussionCommentSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("discussion-comments",),
        operation_summary="Update discussion comment",
        request_body=DiscussionCommentSerializer,
        responses={
            200: DiscussionCommentSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def patch(self, request: Request, *args, **kwargs) -> Response:
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("discussion-comments",),
        operation_summary="Delete discussion comment",
        responses={
            204: "No content.",
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        return super().delete(request, *args, **kwargs)


class VoteDiscussionView(APIView):
    """
    Vote for a discussion.
    """

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=("discussions",),
        operation_summary="Vote for a discussion",
        manual_parameters=(
            openapi.Parameter(
                "value",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Vote, possible values: [-1, 0, 1]",
            ),
        ),
        responses={
            200: "Successfully voted.",
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def post(self, request: Request, pk: int, *args, **kwargs) -> Response:
        discussion = get_object_or_404(Discussion, pk=pk)
        value = request.query_params.get("value")

        value = request.query_params.get("value")
        if value == "0":
            discussion.downvotes.remove(request.user)
            discussion.upvotes.remove(request.user)
        elif value == "1":
            discussion.upvotes.add(request.user)
            discussion.downvotes.remove(request.user)
        elif value == "-1":
            discussion.downvotes.add(request.user)
            discussion.upvotes.remove(request.user)
        else:
            raise ValidationError("Invalid vote value.")

        return Response(status=status.HTTP_204_NO_CONTENT)
