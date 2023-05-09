from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from user.models import User

class FacultySerializer(serializers.ModelSerializer):
    """
    Faculty Serializer.
    """
    class Meta:
        """
        User Serializer Meta class
        """
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'department',
        )



class FacultyField(serializers.RelatedField):
    queryset = User.objects.filter(role=User.RoleChoices.FACULTY)

    def to_representation(self, obj):
        # return obj.pk
        return FacultySerializer(obj).data

    def to_internal_value(self, data):
        queryset = self.get_queryset()
        try:
            return queryset.get(pk=data)
        except queryset.model.DoesNotExist:
            raise serializers.ValidationError(
            f'{queryset.model._meta.verbose_name} id {data} does not exist.'
        )

    def get_queryset(self):
        queryset = super().get_queryset()
        # try:
        #     if self.context['request'].user == User.RoleChoices.STUDENT:
        #         department = self.context['request'].user.student_profile.department
        #     else:
        #         department = self.context['request'].user.faculty_profile.department
        # except ObjectDoesNotExist:
        #     department=''
        # queryset = queryset.filter(department=department)
        return queryset
