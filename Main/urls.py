from django.urls import path
from .views import TextToGlossView, AudioToGlossView, VideoToGlossView

urlpatterns = [
    path("api/text-to-gloss/", TextToGlossView.as_view()),
    path("api/audio-to-gloss/", AudioToGlossView.as_view()),
    path("api/video-to-gloss/", VideoToGlossView.as_view(), name="video-to-gloss"),
]
