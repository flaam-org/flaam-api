from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer"""

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "status",
            "description",
            "avatar",
            "last_login",
            "date_joined",
        )
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ("id", "last_login", "date_joined")

    def create(self, validated_data):
        return UserModel.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)


class PublicUserSerializer(serializers.ModelSerializer):
    """For public user profile"""

    class Meta:
        model = UserModel
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "status",
            "description",
            "avatar",
            "last_login",
            "date_joined",
        )


class ResetPasswordTokenSerializer(serializers.Serializer):
    """Serializer to get reset password token"""

    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            return value
        raise ValidationError("Email does not exist")
