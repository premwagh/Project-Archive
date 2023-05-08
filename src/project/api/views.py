from django.utils import timezone
from rest_framework import status
from rest_framework.viewsets import (
    ModelViewSet,
)
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from core.drf.utils import response_error_msg, response_success_msg
from ..models import (
    ProjectGroup,
)
from ..settings import project_settings
from .permissions import ProjectGroupsPermission
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
        permission_classes=(IsAuthenticated, ProjectGroupsPermission,),
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
        permission_classes=(IsAuthenticated, ProjectGroupsPermission,),
    )
    def invite(self, request, *args, **kwargs):
        """
        Action for user password change.
        """
        instance = self.get_object()
        if not instance.status == ProjectGroup.StatusChoices.CONFORMED:
            return response_error_msg(f"Group status is '{instance.status}', can not invite student")
        return super().create(request, *args, **kwargs)

