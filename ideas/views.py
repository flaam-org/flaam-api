from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from flaam_api.utils.paginations import CustomLimitOffsetPagination
from flaam_api.utils.permissions import IsOwnerOrReadOnly

from .models import Idea
from .serializers import IdeaSerializer, MilestoneSerializer


class IdeaDetailView(RetrieveUpdateDestroyAPIView):
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
        return super().get(request, pk, *args, **kwargs)

    @swagger_auto_schema(
        tags=("ideas",),
        operation_summary="Get idea details",
        request_body=IdeaSerializer,
        responses={
            200: IdeaSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def put(self, request: Request, pk: int, *args, **kwargs) -> Response:
        return super().put(request, pk, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        raise APIException("Not Implemented")


class IdeaListView(ListCreateAPIView):
    """
    List all ideas or create a new one.
    """

    permission_classes = (IsAuthenticated,)
    pagination_class = CustomLimitOffsetPagination
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
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        tags=("ideas",),
        operation_summary="Get idea details",
        request_body=IdeaSerializer,
        responses={
            200: IdeaSerializer,
            401: "Unauthorized.",
            404: "Not found.",
        },
    )
    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            idea = serializer.save(owner=request.user)
            milestone_serializer = MilestoneSerializer(
                data=request.data.get("milestones", []),
                many=True,
                context={"idea": idea},
            )
            if milestone_serializer.is_valid():
                milestone_serializer.save()
            else:
                # idea.delete()
                raise ValidationError(serializer.errors)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
