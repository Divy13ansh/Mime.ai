from django.urls import path
from .views import UnifiedGlossView

urlpatterns = [
    path("api/process/", UnifiedGlossView.as_view(), name="unified_gloss")
]
