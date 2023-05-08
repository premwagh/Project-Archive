from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjUserAdmin
from django.utils.translation import gettext_lazy as _

from rangefilter.filters import DateTimeRangeFilter

from ..models import Student
from .base import BaseUserAdmin


@admin.register(Student)
class StudentAdmin(BaseUserAdmin):
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
        "department",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("-date_joined",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "enrolment_number",
                    "password",
                    "first_name",
                    "last_name",
                    "date_of_birth",
                    "phone_number",
                    "department",
                    "is_email_verified",
                    "project_group",
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
    readonly_fields = ("project_group",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone_number", "password1", "password2", "enrolment_number", "department"),
            },
        ),
    )
