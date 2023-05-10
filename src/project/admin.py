from django.contrib import admin
from django import forms
from taggit.forms import TagField
from taggit_labels.widgets import LabelWidget



from .models import (
    ProjectGroup,
    ProjectGroupInvite,
    ProjectIdea,
)


@admin.register(ProjectGroup)
class ProjectGroupAdmin(admin.ModelAdmin):
    readonly_fields = [
        # 'name',
        # 'faculty',
        'status',
        'conformed_on',
        'conformed_by',
        'created_by',
        'created_on',
        'updated_on',
    ]



@admin.register(ProjectGroupInvite)
class ProjectGroupInviteAdmin(admin.ModelAdmin):
    readonly_fields = [
        'project_group',
        'status',
        'student',
        'expires_on',
        'created_by',
        'created_on',
        'updated_on',
    ]

class ProjectIdeaForm(forms.ModelForm):
    tags = TagField(required=False, widget=LabelWidget)


@admin.register(ProjectIdea)
class ProjectIdeaAdmin(admin.ModelAdmin):
    form = ProjectIdeaForm
    readonly_fields = [
        # 'title',
        # 'project_group',
        # 'report_content',
        # 'abstract_content',
        'uniqueness',
        # 'tags',
        'status',
        'approved_on',
        'completed_on',
        'created_on',
        'updated_on',
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')
