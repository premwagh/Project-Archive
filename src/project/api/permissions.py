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
                return (
                    obj.created_by_id == request.user.id
                    # obj.faculty_id == request.user.id
                    or obj.students.filter(id=request.user.id).exists()
                )
        except ObjectDoesNotExist:
            pass
        return False;

class ProjectGroupInvitePermission(BasePermission):

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
                return (
                    obj.created_by_id == request.user.id
                    # or obj.faculty_id == request.user.id
                    or obj.students.filter(id=request.user.id).exists()
                )
        except ObjectDoesNotExist:
            pass
        return False;


class ProjectIdeaPermission(BasePermission):

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
                return (
                    obj.created_by_id == request.user.id
                    # or obj.faculty_id == request.user.id
                    or obj.students.filter(id=request.user.id).exists()
                )
        except ObjectDoesNotExist:
            pass
        return False;
