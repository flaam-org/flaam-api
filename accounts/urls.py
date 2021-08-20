from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from accounts.views import (
    PublicUserProfileView,
    ResetPasswordTokenView,
    ResetPasswordView,
    UserProfileView,
    UserRegisterView,
)

urlpatterns = [
    # JWT
    path("login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("login/verify", TokenVerifyView.as_view(), name="token_verify"),
    # Users
    path("user", UserRegisterView.as_view(), name="user_register"),
    path("user/profile", UserProfileView.as_view(), name="user_profile"),
    path("user/<int:pk>", PublicUserProfileView.as_view(), name="user_public"),
    # password
    path(
        "user/reset-password",
        ResetPasswordTokenView.as_view(),
        name="reset_password",
    ),
    path(
        "user/reset-password/<str:token>",
        ResetPasswordView.as_view(),
        name="reset_password",
    ),
]
