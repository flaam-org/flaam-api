from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
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
        *BaseUserAdmin.fieldsets,
        (
            "Custom Fiels",  # group heading
            {
                "fields": (
                    "avatar",
                    "status",
                    "description",
                ),
            },
        ),
    )


admin.site.register(User, UserAdmin)
