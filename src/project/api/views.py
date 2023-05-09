from django.utils import timezone
from rest_framework import status
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
    GenericViewSet,
    mixins,
)
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from core.drf.utils import response_error_msg, response_success_msg
from ..models import (
    ProjectGroup,
    ProjectGroupInvite,
)
from ..settings import project_settings
from .permissions import ProjectGroupsPermission, ProjectGroupInvitePermission
from .serializers import (
    ProjectGroupSerializer,
    ProjectGroupInviteCreateSerializer
)


class ProjectGroupViewSet(ModelViewSet):
    """
    get: List all the users.
    post: Create a new user.
    """

    ordering = ('created_on',)

    queryset = ProjectGroup.objects.get_queryset()
    permission_classes = (ProjectGroupsPermission,)
    serializer_class = ProjectGroupSerializer

    @action(
        detail=True,
        methods=["post"],
        name="Conform Group",
        url_name="Conform Group",
        url_path="conform-group",
        serializer_class=serializers.Serializer,
    )
    def conform_group(self, request, *args, **kwargs):
        """
        Action for user password change.
        """
        instance = self.get_object()
        if instance.status == ProjectGroup.StatusChoices.CONFORMED:
            return response_success_msg("Group Already conformed.")
        if instance.status == ProjectGroup.StatusChoices.FORMATION:
            instance.conformed_on = timezone.now()
            instance.conformed_by = request.user.student_profile
            instance.save()
            return response_success_msg("Group conformed.")
        return response_error_msg(f"Unexpected status '{instance.status}'!")

    @action(
        detail=True,
        methods=["post"],
        name="Invite Student",
        url_name="Invite",
        url_path="invite",
        serializer_class=ProjectGroupInviteCreateSerializer,
    )
    def invite(self, request, *args, **kwargs):
        """
        Action for user password change.
        """
        instance = self.get_object()
        if not instance.status == ProjectGroup.StatusChoices.FORMATION:
            return response_error_msg(f"Group status is '{instance.status}', can not invite student")
        return super().create(request, *args, **kwargs)


class ProjectGroupInviteViewSet(ReadOnlyModelViewSet):
    """
    get: List all the invite.
    """

    ordering = ('created_on',)

    queryset = ProjectGroupInvite.objects.get_queryset()
    permission_classes = (ProjectGroupInvitePermission,)
    serializer_class = ProjectGroupInviteCreateSerializer

    @action(
        detail=True,
        methods=["post"],
        name="Accept",
        url_name="Accept",
        url_path="accept",
        serializer_class=serializers.Serializer,
    )
    def accept(self, request, *args, **kwargs):
        """
        Action to accept project group invite.
        """
        instance = self.get_object()
        if not instance.status == ProjectGroupInvite.StatusChoices.PENDING:
            return response_error_msg(f"Can not perform this action, Invite status is '{instance.status}'.")
        if instance.is_expired:
            return response_error_msg("Invite is expired.")
        if not instance.project_group.status == ProjectGroup.StatusChoices.FORMATION:
            return response_error_msg(f"Group status is '{instance.project_group.status}', can not join the group")
        instance.accept_invite()
        return response_success_msg("invite is Accepted.")

    @action(
        detail=True,
        methods=["post"],
        name="Reject",
        url_name="Reject",
        url_path="reject",
        serializer_class=serializers.Serializer,
    )
    def reject(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_expired:
            return response_error_msg("Invite is expired.")
        instance.reject_invite()
        return response_success_msg("invite is rejected.")
