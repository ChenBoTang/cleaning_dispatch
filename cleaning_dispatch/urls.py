from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("esp32/", include("device.urls")),
    path("", include("dispatch.urls")),
]
