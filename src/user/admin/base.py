from itertools import chain
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjUserAdmin
from django.utils.translation import gettext_lazy as _

from rangefilter.filters import DateTimeRangeFilter


class BaseUserAdmin(DjUserAdmin):
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
                    "created_on"
                    "updated_on",
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )
    user_list_filter = (
        "is_email_verified",
        "role",
        "is_staff",
        "is_active",
        "is_active",
        ("created_on", DateTimeRangeFilter),
        ("updated_on", DateTimeRangeFilter),
    )
    user_readonly_fields = (
        "phone_number",
        "email",
        "is_active",
        "is_staff",
        "created_on",
        "updated_on",
        'is_email_verified',
        "date_joined",
        "is_superuser",
        "last_login",
    )
    list_per_page = 25
    list_max_show_all = 500

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "phone_number", "password1", "password2"),
            },
        ),
    )
    def has_delete_permission(self, request, obj=None):
        return bool(request.user.is_superuser)

    def get_list_filter(self, request):
        return self.merge_iterable(self.list_filter, self.user_list_filter)

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return ()
        return self.merge_iterable(self.readonly_fields, self.user_readonly_fields)

    @staticmethod
    def merge_iterable(*args):
        x=[]
        for e in chain(*args):
            if e not in x:
                x.append(e)
        return tuple(x)
