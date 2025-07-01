from django.urls import path
from .views import UnifiedGlossView, Ping
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("api/process/", UnifiedGlossView.as_view(), name="unified_gloss"),
    path("api/ping/",Ping.as_view(), name = "ping"),
    path("", health_check),
]
