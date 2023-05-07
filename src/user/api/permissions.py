from rest_framework.permissions import BasePermission

class UserPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        return True
