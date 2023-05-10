from django.utils import timezone
from rest_framework import status
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

import django_filters

from core.drf.utils import response_error_msg, response_success_msg
from ..settings import project_settings
from ..models import (
    ProjectGroup,
    ProjectGroupInvite,
    ProjectIdea,
)
from .permissions import (
    ProjectGroupsPermission,
    ProjectGroupInvitePermission,
    ProjectIdeaPermission,
)
from .serializers import (
    ProjectGroupSerializer,
    ProjectGroupInviteCreateSerializer,
    ProjectIdeaSerializer,
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
            instance.status = ProjectGroup.StatusChoices.CONFORMED
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


class ProjectGroupInviteFilterSet(django_filters.FilterSet):
    """
    Facility FilterSet
    """

    class Meta:
        model = ProjectGroupInvite
        fields = {
            'status':     ['exact', 'in'],
            'created_by': ['exact', 'in'],
        }


class ProjectGroupInviteViewSet(ReadOnlyModelViewSet):
    """
    get: List all the invite.
    """

    filterset_class = ProjectGroupInviteFilterSet
    ordering_fields = '__all__'
    search_fields = ['status', 'profile_category']
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


class ProjectIdeaFilterSet(django_filters.FilterSet):
    """
    Facility FilterSet
    """
    tags = django_filters.CharFilter(field_name='tags__name', lookup_expr='exact')
    tags__iexact = django_filters.CharFilter(field_name='tags__name', lookup_expr='iexact')
    tags__in = django_filters.CharFilter(field_name='tags__name', lookup_expr='in')


    class Meta:
        model = ProjectIdea
        fields = {
            'title':       ['icontains', 'exact', 'in'],
            'status':     ['exact', 'in'],
            'uniqueness': ['gt', 'gte', 'lt', 'lte', 'range'],
            'completed_on': ['year', 'year__gt', 'year__gte', 'year__lt', 'year__lte', 'range'],
            'approved_on': ['year', 'year__gt', 'year__gte', 'year__lt', 'year__lte', 'range'],
            'created_on': ['year', 'year__gt', 'year__gte', 'year__lt', 'year__lte', 'range', 'date', 'date__range'],
        }


class ProjectIdeaViewSet(ModelViewSet):
    """
    get: List all the invite.
    """

    filterset_class = ProjectIdeaFilterSet
    ordering_fields = '__all__'
    search_fields = ['status', 'profile_category']
    ordering = ('created_on',)

    queryset = ProjectIdea.objects.get_queryset()
    permission_classes = (ProjectIdeaPermission,)
    serializer_class = ProjectIdeaSerializer

    @action(
        detail=True,
        methods=["get"],
        name="Calculate Uniqueness",
        url_name="Calculate Uniqueness",
        url_path="calculate_uniqueness",
    )
    def calculate_uniqueness(self, request, *args, **kwargs):
        """
        Action to calculate uniqueness of project idea.
        """
        instance = self.get_object()
        if not instance.status in (ProjectIdea.StatusChoices.NEW, ProjectIdea.StatusChoices.PENDING):
            return response_error_msg(f"Can not perform this action, status is '{instance.status}'.")
        instance.calculate_uniqueness(save=True)
        return super().retrieve(request, *args, **kwargs)

    @action(
        detail=True,
        methods=["post"],
        name="Submit",
        url_name="Submit",
        url_path="submit",
        serializer_class=serializers.Serializer,
    )
    def submit(self, request, *args, **kwargs):
        """
        Action to submit project idea.
        """
        instance = self.get_object()
        if not instance.status == ProjectIdea.StatusChoices.NEW:
            return response_error_msg(f"Can not perform this action, status is '{instance.status}'.")
        instance.submit()
        return response_success_msg("Idea is submitted.")

    @action(
        detail=True,
        methods=["post"],
        name="Approve",
        url_name="Approve",
        url_path="approve",
        serializer_class=serializers.Serializer,
    )
    def approve(self, request, *args, **kwargs):
        """
        Action to approve project idea.
        """
        instance = self.get_object()
        if not instance.status == ProjectIdea.StatusChoices.PENDING:
            return response_error_msg(f"Can not perform this action, status is '{instance.status}'.")
        instance.approve()
        return response_success_msg("Idea is approved.")

    @action(
        detail=True,
        methods=["post"],
        name="Reject",
        url_name="Reject",
        url_path="reject",
        serializer_class=serializers.Serializer,
    )
    def reject(self, request, *args, **kwargs):
        """
        Action to reject project idea.
        """
        instance = self.get_object()
        if not instance.status == ProjectIdea.StatusChoices.PENDING:
            return response_error_msg(f"Can not perform this action, status is '{instance.status}'.")
        instance.reject()
        return response_success_msg("Idea is rejected.")

    @action(
        detail=True,
        methods=["post"],
        name="Complete",
        url_name="Complete",
        url_path="complete",
        serializer_class=serializers.Serializer,
    )
    def complete(self, request, *args, **kwargs):
        """
        Action to complete project idea.
        """
        instance = self.get_object()
        if not instance.status == ProjectIdea.StatusChoices.COMPLETED:
            return response_error_msg(f"Can not perform this action, status is '{instance.status}'.")
        instance.approve()
        return response_success_msg("Idea is Completed.")

