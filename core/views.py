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


from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import render

from django.urls import get_resolver

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ExchangeRate

from .models import Expense, ExchangeRate
from .serializers import ExpenseSerializer, ExchangeRateSerializer
from .services import fetch_exchange_rates

class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

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
    base = request.data.get("base", "USD")

    # fetch from API (you already have this working)
    data = fetch_exchange_rates(base)

    ExchangeRate.objects.filter(base=base).delete()

    for target, rate in data["rates"].items():
        ExchangeRate.objects.create(
            base=base,
            target=target,
            rate=rate
        )

    return Response({"status": "ok"})

@api_view(["GET"])
def latest_rates(request):
    qs = ExchangeRate.objects.all()

    if not qs.exists():
        return Response({
            "base": "USD",
            "rates": {}
        })

    base = qs.first().base
    rates = {r.target: float(r.rate) for r in qs}

    # 🔥 IMPORTANT: include base currency as 1
    rates[base] = 1.0

    return Response({
        "base": base,
        "rates": rates
    })

@api_view(["GET"])
def debug_urls(request):
    resolver = get_resolver()
    urls = []

    for pattern in resolver.url_patterns:
        urls.append(str(pattern))

    return Response(urls)


def dashboard(request):
    return render(request, "dashboard.html")
