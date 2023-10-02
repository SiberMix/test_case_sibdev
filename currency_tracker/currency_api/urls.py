from django.urls import path
from . import views

urlpatterns = [
    path('user/register/', views.register_user, name='register_user'),
    path('user/login/', views.login_user, name='login_user'),
    path('rates/', views.latest_currency_rates, name='latest_currency_rates'),
    path('currency/user_currency/', views.user_currency_add, name='user_currency_add'),
    path('currency/<int:id>/analytics/', views.currency_analytics, name='currency_analytics'),

]
