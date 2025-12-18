# from django.contrib import admin
# from django.urls import path, include
# from core.views import dashboard

# urlpatterns = [
#     path("admin/", admin.site.urls),
#     path("api/", include("core.urls")),
#     path("dashboard/", dashboard, name="dashboard"),
# ]


from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.shortcuts import redirect

def favicon(request):
    return HttpResponse(status=204)

def root_redirect(request):
    return redirect("/dashboard/")

urlpatterns = [
    path("", root_redirect),
    path("favicon.ico", favicon),
    path("admin/", admin.site.urls),

    # ✅ API namespace
    path("api/", include("core.urls")),
]


