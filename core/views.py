# from django.db.models import Sum
# from django.db.models.functions import TruncMonth
# from django.shortcuts import render
# from rest_framework import viewsets, status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# from .models import Expense, ExchangeRate
# from .serializers import ExpenseSerializer, ExchangeRateSerializer
# from .services import fetch_exchange_rate

# class ExpenseViewSet(viewsets.ModelViewSet):
#     queryset = Expense.objects.all().order_by("-created_at")
#     serializer_class = ExpenseSerializer

# @api_view(["POST"])
# def sync_exchange_rate(request):
#     base = request.data.get("base", "USD")
#     target = request.data.get("target", "INR")

#     try:
#         rate = fetch_exchange_rate(base, target)
#         obj = ExchangeRate.objects.create(base=base.upper(), target=target.upper(), rate=rate)
#         return Response(ExchangeRateSerializer(obj).data, status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["GET"])
# def report_monthly_spend(request):
#     qs = (
#         Expense.objects
#         .annotate(month=TruncMonth("created_at"))
#         .values("month")
#         .annotate(total=Sum("amount"))
#         .order_by("month")
#     )
#     data = [{"month": row["month"].date().isoformat(), "total": str(row["total"] or 0)} for row in qs]
#     return Response(data)

# def dashboard(request):
#     return render(request, "dashboard.html")


from django.shortcuts import render
from django.urls import get_resolver

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Expense, ExchangeRate
from .serializers import ExpenseSerializer
from .services import fetch_exchange_rates


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    Public API for this demo app (no auth).
    Fixes CSRF issues by disabling Session auth requirement.
    """
    serializer_class = ExpenseSerializer
    permission_classes = [AllowAny]
    authentication_classes = []  # ✅ IMPORTANT: avoids CSRF/session auth issues

    def get_queryset(self):
        qs = Expense.objects.all().order_by("-created_at")

        category = self.request.query_params.get("category")
        start = self.request.query_params.get("startDate")
        end = self.request.query_params.get("endDate")

        if category and category != "all":
            qs = qs.filter(category=category)

        if start:
            qs = qs.filter(created_at__date__gte=start)

        if end:
            qs = qs.filter(created_at__date__lte=end)

        return qs


@api_view(["POST"])
def sync_exchange_rate(request):
    """
    Fetch latest exchange rates from API and store them as JSON in ExchangeRate.rates
    """
    try:
        base = (request.data.get("base") or "USD").upper()
        rates = fetch_exchange_rates(base)

        # keep only one row (latest)
        ExchangeRate.objects.all().delete()

        obj = ExchangeRate.objects.create(
            base=base,
            rates=rates
        )

        return Response({
            "base": obj.base,
            "count": len(obj.rates or {}),
            "status": "ok"
        })
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(["GET"])
def latest_rates(request):
    """
    Returns: { base: "USD", rates: { "USD": 1, "INR": 83.2, ... } }
    ✅ FIXED: works with JSONField rates (NOT target/rate columns)
    """
    latest = ExchangeRate.objects.order_by("-fetched_at").first()
    if not latest or not latest.rates:
        return Response({"base": "USD", "rates": {}})

    rates = dict(latest.rates)

    # Ensure base currency exists
    if latest.base and latest.base not in rates:
        rates[latest.base] = 1.0

    return Response({
        "base": latest.base,
        "rates": rates
    })


@api_view(["GET"])
def debug_urls(request):
    resolver = get_resolver()
    return Response([str(p) for p in resolver.url_patterns])


def dashboard(request):
    return render(request, "dashboard.html")
