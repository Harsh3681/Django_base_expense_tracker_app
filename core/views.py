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
    try:
        rates = fetch_exchange_rates(base)
        obj = ExchangeRate.objects.create(base=base.upper(), rates=rates)
        return Response({"id": obj.id, "base": obj.base, "fetched_at": obj.fetched_at, "count": len(rates)}, status=201)
    except Exception as e:
        return Response({"error": str(e)}, status=400)

@api_view(["GET"])
def report_monthly_spend(request):
    qs = (
        Expense.objects
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("month")
    )

    data = [
        {"month": row["month"].date().isoformat(), "total": str(row["total"] or 0)}
        for row in qs
    ]
    return Response(data)

@api_view(["GET"])
def latest_rates(request):
    latest = ExchangeRate.objects.order_by("-fetched_at").first()
    if not latest:
        return Response({"base": "USD", "rates": {}})
    return Response({"base": latest.base, "rates": latest.rates})

def dashboard(request):
    return render(request, "dashboard.html")
