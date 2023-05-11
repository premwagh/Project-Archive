from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from taggit.serializers import (TagListSerializerField, TaggitSerializer)

from user.models import User
from ..models import (
    ProjectGroup,
    ProjectGroupInvite,
    ProjectIdea,
)
from .serializer_fields import FacultyField


class ProjectGroupInviteListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.exclude(
            status__in=(
                ProjectGroupInvite.StatusChoices.ACCEPTED,
            )
        )
        return super().to_representation(data)


class NestedPendingProjectGroupInviteSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = ProjectGroupInviteListSerializer
        model = ProjectGroupInvite
        fields = (
            'id',
            'project_group',
            'is_expired',
            'status',
            'student',
            'expires_on',
            'created_by',
            'created_on',
            'updated_on',
        )


class ProjectGroupSerializer(serializers.ModelSerializer):
    """
    User Serializer.
    """
    faculty = FacultyField()
    invites = NestedPendingProjectGroupInviteSerializer(
        many=True,
        read_only=True,
    )

    def create(self, validated_data):
        request = self.context.get('request')
        if request:
            validated_data['created_by_id'] = request.user.id
        return super().create(validated_data)

    class Meta:
        """
        User Serializer Meta class
        """
        model = ProjectGroup
        read_only_fields = (
            'id',
            'status',
            'invites',
            # 'faculty',
            'conformed_on',
            'conformed_by',
            'created_by',
            'created_on',
            'updated_on',
        )
        exclude = (
        )


class ProjectGroupInviteCreateSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user.student_profile
        validated_data['project_group'] = self.context['view'].get_object()
        return super().create(validated_data)

    class Meta:
        model = ProjectGroupInvite
        read_only_fields = (
            'id',
            'project_group',
            'status',
            # 'student',
            'expires_on',
            'created_by',
            'created_on',
            'updated_on',
        )
        fields = (
            'id',
            'project_group',
            'student',
            'status',
            'is_expired',
            'expires_on',
            'created_by',
            'created_on',
            'updated_on',
        )


class ProjectIdeaSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    def create(self, validated_data):
        validated_data['project_group'] = self.context['request'].user.student_profile.project_group
        return super().create(validated_data)

    def validate(self, attrs):
        request = self.context['request']
        # action = self.context['view'].action
        if request.user.role == User.RoleChoices.STUDENT:
                try:
                    project_group = request.user.student_profile.project_group
                except ObjectDoesNotExist as e:
                    raise serializers.ValidationError("Please complete Student profile.")
                else:
                    if not project_group:
                        raise serializers.ValidationError("You do not belong to any group.")
                    if project_group.status != ProjectGroup.StatusChoices.CONFORMED:
                        raise serializers.ValidationError(f"Your group '{project_group.name}' is not conformed.")

        return super().validate(attrs)

    class Meta:
        model = ProjectIdea
        read_only_fields = (
            'id',
            'project_group',
            'uniqueness',
            'status',
            'approved_on',
            'completed_on',
            'created_on',
            'updated_on',
        )
        fields = (
            'id',
            'project_group',
            'title',
            'report_content',
            'abstract_content',
            'tags',
            'uniqueness',
            'status',
            'approved_on',
            'completed_on',
            'submitted_on',
            'created_on',
            'updated_on',

        )