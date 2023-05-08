from rest_framework import serializers

from ..models import ProjectGroup, ProjectGroupInvites, ProjectIdea
from .serializer_fields import FacultyField


class ProjectGroupSerializer(serializers.ModelSerializer):
    """
    User Serializer.
    """
    faculty = FacultyField()

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
    """
    User Serializer.
    """


    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user.student_profile
        validated_data['project_group'] = self.context['view'].get_object()
        return super().create(validated_data)

    class Meta:
        """
        User Serializer Meta class
        """
        model = ProjectGroupInvites
        fields = (
            'student',
        )





