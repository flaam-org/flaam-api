from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVector
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from flaam_api.utils.paginations import CustomLimitOffsetPagination

from .models import Tag
from .serializers import TagDetailSerializer

UserModel = get_user_model()


class TagDetailView(RetrieveAPIView):
    serializer_class = TagDetailSerializer
    queryset = Tag.objects.all()

    @swagger_auto_schema(
        tags=("tags",),
        operation_summary="Get tag details",
        responses={
            200: TagDetailSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def get(self, request: Request, pk: int) -> Response:
        return super().get(request, pk)


class TagListView(ListCreateAPIView):

    pagination_class = CustomLimitOffsetPagination
    serializer_class = TagDetailSerializer

    def get_queryset(self):
        tags = Tag.objects.all()

        favourited_by = self.request.query_params.get("favourited_by", None)
        if favourited_by:
            user = get_object_or_404(UserModel, pk=favourited_by)
            return user.favourite_tags.all()

        tag_ids = self.request.query_params.get("ids", None)
        if tag_ids:
            return tags.filter(id__in=tag_ids.split(","))

        tag_name = self.request.query_params.get("name", None)
        if tag_name:
            vector = SearchVector("name")  # + SearchVector("description")
            tags = tags.annotate(search=vector).filter(search__icontains=tag_name)
        return tags

    @swagger_auto_schema(
        tags=("tags",),
        operation_summary="Get tags",
        manual_parameters=(
            openapi.Parameter(
                "favourited_by",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_INTEGER,
                description="Get user's favourite tags",
            ),
            openapi.Parameter(
                "name",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Search tags by name",
            ),
            openapi.Parameter(
                "ids",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Get tags by id",
            ),
        ),
        responses={
            200: TagDetailSerializer,
            401: "Unauthorized.",
            404: "Not Found.",
        },
    )
    def get(self, request: Request) -> Response:
        return super().get(request)

    @swagger_auto_schema(
        tags=("tags",),
        operation_summary="Create a new tag",
        responses={
            201: TagDetailSerializer,
            400: "Bad request.",
            401: "Unauthorized.",
        },
    )
    def post(self, request: Request) -> Response:
        return super().post(request)


class FavouriteTagView(APIView):
    """
    Add or remove a tag from the user's favourites list.
    """

    @swagger_auto_schema(
        tags=("tags",),
        operation_id="favourite_tag_add",
        operation_summary="Add a tag to the user's favourites list",
        responses={
            200: "Success.",
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def post(self, request: Request, pk: int) -> Response:
        tag = get_object_or_404(Tag, pk=pk)
        tag.favorited_by.add(request.user)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=("tags",),
        operation_id="favourite_tag_remove",
        operation_summary="Remove a tag from the user's favourites list",
        responses={
            200: "Success.",
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def delete(self, request: Request, pk: int) -> Response:
        tag = get_object_or_404(Tag, id=pk)
        tag.favorited_by.remove(request.user)
        return Response(status=status.HTTP_200_OK)
