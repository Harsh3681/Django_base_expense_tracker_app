from django.db import models
from django.utils.timezone import now

class Expense(models.Model):
    class Category(models.TextChoices):
        FOOD = "Food", "Food"
        TRANSPORT = "Transport", "Transport"
        ENTERTAINMENT = "Entertainment", "Entertainment"
        BILLS = "Bills", "Bills"
        HEALTHCARE = "Healthcare", "Healthcare"
        SHOPPING = "Shopping", "Shopping"
        OTHER = "Other", "Other"

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="INR")
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER
    )
    note = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=now)


    def __str__(self):
        return f"{self.amount} {self.currency} - {self.category}"

class ExchangeRate(models.Model):
    base = models.CharField(max_length=3, default="USD")
    rates = models.JSONField(default=dict)  # stores ALL rates mapping
    fetched_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
         return f"Rates {self.base} @ {self.fetched_at}"
