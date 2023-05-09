from rest_framework import serializers

from project.api.serializers import ProjectGroup
from ..settings import user_settings
from ..models import User, Student


class StudentSerializer(serializers.ModelSerializer):
    """
    User Api.
    """
    class Meta:
        """
        User Serializer Meta class
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
            'role',
            'password',
        )


class StudentCreateSerializer(StudentSerializer):

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

    class Meta(StudentSerializer.Meta):
        """
        Student Serializer Meta class
        """
        exclude = (
            'last_login',
            'is_active',
            'groups',
            'user_permissions',
            'role'
        )

class StudentProfileSerializer(serializers.ModelSerializer):

    project_group = ProjectGroup()

    class Meta:
        model = Student
        read_only_fields = (
            'project_group',
        )
        fields = (
            'enrolment_number',
            'project_group',
        )


class UserMeSerializer(serializers.ModelSerializer):
    """
    User Me Serializer.
    """
    student_profile = StudentProfileSerializer()
    class Meta:
        """
        User Me Serializer Meta class
        """
        model = User
        read_only_fields = (
            'id',
            'email',
            'role',
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
