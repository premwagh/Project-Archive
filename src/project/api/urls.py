from rest_framework.routers import SimpleRouter

from .views import (
    ProjectGroupViewSet,
)

app_name = 'project'
router = SimpleRouter()
router.register('group', ProjectGroupViewSet, basename="group")
router.register('group-invites', ProjectGroupViewSet, basename="group")

urlpatterns = [
]+ router.urls
