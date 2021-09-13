from django.conf import settings
from django.db import models


class Implementation(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    body = models.TextField(blank=True)
    repo_url = models.URLField(blank=True)
    draft = models.BooleanField(default=True)
    tags = models.ManyToManyField(
        "tags.Tag", blank=True, related_name="implementation_tags"
    )
    completed_milestones = models.ManyToManyField(
        "ideas.Milestone",
        blank=True,
        related_name="completed_implementations",
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


class ImplementationComment(models.Model):
    implementation = models.ForeignKey(Implementation, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="upvoted_implementation_comments",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
