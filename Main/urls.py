from django.urls import path
from .views import UnifiedGlossView
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("api/process/", UnifiedGlossView.as_view(), name="unified_gloss"),
    path("", health_check),
]
