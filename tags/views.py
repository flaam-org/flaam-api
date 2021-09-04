from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.exceptions import APIException, NotFound, ParseError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Tag
from .serializers import TagDetailSerializer, TagSerializer


class TagDetailView(APIView):
    @swagger_auto_schema(
        responses={
            200: TagDetailSerializer,
            404: "Not found.",
        }
    )
    def get(self, request: Request, name: str) -> Response:
        tags = get_object_or_404(Tag, name=name)
        serializer = TagDetailSerializer(tags)
        return Response(serializer.data, status=status.HTTP_200_OK)
