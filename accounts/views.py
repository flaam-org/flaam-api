from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from flaam_api.exceptions import NotFound

from .models import User
from .serializers import PublicUserSerializer, UserSerializer

UserModel: User = get_user_model()


class UserRegisterView(APIView):
    """
    User Model
    """

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: UserSerializer,
            400: "Bad request",
        },
    )
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )


class UserProfileView(APIView):
    """
    User Profile
    """

    @swagger_auto_schema(
        responses={
            200: UserSerializer,
            401: "Unauthorized",
        },
    )
    def get(self, request: Request) -> Response:
        """
        Get user profile
        """
        serializer = UserSerializer(request.user)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Bad request",
            401: "Unauthorized",
        },
    )
    def put(self, request: Request) -> Response:
        """
        Update user profile
        """
        serializer = UserSerializer(request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            204: "No content",
        },
    )
    def delete(self, request: Request) -> Response:
        # Just deactivate the user
        # TODO: send email that account will be deleted after x days
        # TODO: add a delay period for deletion request
        request.user.is_active = False
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublicUserProfileView(APIView):
    def get_object(self, pk):
        try:
            return UserModel.objects.get(pk=pk)
        except UserModel.DoesNotExist:
            raise NotFound(detail={"detail": "User does not exist."})

    @swagger_auto_schema(
        responses={
            200: PublicUserSerializer,
            401: "Unauthorized",
            404: "User does not exist.",
        },
    )
    def get(self, request, pk):
        """
        Read public user profile
        """
        user = self.get_object(pk)
        serializer = PublicUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    """
    Reset password
    """

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Bad request",
            401: "Unauthorized",
        },
    )
    def post(self, request: Request) -> Response:
        """
        Reset password
        """
        raise APIException(detail="Not implemented yet.")
