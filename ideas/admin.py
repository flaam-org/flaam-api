from django.contrib import admin
from django.http import request
from djangoql.admin import DjangoQLSearchMixin

from .models import Idea, Milestone


class MilestoneAdmin(admin.ModelAdmin):
    ...


class MileStoneInline(admin.TabularInline):
    model = Milestone
    show_change_link = True
    extra = 1
    max_num = 20


class IdeaAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    readonly_fields = ("id", "created_at", "updated_at")
    list_display = ("title", "owner", "created_at", "updated_at", "draft")
    list_display_links = list_display
    list_filter = ("created_at", "updated_at", "draft")
    filter_horizontal = ("tags", "views", "upvotes", "downvotes")
    inlines = (MileStoneInline,)
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
            None,
            {
                "fields": (
                    "id",
                    "owner",
                    "draft",
                    "title",
                    "description",
                    "body",
                    "tags",
                )
            },
        ),
        (
            "Metadata",
            {
                "fields": (
                    "views",
                    "upvotes",
                    "downvotes",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


admin.site.register(Idea, IdeaAdmin)
admin.site.register(Milestone, MilestoneAdmin)
