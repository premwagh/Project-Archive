from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission

from user.models import User

class ProjectGroupsPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            if view.action == 'create':
                return request.user.role == User.RoleChoices.STUDENT
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        try:
            if request.user.role == User.RoleChoices.STUDENT:
                return request.user.student_profile.project_group_id == obj.id
        except ObjectDoesNotExist:
            pass
        return False;
