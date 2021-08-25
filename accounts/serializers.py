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
        if validated_data["password"]:
            user = UserModel.objects.create(**validated_data)
            user.set_password(validated_data["password"])
            user.save()
        else:
            raise ValidationError("Password is required")

        return user

    def update(self, instance, validated_data):
        if validated_data["password"]:
            instance.set_password(validated_data["password"])
        instance.save()
        return instance


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
