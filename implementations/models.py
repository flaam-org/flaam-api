from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models


class Implementation(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="implementations",
    )
    idea = models.ForeignKey(
        "ideas.Idea", on_delete=models.CASCADE, related_name="implementations"
    )
    description = models.TextField(max_length=500, blank=True)
    body = models.TextField(blank=True)
    repo_url = models.URLField(blank=True)
    draft = models.BooleanField(default=True)
    is_validated = models.BooleanField(default=False)
    is_accepted = models.BooleanField(default=False)
    tags = models.ManyToManyField(
        "tags.Tag", blank=True, related_name="implementation_tags"
    )
    completed_milestones = ArrayField(
        models.CharField(max_length=10), size=20, default=list, blank=True
    )
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="upvoted_implementations"
    )
    downvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="downvoted_implementations"
    )
    views = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="viewed_implementations"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"IMPL{self.id}"


class ImplementationComment(models.Model):
    implementation = models.ForeignKey(
        Implementation, on_delete=models.CASCADE, related_name="comments"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="implementation_comments",
    )
    body = models.TextField(max_length=500)
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="upvoted_implementation_comments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"IMPLCOM{self.id}"
