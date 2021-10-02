from rest_framework import serializers

from accounts import views
from tags.serializers import TagSerializer

from .models import Idea


class IdeaSerializer(serializers.ModelSerializer):
    owner_avatar = serializers.SerializerMethodField()
    owner_username = serializers.SerializerMethodField()
    view_count = serializers.IntegerField()
    implementation_count = serializers.IntegerField()
    upvote_count = serializers.IntegerField()
    downvote_count = serializers.IntegerField()
    viewed = serializers.SerializerMethodField()
    bookmarked = serializers.SerializerMethodField()
    vote = serializers.SerializerMethodField()

    def get_owner_avatar(self, obj):
        return obj.owner.avatar

    def get_owner_username(self, obj):
        return obj.owner.username

    def get_viewed(self, obj):
        request = self.context.get("request")
        if request is not None:
            return obj.views.filter(pk=request.user.pk).exists()
        return False

    def get_bookmarked(self, obj):
        request = self.context.get("request")
        if request is not None:
            return obj.bookmarked_by.filter(pk=request.user.pk).exists()
        return False

    def get_vote(self, obj):
        request = self.context.get("request")
        if request is not None:
            if obj.upvotes.filter(pk=request.user.pk).exists():
                return 1
            elif obj.downvotes.filter(pk=request.user.pk).exists():
                return -1
        return 0

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["tags"] = TagSerializer(instance.tags.all(), many=True).data
        return representation

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Idea
        fields = (
            "id",
            "title",
            "owner",
            "owner_avatar",
            "owner_username",
            "description",
            "body",
            "tags",
            "draft",
            "viewed",
            "bookmarked",
            "view_count",
            "vote",
            "implementation_count",
            "upvote_count",
            "downvote_count",
            "milestones",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "owner", "created_at", "updated_at")
