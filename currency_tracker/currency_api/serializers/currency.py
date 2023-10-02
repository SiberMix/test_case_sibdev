from rest_framework import serializers

from ..models import CurrencyQuote, TrackedQuote, QuoteAnalytics

class CurrencyQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrencyQuote
        fields = '__all__'

class TrackedQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackedQuote
        fields = '__all__'

class QuoteAnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteAnalytics
        fields = '__all__'

