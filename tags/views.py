from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Tag
from .serializers import TagDetailSerializer, TagSerializer


class TagDetailView(RetrieveAPIView):
    serializer_class = TagDetailSerializer
    lookup_field = "name"
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
    def get(self, request: Request, name: str) -> Response:
        return super().get(request, name)


class TagListView(ListCreateAPIView):

    pagination_class = LimitOffsetPagination
    serializer_class = TagSerializer

    def get_queryset(self):
        tag_name = self.request.query_params.get("name", None)
        tag_ids = self.request.query_params.get("ids", None)
        tags = Tag.objects.all()
        if tag_name:
            # TODO: improve search
            # https://docs.djangoproject.com/en/3.2/ref/contrib/postgres/search/
            tags = tags.filter(name__search=tag_name)
        elif tag_ids:
            tags = tags.filter(id__in=tag_ids.split(","))
        return tags

    @swagger_auto_schema(
        tags=("tags",),
        operation_summary="Get tags",
        manual_parameters=(
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
            200: TagSerializer,
            401: "Unauthorized.",
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
