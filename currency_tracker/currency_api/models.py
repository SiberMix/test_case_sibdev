from django.db import models
from django.contrib.auth.models import User



class CurrencyQuote(models.Model):
    base_currency = models.CharField(max_length=3)
    quoted_currency = models.CharField(max_length=3)
    date = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=4)

class TrackedQuote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quote = models.ForeignKey(CurrencyQuote, on_delete=models.CASCADE)
    threshold_value = models.DecimalField(max_digits=10, decimal_places=4)

class QuoteAnalytics(models.Model):
    quote = models.ForeignKey(CurrencyQuote, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    threshold_exceeded = models.BooleanField()
    max_value = models.BooleanField()
    min_value = models.BooleanField()
    percentage_difference = models.DecimalField(max_digits=10, decimal_places=4)
    date = models.DateTimeField(auto_now_add=True)
