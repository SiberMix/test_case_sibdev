from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Спецификация API для тестового задания Currencies",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Оставим AllowAny для доступа к Swagger
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('currency_api.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),


]
