from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('weather/current/<str:location>/', views.get_weather_current, name='get_weather_current'),
    path('weather/history/<str:location>,<str:dt>/', views.get_weather_history, name='get_weather_history'),
    path('weather/forecast/<str:location>,<str:days>/', views.get_weather_forecast, name='get_weather_forecast'),
    path('nws/forecast/<str:location>/', views.get_nws_forecast, name='nws_weather_forecast'),
    path('nws/forecastHourly/<str:location>/', views.get_nws_hourly_forecast, name='nws_weather_hourly_forecast'),
    path('data/<str:location>/', views.get_combined_observations, name='get_combined_observations'),
]
