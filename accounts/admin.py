from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from djangoql.admin import DjangoQLSearchMixin
from rest_framework_simplejwt import token_blacklist

from .models import User


class UserAdmin(DjangoQLSearchMixin, BaseUserAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
    )
    list_display_links = list_display
    filter_horizontal = (
        *BaseUserAdmin.filter_horizontal,
        "following",
        "favourite_tags",
        "bookmarked_ideas",
        "bookmarked_implementations",
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                )
            },
        ),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "show_email",
                    "avatar",
                    "status",
                    "description",
                    "following",
                    "favourite_tags",
                    "bookmarked_ideas",
                    "bookmarked_implementations",
                )
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )


class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):
    # https://github.com/jazzband/djangorestframework-simplejwt/issues/266#issuecomment-820745103
    def has_delete_permission(self, *args, **kwargs):
        return True


admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)
admin.site.register(User, UserAdmin)
