from rest_framework.routers import SimpleRouter

from .views import (
    ProjectGroupViewSet,
    ProjectGroupInviteViewSet
)

app_name = 'project'
router = SimpleRouter()
router.register('group', ProjectGroupViewSet, basename="group")
router.register('group-invite', ProjectGroupInviteViewSet, basename="group")

urlpatterns = [
]+ router.urls
