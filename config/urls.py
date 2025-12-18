from django.contrib import admin
from django.urls import path, include
from core.views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
    path("dashboard/", dashboard, name="dashboard"),
]
