from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tag
from .serializers import TagDetailSerializer, TagSerializer


class TagDetailView(APIView):
    @swagger_auto_schema(
        tags=("tags",),
        operation_summary="Get tag details",
        responses={
            status.HTTP_200_OK: TagDetailSerializer,
            status.HTTP_404_NOT_FOUND: "Not found.",
        },
    )
    def get(self, request: Request, name: str) -> Response:
        tags = get_object_or_404(Tag, name=name)
        serializer = TagDetailSerializer(tags)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagListView(APIView):
    def get_queryset(self):
        tags = None
        tag_name = self.request.query_params.get("name", None)
        tag_ids = self.request.query_params.get("ids", None)
        print(tag_name, tag_ids)
        if tag_name:
            tags = Tag.objects.filter(name__search=tag_name)[:10]
        elif tag_ids:
            tags = Tag.objects.filter(id__in=tag_ids.split(","))[:10]
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
                description="Search tags by id",
            ),
        ),
        responses={
            status.HTTP_200_OK: TagSerializer,
        },
    )
    def get(self, request: Request) -> Response:
        serializer = TagSerializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=("tags",),
        operation_summary="Create a new tag",
        request_body=TagDetailSerializer,
        responses={
            status.HTTP_201_CREATED: TagDetailSerializer,
            status.HTTP_400_BAD_REQUEST: "Bad request.",
            status.HTTP_401_UNAUTHORIZED: "Unauthorized.",
        },
    )
    def post(self, request: Request) -> Response:
        serializer = TagDetailSerializer(request.data, owner=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
