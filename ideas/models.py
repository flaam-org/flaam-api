from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Idea(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ideas"
    )
    description = models.TextField(max_length=500, blank=True)
    body = models.TextField(blank=True)
    milestones = ArrayField(
        ArrayField(
            models.CharField(max_length=255),
            size=2,
        ),
        size=10,
        default=list,
        blank=True,
    )
    tags = models.ManyToManyField("tags.Tag", related_name="idea_tags")
    draft = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="upvoted_ideas"
    )
    downvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="downvoted_ideas"
    )
    views = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="viewed_ideas"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"IDEA{self.id}"
