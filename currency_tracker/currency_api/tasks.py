from celery import shared_task
from .models import CurrencyQuote
import requests
from datetime import datetime, timedelta

@shared_task
def update_currency_data():
    # Здесь выполните запрос к API ЦБ РФ и обновление котировок в БД
    try:
        response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        data = response.json()

        # Преобразуйте данные из API и сохраните их в БД (псевдокод)
        for currency, rate in data['Valute'].items():
            base_currency = 'RUB'
            quoted_currency = currency
            date = datetime.strptime(data['Date'], '%Y-%m-%dT%H:%M:%SZ')
            value = rate['Value']
            CurrencyQuote.objects.create(
                base_currency=base_currency,
                quoted_currency=quoted_currency,
                date=date,
                value=value
            )

        # Удалите старые записи, оставив только последние 30 дней
        thirty_days_ago = datetime.now() - timedelta(days=30)
        CurrencyQuote.objects.filter(date__lt=thirty_days_ago).delete()
    except Exception as e:
        # Обработайте ошибку
        print(f"Error updating currency data: {str(e)}")
