from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from PROJ3CT.api_v1 import api


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
    path("", include("PROJ3CT.core.urls")),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
