from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import ParseError, PermissionDenied
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from flaam_api.utils.paginations import CustomLimitOffsetPagination
from flaam_api.utils.permissions import IsOwnerOrReadOnly

from .models import Implementation, ImplementationComment
from .serializers import ImplementationCommentSerializer, ImplementationSerializer

UserModel = get_user_model()


class ImplementationListView(ListCreateAPIView):
    """
    Implementation list view.
    """

    permission_classes = (IsAuthenticated,)
    pagination_class = CustomLimitOffsetPagination
    serializer_class = ImplementationSerializer

    queryset = Implementation.objects.all()

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Get implementation list",
        responses={
            200: ImplementationSerializer(many=True),
            401: "Unauthorized.",
        },
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Create implementation",
        request_body=ImplementationSerializer,
        responses={
            201: ImplementationSerializer,
            401: "Unauthorized.",
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class ImplementationDetailView(RetrieveUpdateAPIView):
    """
    Implementation detail view.
    """

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ImplementationSerializer
    queryset = (
        Implementation.objects.all()
        .select_related("owner")
        .prefetch_related(
            "upvotes",
            "downvotes",
            "views",
            "tags",
            "comments",
        )
        .annotate(
            upvotes_count=Count("upvotes"),
            downvotes_count=Count("downvotes"),
            views_count=Count("views"),
            comments_count=Count("comments"),
        )
    )

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Get implementation details",
        responses={
            200: ImplementationSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def get(self, request: Request, pk: int, *args, **kwargs) -> Response:
        # increment view count
        self.get_object().views.add(request.user)
        return super().get(request, pk, *args, **kwargs)

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Replace idea",
        request_body=ImplementationSerializer,
        responses={
            200: ImplementationSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Update idea details",
        request_body=ImplementationSerializer,
        responses={
            200: ImplementationSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def patch(self, request: Request, *args, **kwargs) -> Response:
        return super().patch(request, *args, **kwargs)


class ImplementationCommentListView(ListCreateAPIView):

    permission_classes = (IsAuthenticated,)
    pagination_class = CustomLimitOffsetPagination
    serializer_class = ImplementationCommentSerializer

    queryset = ImplementationComment.objects.all()

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Get implementation comment list",
        responses={
            200: ImplementationCommentSerializer(many=True),
            401: "Unauthorized.",
        },
    )
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Create implementation comment",
        request_body=ImplementationCommentSerializer,
        responses={
            201: ImplementationCommentSerializer,
            401: "Unauthorized.",
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        return super().post(request, *args, **kwargs)


class ImplementationCommentDetailView(RetrieveUpdateDestroyAPIView):

    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ImplementationCommentSerializer

    queryset = ImplementationComment.objects.all()

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Get implementation comment details",
        responses={
            200: ImplementationCommentSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def get(self, request: Request, pk: int, *args, **kwargs) -> Response:
        return super().get(request, pk, *args, **kwargs)

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Replace implementation comment",
        request_body=ImplementationCommentSerializer,
        responses={
            200: ImplementationCommentSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def put(self, request: Request, *args, **kwargs) -> Response:
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Update implementation comment details",
        request_body=ImplementationCommentSerializer,
        responses={
            200: ImplementationCommentSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def patch(self, request: Request, *args, **kwargs) -> Response:
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Delete implementation comment",
        responses={
            204: "No content.",
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def delete(self, request: Request, *args, **kwargs) -> Response:
        return super().delete(request, *args, **kwargs)


class VoteImplementationView(APIView):
    """
    Vote implementation view.
    """

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Vote implementation",
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
    def post(self, request: Request, pk: int, *args, **kwargs) -> Response:
        implementation = get_object_or_404(Implementation, pk=pk)
        value = request.query_params.get("value")

        value = request.query_params.get("value")
        if value == "0":
            implementation.downvotes.remove(request.user)
            implementation.upvotes.remove(request.user)
        elif value == "1":
            implementation.upvotes.add(request.user)
            implementation.downvotes.remove(request.user)
        elif value == "-1":
            implementation.downvotes.add(request.user)
            implementation.upvotes.remove(request.user)
        else:
            raise ParseError("Invalid vote value.")

        return Response(status=status.HTTP_204_NO_CONTENT)


class VoteImplementationCommentView(APIView):
    """
    Vote implementation comment view.
    """

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Vote implementation comment",
        manual_parameters=(
            openapi.Parameter(
                "value",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Vote, possible values: [0, 1]",
            ),
        ),
        responses={
            204: "Success.",
            400: "Bad request.",
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def post(self, request: Request, pk: int, *args, **kwargs) -> Response:
        implementation_comment = get_object_or_404(ImplementationComment, pk=pk)
        value = request.query_params.get("value")

        value = request.query_params.get("value")
        if value == "0":
            implementation_comment.upvotes.remove(request.user)
        elif value == "1":
            implementation_comment.upvotes.add(request.user)
        else:
            raise ParseError("Invalid vote value.")

        return Response(status=status.HTTP_204_NO_CONTENT)


class ValidateImplementationView(APIView):
    """
    Validate implementation view.
    """

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Validate implementation",
        responses={
            204: "Success.",
            400: "Bad request.",
            401: "Unauthorized.",
            403: "Forbidden.",
            404: "Not found.",
        },
    )
    def post(self, request: Request, pk: int, *args, **kwargs) -> Response:
        implementation = get_object_or_404(Implementation, pk=pk)

        if request.user != implementation.idea.owner:
            raise PermissionDenied(
                "Only the owner of the idea can perform this action."
            )
        implementation.is_validated = True
        implementation.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Unvalidate implementation",
        responses={
            204: "Success.",
            400: "Bad request.",
            401: "Unauthorized.",
            403: "Forbidden.",
            404: "Not found.",
        },
    )
    def delete(self, request: Request, pk: int, *args, **kwargs) -> Response:
        implementation = get_object_or_404(Implementation, pk=pk)

        if request.user != implementation.idea.owner:
            raise PermissionDenied(
                "Only the owner of the idea can perform this action."
            )
        implementation.is_validated = False
        implementation.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AcceptImplementationView(APIView):
    """
    Accept implementation view.
    """

    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Accept implementation",
        responses={
            204: "Success.",
            400: "Bad request.",
            401: "Unauthorized.",
            403: "Forbidden.",
            404: "Not found.",
        },
    )
    def post(self, request: Request, pk: int, *args, **kwargs) -> Response:
        implementation = get_object_or_404(Implementation, pk=pk)

        if request.user != implementation.idea.owner:
            raise PermissionDenied(
                "Only the owner of the idea can perform this action."
            )
        implementation.is_accepted = True
        implementation.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        tags=("implementations",),
        operation_summary="Unaccept implementation",
        responses={
            204: "Success.",
            400: "Bad request.",
            401: "Unauthorized.",
            403: "Forbidden.",
            404: "Not found.",
        },
    )
    def delete(self, request: Request, pk: int, *args, **kwargs) -> Response:
        implementation = get_object_or_404(Implementation, pk=pk)

        if request.user != implementation.idea.owner:
            raise PermissionDenied(
                "Only the owner of the idea can perform this action."
            )
        implementation.is_accepted = False
        implementation.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
