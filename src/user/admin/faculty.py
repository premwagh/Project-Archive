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

    def get_queryset(self, request):
            qs = super().get_queryset(request)
            return qs.filter(role=Faculty.RoleChoices.FACULTY)

    def save_model(self, request: Any, obj: Any, form: Any, change: Any) -> None:
        obj.role = Faculty.RoleChoices.FACULTY
        return super().save_model(request, obj, form, change)
