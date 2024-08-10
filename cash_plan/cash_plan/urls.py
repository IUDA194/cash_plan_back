"""cash_plan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from cash_plan.settings import APPLICATION_VERSION

schema_view = get_schema_view(
   openapi.Info(
      title="HMICST Api",
      default_version='v1',
      description="Swagger — это набор инструментов для проектирования, построения и документирования RESTful API. Он позволяет разработчикам легко создавать спецификации API, которые можно использовать для автоматической генерации документации, тестирования и даже создания клиентского кода. Swagger предоставляет визуальный интерфейс, где можно увидеть все доступные эндпоинты API, их параметры, типы данных и возможные ответы, что делает взаимодействие с API простым и понятным как для разработчиков, так и для пользователей.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="popmsee@gmail.com"),
      license=openapi.License(name="BIMBam License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


base_url = f'api/v{APPLICATION_VERSION}/'

urlpatterns = [
    #Swagger
    path(f'{base_url}swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(f'{base_url}swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(f'{base_url}redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    #Admin
    path(f'{base_url}admin/', admin.site.urls),
    
    #Apps
    path(f'{base_url}users/', include('users.urls')),
    path(f'{base_url}plans/', include('plans.urls')),
    path(f'{base_url}currency/', include('currency.urls')),

]
