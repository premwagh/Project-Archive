from typing import Any
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from rangefilter.filters import DateTimeRangeFilter

from ..models import Faculty
from .base import BaseUserAdmin



@admin.register(Faculty)
class FacultyAdmin(BaseUserAdmin):
    """
    Usr Admin
    """

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
    list_filter = (
        "is_email_verified",
        "is_superuser",
        "is_staff",
        "is_active",
        ("created_on", DateTimeRangeFilter),
        ("updated_on", DateTimeRangeFilter),
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-date_joined",)
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
                    "department",
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
    readonly_fields = ()

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone_number", "password1", "password2", "department"),
            },
        ),
    )

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.role = Faculty.RoleChoices.FACULTY
        return super().save_model(request, obj, form, change)
