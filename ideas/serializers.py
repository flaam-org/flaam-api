from rest_framework import serializers

from .models import Idea, Milestone


class MilestoneListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        try:
            idea = self.context["idea"]
        except KeyError:
            raise serializers.ValidationError("Idea is not specified")
        milestones = [Milestone(idea=idea, **item) for item in validated_data]
        return Milestone.objects.bulk_create(milestones)

    def update(self, instance, validated_data):
        try:
            idea = self.context["idea"]
        except KeyError:
            raise serializers.ValidationError("Idea is not specified")
        # TODO: find if there is better way to do this
        for item in validated_data:
            if instance.idea_id != idea.id:
                raise serializers.ValidationError("Cannot change unrelated milestones")
            instance.title = item["title"]
            instance.save()
        return instance


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ("id", "title", "idea", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
        list_serializer_class = MilestoneListSerializer


class IdeaSerializer(serializers.ModelSerializer):

    upvotes_count = serializers.SerializerMethodField()
    downvotes_count = serializers.SerializerMethodField()
    vote = serializers.SerializerMethodField()
    milestones = MilestoneSerializer(read_only=True, many=True)

    def get_upvotes_count(self, obj):
        return obj.upvotes.count()

    def get_downvotes_count(self, obj):
        return obj.downvotes.count()

    def get_vote(self, obj):
        request = self.context.get("request")
        if request is not None:
            if obj.upvotes.filter(pk=request.user.pk).exists():
                return "up"
            elif obj.downvotes.filter(pk=request.user.pk).exists():
                return "down"
        return None

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
            "description",
            "body",
            "tags",
            "vote",
            "upvotes_count",
            "downvotes_count",
            "milestones",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")
