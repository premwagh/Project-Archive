from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from rangefilter.filters import DateTimeRangeFilter

from ..models import User
from .base import BaseUserAdmin


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "phone_number",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_email_verified",
        "last_login",
        "date_joined",
    )
    search_fields = ("email", "first_name", "last_name")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "password",
                    "first_name",
                    "last_name",
                    "date_of_birth",
                    "phone_number",
                    "is_email_verified",
                )
            },
        ),
        (
            _("Address"),
            {
                "fields": (
                    "address",
                    "city",
                    "state",
                    "country",
                    "zip_code",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Info"),
            {
                "fields": (
                    "created_on",
                    "updated_on",
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone_number", "password1", "password2", "department"),
            },
        ),
    )
