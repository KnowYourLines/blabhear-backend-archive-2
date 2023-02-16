from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import VideoNoteViewSet, TranscribeViewSet

router = DefaultRouter()
router.register(r"vidnote", VideoNoteViewSet, basename="vidnote")
router.register(r"transcribe", TranscribeViewSet, basename="transcribe")

urlpatterns = [
    path("", include(router.urls)),
]
