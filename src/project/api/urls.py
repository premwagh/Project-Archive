from rest_framework.routers import SimpleRouter

from .views import (
    ProjectGroupViewSet,
    ProjectGroupInviteViewSet,
    ProjectIdeaViewSet,
)

app_name = 'project'

router = SimpleRouter()
router.register('group', ProjectGroupViewSet, basename="group")
router.register('group-invite', ProjectGroupInviteViewSet, basename="group-invite")
router.register('idea', ProjectIdeaViewSet, basename="idea")

urlpatterns = [
]+ router.urls
