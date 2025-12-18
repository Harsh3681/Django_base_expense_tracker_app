from rest_framework import serializers
from .models import Expense, ExchangeRate

class ExpenseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(required=False)
    class Meta:
        model = Expense
        fields = ["id", "amount", "currency", "category", "note", "created_at"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "created_at": {"required": False}
        }

class ExchangeRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRate
        fields = ["id", "base", "target", "rate", "fetched_at"]
        read_only_fields = ["id", "rate", "fetched_at"]
