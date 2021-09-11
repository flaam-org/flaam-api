from django.conf import settings
from django.db import models


class Idea(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    body = models.TextField()
    # TODO: milestones field
    tags = models.ManyToManyField("tags.Tag", related_name="idea_tags")
    draft = models.BooleanField(default=True)
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="idea_upvotes", blank=True
    )
    downvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="idea_downvotes", blank=True
    )
    views = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="idea_views", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"IDEA{self.id}"
