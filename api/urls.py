from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import VideoNoteViewSet

router = DefaultRouter()
router.register(r"vidnote", VideoNoteViewSet, basename="vidnote")

urlpatterns = [
    path("", include(router.urls)),
]
