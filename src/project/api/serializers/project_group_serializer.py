from rest_framework import serializers

from ..models import ProjectGroup

class ProjectGroupSerializer(serializers.ModelSerializer):
    """
    User Serializer.
    """

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
        User Serializer Meta class
        """
        model = ProjectGroup
        read_only_fields = (
            'id',
            'status',
            'conformed_on',
            'created_on',
            'updated_on',
        )
        exclude = (
            'last_login',
            'is_active',
            'groups',
            'user_permissions',
        )
        extra_kwargs = {
            'phone_number': {'max_length': 16, 'min_length': 10}
        }


class UserMeSerializer(serializers.ModelSerializer):
    """
    User Me Serializer.
    """

    class Meta:
        """
        User Me Serializer Meta class
        """
        model = User
        read_only_fields = (
            'id',
            'email',
            'is_staff',
            'is_superuser',
            'is_phone_verified',
            'date_joined',
            'is_email_verified',
            'is_mfa_enabled',
            'is_approved',
            'approved_on',
            'approved_by',
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
