from django.contrib import admin
from djangoql.admin import DjangoQLSearchMixin

from .models import Discussion, DiscussionComment


class DiscussionAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ("id", "owner", "idea", "title", "draft", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "draft")
    search_fields = ("title", "body")
    readonly_fields = ("created_at", "updated_at")


class DiscussionCommentAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ("id", "owner", "discussion", "body", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("body",)
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Discussion, DiscussionAdmin)
admin.site.register(DiscussionComment, DiscussionCommentAdmin)
