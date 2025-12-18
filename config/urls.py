from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect
from core.views import dashboard


def favicon(request):
    return HttpResponse(status=204)


def root_redirect(request):
    return redirect("/dashboard/")


urlpatterns = [
    path("", root_redirect),
    path("favicon.ico", favicon),

    # UI
    path("dashboard/", dashboard, name="dashboard"),

    # Admin
    path("admin/", admin.site.urls),

    # API (IMPORTANT)
    path("api/", include("core.urls")),
]




