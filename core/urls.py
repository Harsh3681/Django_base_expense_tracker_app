# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import ExpenseViewSet, sync_exchange_rate, report_monthly_spend

# router = DefaultRouter()
# router.register(r"expenses", ExpenseViewSet, basename="expense")

# urlpatterns = [
#     path("", include(router.urls)),
#     path("integrations/exchange-rate/", sync_exchange_rate),
#     path("reports/monthly-spend/", report_monthly_spend),
# ]



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ExpenseViewSet,
    dashboard,
)

router = DefaultRouter()
router.register("expenses", ExpenseViewSet, basename="expense")

urlpatterns = [
    # API
    path("api/", include(router.urls)),

    # UI
    path("dashboard/", dashboard, name="dashboard"),
]

