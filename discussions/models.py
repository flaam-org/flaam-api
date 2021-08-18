from django.conf import settings
from django.db import models

from tags.models import Tag


class Discussion(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, related_name="discussion_tags")
    draft = models.BooleanField(default=True)
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="discussion_upvotes"
    )
    downvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="discussion_downvotes"
    )
    views = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="discussion_views"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DiscussionComment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    upvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="discussion_comment_upvotes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
