from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .validators import PasswordValidator

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "email",
            "show_email",
            "password",
            "first_name",
            "last_name",
            "status",
            "description",
            "avatar",
            "following",
            "followers",
            "favourite_tags",
            "bookmarked_ideas",
            "bookmarked_implementations",
            "last_login",
            "date_joined",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }
        read_only_fields = ("id", "last_login", "date_joined", "followers")

    def create(self, validated_data):
        favourite_tags = validated_data.pop("favourite_tags", None)
        following = validated_data.pop("following", None)
        bookmarked_ideas = validated_data.pop("bookmarked_ideas", None)
        bookmarked_implementations = validated_data.pop(
            "bookmarked_implementations", None
        )
        user = UserModel.objects.create_user(**validated_data)
        if favourite_tags is not None:
            user.favourite_tags.set(favourite_tags)
        if following is not None:
            user.following.set(following)
        if bookmarked_ideas is not None:
            user.bookmarked_ideas.set(bookmarked_ideas)
        if bookmarked_implementations is not None:
            user.bookmarked_implementations.set(bookmarked_implementations)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class PublicUserSerializer(serializers.ModelSerializer):
    """For public user profile"""

    email = serializers.SerializerMethodField()

    def get_email(self, instance):
        return instance.email if instance.show_email else None

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "status",
            "description",
            "avatar",
            "following",
            "followers",
            "favourite_tags",
            "bookmarked_ideas",
            "bookmarked_implementations",
            "last_login",
            "date_joined",
        )
        read_only_fields = ("id", "last_login", "date_joined", "followers")

    def create(self, validated_data):
        raise NotImplementedError

    def update(self, instance, validated_data):
        raise NotImplementedError


class PasswordResetTokenSerializer(serializers.Serializer):
    """Serializer to get reset password token"""

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            return value
        raise ValidationError("Email does not exist")


class PasswordResetSerializer(serializers.Serializer):
    """Serializer to change password"""

    password = serializers.CharField(required=True, validators=(PasswordValidator(),))


class TokenObtainPairResponseSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenRefreshResponseSerializer(serializers.Serializer):
    access = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


class TokenVerifyResponseSerializer(serializers.Serializer):
    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()
