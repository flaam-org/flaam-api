import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.core.validators import EmailValidator
from django.shortcuts import get_object_or_404
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
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

from .models import User
from .serializers import (
    PasswordResetSerializer,
    PasswordResetTokenSerializer,
    PublicUserSerializer,
    TokenObtainPairResponseSerializer,
    TokenRefreshResponseSerializer,
    TokenVerifyResponseSerializer,
    UserSerializer,
)
from .validators import UsernameValidator

UserModel: User = get_user_model()


class UserRegisterView(APIView):
    """Register a new user"""

    authentication_classes = ()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        tags=("users", "auth"),
        security=[],
        operation_summary="Register a new user",
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
            return Response(data, status=status.HTTP_201_CREATED)


class UserExistsView(APIView):
    """Query if given username or email already exists"""

    authentication_classes = ()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        tags=("auth",),
        security=[],
        operation_id="accounts_user_exists_read",
        operation_summary="Check if username or email is already in use",
        manual_parameters=(
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
        ),
        responses={
            204: "Username or email already exist",
            400: "Bad request",
            status.HTTP_404_NOT_FOUND: "Username or email does not exist",
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
        tags=("users",),
        operation_id="accounts_user_profile_read",
        operation_summary="Get authenticated user's profile",
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
        tags=("users",),
        operation_summary="Update authenticated user's profile",
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            400: "Bad request",
            401: "Unauthorized",
        },
    )
    def patch(self, request: Request) -> Response:
        """Update user profile"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        tags=("users",),
        operation_summary="Deactivate authenticated user's profile",
        responses={
            204: "Accout deactivated successfully",
            401: "Unauthorized",
        },
    )
    def delete(self, request: Request) -> Response:
        # Just deactivate the user
        send_mail(
            subject="Flaam | Account deactivated",
            message="Your flaam account has been deactivated",
            from_email=None,
            recipient_list=[request.user.email],
        )
        # TODO: add a delay period for deletion request
        request.user.is_active = False
        request.user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PublicUserProfileView(APIView):
    """Public User Profile"""

    @swagger_auto_schema(
        tags=("users",),
        operation_id="accounts_user_public_profile_read",
        operation_summary="Get public user's profile",
        responses={
            200: PublicUserSerializer,
            401: "Unauthorized",
            status.HTTP_404_NOT_FOUND: "Not found.",
        },
    )
    def get(self, request: Request, pk: int) -> Response:
        """Read public user profile"""
        user = get_object_or_404(UserModel, pk=pk)
        serializer = PublicUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPasswordTokenView(APIView):
    """Obtain Reset Password Token"""

    authentication_classes = ()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        tags=("auth",),
        security=[],
        operation_id="accounts_password_reset_token_create",
        operation_summary="Obtain a password reset token",
        request_body=PasswordResetTokenSerializer,
        responses={
            204: "",
            400: "Bad request",
        },
    )
    def post(self, request: Request) -> Response:
        """generate password reset token"""
        serializer = PasswordResetTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = get_object_or_404(
                UserModel, email=serializer.validated_data["email"]
            )
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)

        try:
            message = (
                f"{settings.FRONTEND_URL}/reset-password?uidb64={uidb64}&token={token}"
            )
            print(message)  # TODO: no prod
            send_mail(
                subject="Flaam | Password reset",
                message=message,
                from_email=None,
                recipient_list=[user.email],
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            raise APIException(detail={"detail": str(e)})
        finally:
            # TODO: no prod
            url = (
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            )
            params = {
                "chat_id": settings.TELEGRAM_CHAT_ID,
                "text": f"EMAIL\nID: {user.email}\n\n{message}",
            }
            requests.get(url, params=params)


class ResetPasswordView(APIView):
    """Reset Password"""

    authentication_classes = ()
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        tags=("auth",),
        security=[],
        operation_id="accounts_password_reset_token_verify",
        operation_summary="validate password reset token",
        responses={
            200: openapi.Response(
                description="Valid reset token",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "username": openapi.Schema(type=openapi.TYPE_STRING),
                        "email": openapi.Schema(type=openapi.TYPE_STRING),
                    },
                ),
            ),
            400: "Invalid reset token",
        },
    )
    def get(self, request: Request, uidb64, token) -> Response:
        """Check reset token"""
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(UserModel, pk=uid)
        if PasswordResetTokenGenerator().check_token(user, token):
            return Response(
                {
                    "username": user.username,
                    "email": user.email,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Invalid reset token"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @swagger_auto_schema(
        tags=("auth",),
        security=[],
        operation_id="accounts_password_reset",
        operation_summary="Reset user password",
        request_body=PasswordResetSerializer,
        responses={
            200: TokenObtainPairResponseSerializer,
            400: "Invalid token",
        },
    )
    def post(self, request: Request, uidb64, token) -> Response:
        """Reset password"""
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_object_or_404(UserModel, pk=uid)
        if PasswordResetTokenGenerator().check_token(user, token):
            serializer = PasswordResetSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user.set_password(serializer.validated_data["password"])
                # TODO: blacklist outstanding jwt tokens
                send_mail(
                    subject="Flaam | Password reset",
                    message="Your password has been reset",
                    from_email=None,
                    recipient_list=[user.email],
                )
                refresh = RefreshToken.for_user(user)
                data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
                return Response(data, status=status.HTTP_200_OK)
        return Response(
            {"detail": "Invalid reset token"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class DecoratedTokenObtainPairView(TokenObtainPairView):
    @swagger_auto_schema(
        tags=("auth",),
        security=[],
        operation_summary="Obtain token pair",
        responses={
            200: TokenObtainPairResponseSerializer,
            400: "Bad request",
            401: "Unauthorized",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenRefreshView(TokenRefreshView):
    @swagger_auto_schema(
        tags=("auth",),
        security=[],
        operation_id="accounts_login_refresh",
        operation_summary="Refresh access token",
        responses={
            200: TokenRefreshResponseSerializer,
            400: "Bad request",
            401: "Unauthorized",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class DecoratedTokenVerifyView(TokenVerifyView):
    @swagger_auto_schema(
        tags=("auth",),
        security=[],
        operation_id="accounts_login_verify",
        operation_summary="Verify token",
        responses={
            200: TokenVerifyResponseSerializer,
            400: "Bad request",
            401: "Unauthorized",
        },
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
