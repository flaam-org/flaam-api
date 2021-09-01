from django.contrib import admin

from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at", "updated_at")
    search_fields = ("name", "description", "created_by")
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "name",
                    "description",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


admin.site.register(Tag, TagAdmin)
