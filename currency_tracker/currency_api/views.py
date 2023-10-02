from datetime import datetime

from django.views.decorators.cache import cache_page
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers.user_serializers import UserRegistrationSerializer
from .serializers.user_serializers import UserLoginSerializer
from .serializers.currency import *

@swagger_auto_schema(
    method='post',
    request_body=UserRegistrationSerializer,
    responses={201: 'Пользователь успешно зарегистрирован', 400: 'Неверные данные запроса'}
)
@api_view(['POST'])
def register_user(request):
    """
    Регистрация пользователя
    :param request: параметры
    :return: результат регистрации 201 или 400
    """
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": " Пользователь успешно зарегистрирован"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=UserLoginSerializer,
    responses={201: 'Пользователь успешно зарегистрирован', 400: 'Неверные данные запроса'}
)
@api_view(['POST'])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data.get('user')
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({"access_token": access_token}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'sort',  # Имя параметра
            openapi.IN_QUERY,  # Где параметр будет передаваться (в запросе)
            description='Сортировка котировок (asc - по возрастанию, desc - по убыванию)',
            type=openapi.TYPE_STRING,
            enum=['asc', 'desc'],  # Допустимые значения
            default='asc',  # Значение по умолчанию
        ),
    ]
)
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@cache_page(60 * 5)  # Кэшировать ответ на 5 минут
def latest_currency_rates(request):
    # Получаем параметр сортировки из запроса (по умолчанию сортировка по возрастанию)
    sort_order = request.query_params.get('sort', 'asc')

    # Получаем последние котировки с возможной сортировкой
    if sort_order == 'asc':
        latest_quotes = CurrencyQuote.objects.order_by('value')
    else:
        latest_quotes = CurrencyQuote.objects.order_by('-value')

    serializer = CurrencyQuoteSerializer(latest_quotes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
def user_currency_add(request):
    """
    Добавление котируемой валюты в список отслеживаемых с установкой порогового значения
    """
    serializer = TrackedQuoteSerializer(data=request.data)
    if serializer.is_valid():
        # Убедитесь, что пользователь указан в запросе
        serializer.validated_data['user'] = request.user
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
def currency_analytics(request, id):
    try:
        threshold = float(request.query_params.get('threshold', 0))
        date_from = request.query_params.get('date_from', '')
        date_to = request.query_params.get('date_to', '')

        # Преобразуем даты в объекты datetime
        date_from = datetime.strptime(date_from, '%Y-%m-%d') if date_from else None
        date_to = datetime.strptime(date_to, '%Y-%m-%d') if date_to else None

        # Получаем котировки для заданной валюты и периода
        quotes = CurrencyQuote.objects.filter(
            quoted_currency=id,
            date__range=(date_from, date_to)
        )

        # Выполняем анализ и создаем сериализатор для результатов
        analytics = []
        for quote in quotes:
            threshold_exceeded = quote.value > threshold
            max_value = quote.value == max(quotes, key=lambda x: x.value).value
            min_value = quote.value == min(quotes, key=lambda x: x.value).value
            percentage_difference = (quote.value - threshold) / threshold * 100 if threshold != 0 else 0

            analytics.append({
                'quote': quote.id,
                'threshold_exceeded': threshold_exceeded,
                'max_value': max_value,
                'min_value': min_value,
                'percentage_difference': percentage_difference,
                'date': quote.date,
            })

        serializer = QuoteAnalyticsSerializer(analytics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)