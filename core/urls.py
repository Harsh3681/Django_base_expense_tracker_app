from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExpenseViewSet,
    dashboard,
    sync_exchange_rate,
    latest_rates,
    debug_urls,
)

router = DefaultRouter()
router.register("expenses", ExpenseViewSet, basename="expense")

urlpatterns = [
    # API
    path("", include(router.urls)),

    # integrations
    path("integrations/exchange-rate/", sync_exchange_rate),
    path("integrations/rates/", latest_rates),

    # UI
    # path("dashboard/", dashboard, name="dashboard"),
    path("debug/urls/", debug_urls),
]

