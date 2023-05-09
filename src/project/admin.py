from django.contrib import admin

from .models import (
    ProjectGroup,
    ProjectGroupInvite,
    ProjectIdea,
)


@admin.register(ProjectGroup)
class ProjectGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(ProjectGroupInvite)
class ProjectGroupInviteAdmin(admin.ModelAdmin):
    pass

@admin.register(ProjectIdea)
class ProjectIdeaAdmin(admin.ModelAdmin):
    pass

