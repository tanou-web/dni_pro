from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({
        "status": "ok"
    })


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/gestion_actu/', include('gestion_actu.urls')),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # Health check pour Render / UptimeRobot
    path("health/", health_check, name="health_check"),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )