from django.contrib import admin
from djangoql.admin import DjangoQLSearchMixin

from .models import Implementation, ImplementationComment


class ImplementationAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ("id", "owner", "idea", "title", "draft", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at", "draft")
    search_fields = ("name", "description")
    readonly_fields = ("created_at", "updated_at")


class ImplementationCommentAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ("id", "owner", "implementation", "body", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("body",)
    readonly_fields = ("created_at", "updated_at")


admin.site.register(Implementation, ImplementationAdmin)
admin.site.register(ImplementationComment, ImplementationCommentAdmin)
