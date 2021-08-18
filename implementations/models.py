from django.conf import settings
from django.db import models

from tags.models import Tag


class Implementation(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(max_length=500)
    body = models.TextField(blank=True)
    repo_url = models.URLField(blank=True)
    # TODO: milestones field
    tags = models.ManyToManyField(Tag, related_name="implementation_tags")
    draft = models.BooleanField(default=True)
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="implementation_upvotes"
    )
    downvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="implementation_downvotes"
    )
    views = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="implementation_views"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ImplementationComment(models.Model):
    implementation = models.ForeignKey(Implementation, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="implementation_comment_upvotes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
