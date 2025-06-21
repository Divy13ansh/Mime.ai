from django.urls import path
from .views import TextToGlossView, AudioToGlossView, VideoToGlossView, TranslateToGlossView

urlpatterns = [
    path("api/text-to-gloss/", TextToGlossView.as_view()),
    path("api/audio-to-gloss/", AudioToGlossView.as_view()),
    path("api/video-to-gloss/", VideoToGlossView.as_view(), name="video-to-gloss"),
    path("api/translate-to-gloss/", TranslateToGlossView.as_view(), name="translate_to_gloss"),
    # path("api/sign-video-to-text/", SignVideoToTextView.as_view(), name="sign_to_text")

]
