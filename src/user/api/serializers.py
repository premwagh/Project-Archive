from django.utils import timezone
from rest_framework import serializers

from project.api.serializers import ProjectGroupSerializer
from project.models import ProjectGroup, ProjectGroupInvite
from ..settings import user_settings
from ..models import User, Student


class UserSerializer(serializers.ModelSerializer):
    """
    User Api.
    """
    enrolment_number = serializers.CharField(
        source='student_profile.enrolment_number',
        read_only=True,
    )
    project_group = serializers.PrimaryKeyRelatedField(
        source='student_profile.project_group',
        read_only=True,
    )
    project_group_status = serializers.CharField(
        source='student_profile.project_group.status',
        read_only=True,
    )

    class Meta:
        """
        User Serializer Meta class
        """
        model = User
        read_only_fields = (
            'id',
            'email'
            'is_staff',
            'is_superuser',
            'date_joined',
            'is_email_verified',
            'project_group',
            'created_on',
            'updated_on',
            'role',
        )
        exclude = (
            'last_login',
            'is_active',
            'groups',
            'user_permissions',
            'password',
            'date_joined',
            'is_superuser',
        )


class StudentCreateSerializer(serializers.ModelSerializer):

    """
    User Api.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(user.password)
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data.pop('password')
        return super().update(instance, validated_data)

    class Meta:
        """
        Student Serializer Meta class
        """
        model = Student
        read_only_fields = (
            'id',
            'email'
            'is_staff',
            'is_superuser',
            'date_joined',
            'is_email_verified',
            'project_group',
            'created_on',
            'updated_on',
        )
        exclude = (
            'last_login',
            'is_active',
            'groups',
            'user_permissions',
            'role'
        )

class ProjectGroupSerializer(serializers.ModelSerializer):
    """
    User Serializer.
    """

    class Meta:
        """
        User Serializer Meta class
        """
        model = ProjectGroup
        read_only_fields = (
            'id',
            'status',
            'faculty',
            'conformed_on',
            'conformed_by',
            'created_by',
            'created_on',
            'updated_on',
        )
        exclude = (
        )



class StudentProfileSerializer(serializers.ModelSerializer):

    project_group = ProjectGroupSerializer()

    class Meta:
        model = Student
        read_only_fields = (
            'project_group',
        )
        fields = (
            'enrolment_number',
            'project_group',
        )


class ProjectGroupInviteListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        # data = data.filter(
        #     status__in=(
        #         ProjectGroupInvite.StatusChoices.PENDING,
        #     ),
        #     expires_on__gt=timezone.now(),
        # )
        return super().to_representation(data)


class NestedPendingProjectGroupInviteSerializer(serializers.ModelSerializer):

    project_group = ProjectGroupSerializer()
    class Meta:
        list_serializer_class = ProjectGroupInviteListSerializer
        model = ProjectGroupInvite
        fields = (
            'id',
            'project_group',
            'is_expired',
            'status',
            # 'student',
            'expires_on',
            'created_by',
            'created_on',
            'updated_on',
        )



class UserMeSerializer(serializers.ModelSerializer):
    """
    User Me Serializer.
    """
    student_profile = StudentProfileSerializer()
    pending_invites = NestedPendingProjectGroupInviteSerializer(
        source='student_profile.invites',
        many=True,
        read_only=True,
    )
    class Meta:
        """
        User Me Serializer Meta class
        """
        model = User
        read_only_fields = (
            'id',
            'email',
            'role',
            'pending_invites',
            'is_staff',
            'is_superuser',
            'is_email_verified',
            'date_joined',
            'created_on',
            'updated_on',
        )
        exclude = (
            'password',
            'last_login',
            'is_active',
            'groups',
            'user_permissions',
        )
        extra_kwargs = {
            'phone_number': {'max_length': 16, 'min_length': 10}
        }


class PasswordSerializer(serializers.Serializer): # pylint: disable=W0223
    """
    Serializer for default password fields.
    """
    new_password = serializers.CharField(required=True, max_length=30)
    confirm_password = serializers.CharField(required=True, max_length=30)

    def validate(self, attrs):
        if attrs.get('confirm_password') != attrs.get('new_password'):
            raise serializers.ValidationError(
                {'confirm_password': "Passwords didn't match."})
        return attrs


class ChangePasswordSerializer(PasswordSerializer): # pylint: disable=W0223
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True, max_length=30)

    def validate_old_password(self, value):
        user = self.context['view'].get_object()
        if not user.check_password(value):
            raise serializers.ValidationError("Wrong password.")
        return value


class EmailSerializer(serializers.Serializer):  # pylint: disable=W0223
    """
    Serializer for requesting verification link or password reset link.
    """
    email = serializers.EmailField(max_length=255)


class VerifyTokenSerializer(serializers.Serializer):  # pylint: disable=W0223
    """
    Serializer for Token
    """
    token = serializers.CharField(max_length=512)


class ResetPasswordSerializer(PasswordSerializer, VerifyTokenSerializer): # pylint: disable=W0223
    """
    Serializer for reset user's password by token.
    """
