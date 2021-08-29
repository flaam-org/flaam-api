from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.utils.timezone import datetime, timedelta
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import APIException, ParseError
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from flaam_api.exceptions import NotFound

from .models import PasswordResetToken, User
from .serializers import (
    PublicUserSerializer,
    ResetPasswordTokenSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
    TokenVerifyResponseSerializer,
    UserSerializer,
)
from .validators import PasswordValidator, UsernameValidator

UserModel: User = get_user_model()


class UserRegisterView(APIView):
    """Register a new user"""

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={
            201: TokenObtainPairResponseSerializer,
            400: "Bad request",
        },
    )
    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            refresh = RefreshToken.for_user(serializer.instance)
            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(
                data,
                status=status.HTTP_201_CREATED,
            )


class UserExistsView(APIView):
    """Query if given username or email already exists"""

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "username",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "email",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            204: "Username or email already exist",
            400: "Bad request",
            404: "Username or email does not exist",
        },
    )
    def get(self, request: Request) -> Response:
        username = request.query_params.get("username")
        email = request.query_params.get("email")

        if username:
            UsernameValidator()(username)
            exists = UserModel.objects.filter(username=username).exists()
        elif email:
            EmailValidator()(email)
            exists = UserModel.objects.filter(email=email).exists()
        else:
            raise ParseError("Provide either username or email")

        if exists:
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    """User Profile"""

    @swagger_auto_schema(
        responses={
            200: UserSerializer,
            401: "Unauthorized",
        },
    )
    def get(self, request: Request) -> Response:
        """Get user profile"""
        serializer = UserSerializer(request.user)
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
        """Update user profile"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            204: "No content",
            401: "Unauthorized",
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
    """Public User Profile"""

    def get_object(self, pk: int) -> User:
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
    def get(self, request: Request, pk: int) -> Response:
        """Read public user profile"""
        user = self.get_object(pk)
        serializer = PublicUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordTokenView(APIView):
    """Obtain Reset Password Token"""

    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        request_body=ResetPasswordTokenSerializer,
        responses={
            200: UserSerializer,
            400: "Bad request",
            401: "Unauthorized",
        },
    )
    def post(self, request: Request) -> Response:
        """generate password reset token"""
        serializer = ResetPasswordTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]

        # generate token
        reset_token = PasswordResetToken.objects.get_or_create(user=user)
        email = True  # TODO: send email
        if email:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise APIException(detail={"detail": "Failed to send Email."})


class ResetPasswordView(APIView):
    """Reset Password"""

    permission_classes = (AllowAny,)

    def get_object(self, token: str) -> PasswordResetToken:
        try:
            token = PasswordResetToken.objects.get(token=token)
            is_token_valid = (
                token.created_at
                + timedelta(minutes=settings.PASSWORD_RESET_TOKEN_VALIDITY)
                > datetime.now()
            )
            if is_token_valid:
                return token
            token.delete()
            raise PasswordResetToken.DoesNotExist
        except PasswordResetToken.DoesNotExist:
            raise NotFound(detail={"detail": "Invalid token."})

    def get(self, request: Request, token) -> Response:
        """Check reset token"""
        reset_token: PasswordResetToken = self.get_object(token)
        return Response(
            {
                "username": reset_token.user.username,
                "email": reset_token.user.email,
            },
            status=status.HTTP_200_OK,
        )

    @swagger_auto_schema(
        # request_body="",
        responses={
            200: "",
            404: "Invalid token",
        },
    )
    def post(self, request: Request, token) -> Response:
        """Reset password"""
        reset_token: PasswordResetToken = self.get_object(token)
        password = request.data.get("password")
        if not password:
            raise ParseError(detail={"detail": "Password is required."})

        # validate password
        PasswordValidator()(password)

        reset_token.user.set_password(password)
        reset_token.delete()
        # TODO: send email
        return Response(status=status.HTTP_204_NO_CONTENT)


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: TokenObtainPairResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: TokenRefreshResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        responses={status.HTTP_200_OK: TokenVerifyResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
