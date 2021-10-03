from rest_framework import serializers

from accounts import views
from flaam_api.utils.primitives import sha1sum
from tags.serializers import TagSerializer

from .models import Idea


class IdeaSerializer(serializers.ModelSerializer):
    owner_avatar = serializers.SerializerMethodField(read_only=True)
    owner_username = serializers.SerializerMethodField(read_only=True)
    bookmarked = serializers.SerializerMethodField(read_only=True)
    viewed = serializers.SerializerMethodField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    vote = serializers.SerializerMethodField(read_only=True)
    upvote_count = serializers.IntegerField(read_only=True)
    downvote_count = serializers.IntegerField(read_only=True)
    implementation_count = serializers.IntegerField(read_only=True)

    def get_owner_avatar(self, obj):
        return obj.owner.avatar

    def get_owner_username(self, obj):
        return obj.owner.username

    def get_bookmarked(self, obj):
        request = self.context.get("request")
        if request is not None:
            return obj.bookmarked_by.filter(pk=request.user.pk).exists()
        return False

    def get_viewed(self, obj):
        request = self.context.get("request")
        if request is not None:
            return obj.views.filter(pk=request.user.pk).exists()
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
        ret = super().to_representation(instance)
        ret["tags"] = TagSerializer(instance.tags.all(), many=True).data
        return ret

    def to_internal_value(self, data):
        milestones = data.pop("milestones", None)
        ret = super().to_internal_value(data)
        if milestones:
            ret["milestones"] = [[sha1sum(m)[:8], m] for m in milestones]
        return ret

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
            "milestones",
            "draft",
            "bookmarked",
            "viewed",
            "view_count",
            "vote",
            "upvote_count",
            "downvote_count",
            "implementation_count",
            "created_at",
            "updated_at",
        )
