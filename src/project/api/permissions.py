from django.core.exceptions import ObjectDoesNotExist
from rest_framework.permissions import BasePermission

from user.models import User
from ..models import ProjectGroup

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
            if view.action in ('list', 'retrieve', 'calculate_uniqueness'):
                return True
            if request.user.role == User.RoleChoices.FACULTY:
                return view.action in ('approve', 'complete', 'reject')
            elif request.user.role == User.RoleChoices.STUDENT:
                return view.action not in ('approve', 'complete', 'reject')
        return False

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if view.action in ('list', 'retrieve'):
            return True
        group = obj.project_group
        if request.user.role == User.RoleChoices.STUDENT:
            return (
                group.created_by_id == request.user.id
                or group.students.filter(id=request.user.id).exists()
            )
        elif request.user.role == User.RoleChoices.FACULTY:
            return group.faculty_id == request.user.id
        return False
