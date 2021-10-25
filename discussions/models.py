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
        settings.AUTH_USER_MODEL, blank=True, related_name="upvoted_discussions"
    )
    downvotes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="downvoted_discussions"
    )
    views = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="viewed_discussions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class DiscussionComment(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
