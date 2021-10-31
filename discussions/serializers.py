from rest_framework import serializers

from .models import Discussion, DiscussionComment


class DiscussionSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source="owner.username", read_only=True)
    owner_avatar = serializers.CharField(source="owner.avatar", read_only=True)
    viewed = serializers.SerializerMethodField(read_only=True)
    view_count = serializers.IntegerField(read_only=True)
    vote = serializers.SerializerMethodField(read_only=True)
    upvote_count = serializers.IntegerField(read_only=True)
    downvote_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

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
        data = super().to_representation(instance)
        print(data)
        return data

    class Meta:
        model = Discussion
        fields = (
            "id",
            "idea",
            "title",
            "body",
            "owner",
            "owner_username",
            "owner_avatar",
            "viewed",
            "draft",
            "view_count",
            "vote",
            "upvote_count",
            "downvote_count",
            "comments_count",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("owner",)


class DiscussionCommentSerializer(serializers.ModelSerializer):
    owner_avatar = serializers.CharField(source="owner.avatar", read_only=True)
    owner_username = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = DiscussionComment
        fields = (
            "id",
            "discussion",
            "body",
            "owner",
            "owner_avatar",
            "owner_username",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("owner",)
