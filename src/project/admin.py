from django.contrib import admin

from .models import (
    ProjectGroup,
    ProjectGroupInvite,
)


@admin.register(ProjectGroup)
class ProjectGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectGroupInvite)
class ProjectGroupInviteAdmin(admin.ModelAdmin):
    pass

