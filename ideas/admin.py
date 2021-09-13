from django.contrib import admin
from djangoql.admin import DjangoQLSearchMixin

from .models import Idea


class IdeaAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    readonly_fields = ("id", "created_at", "updated_at")
    list_display = ("title", "owner", "created_at", "updated_at", "draft")
    list_display_links = list_display
    list_filter = ("created_at", "updated_at", "draft")
    filter_horizontal = ("tags", "views", "upvotes", "downvotes")
    search_fields = (
        "title",
        "description",
        "body",
        "owner__email",
        "owner__username",
    )
    ordering = ("-created_at",)
    fieldsets = (
        (
            "General",
            {
                "fields": (
                    "id",
                    "owner",
                    "draft",
                    "title",
                    "description",
                    "body",
                    "tags",
                    "views",
                    "upvotes",
                    "downvotes",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


admin.site.register(Idea, IdeaAdmin)
