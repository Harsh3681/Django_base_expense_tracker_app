from django.contrib import admin
from .models import Expense, ExchangeRate

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "amount", "currency", "category", "created_at")
    search_fields = ("note",)
    list_filter = ("category", "currency")

@admin.register(ExchangeRate)
class ExchangeRateAdmin(admin.ModelAdmin):
    list_display = ("base", "fetched_at", "rate_count")
    list_filter = ("base",)
    readonly_fields = ("rates", "fetched_at")

    def rate_count(self, obj):
        return len(obj.rates or {})

    rate_count.short_description = "Currencies"