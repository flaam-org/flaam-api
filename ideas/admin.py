from django.contrib import admin

from .models import Idea


class IdeaAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "created_at", "updated_at", "draft")
    list_display_links = list_display
    list_filter = ("created_at", "updated_at", "draft")
    filter_horizontal = ("tags", "views", "upvotes", "downvotes")
    search_fields = ("title", "description", "body", "owner__email", "owner__username")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")


admin.site.register(Idea, IdeaAdmin)
