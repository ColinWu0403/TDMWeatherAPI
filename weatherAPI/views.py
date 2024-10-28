from django.shortcuts import render
from django.http import JsonResponse
from .weather_service import fetch_current_weather_data, fetch_forecast_weather_data
from .nws_service import get_weather_location, get_forecast, get_forecast_hourly
import logging

logger = logging.getLogger(__name__)

def get_weather_current(request, location):
    # Fetch weather data using the weather_service.py function
    data = fetch_current_weather_data(location)
    
    if data:
        return JsonResponse(data)  # Return the data as JSON response
    else:
        return JsonResponse({'error': 'Unable to fetch weather data'}, status=500)

def get_weather_forecast(request, location):
    # Fetch weather data using the weather_service.py function
    data = fetch_forecast_weather_data(location)
    
    if data:
        return JsonResponse(data)  # Return the data as JSON response
    else:
        return JsonResponse({'error': 'Unable to fetch weather data'}, status=500)

def get_nws_forecast(request, latitude, longitude):
    try:
        lat = float(latitude)
        lon = float(longitude)

        # Get location data
        location_data, location_error = get_weather_location(lat, lon)
        if location_error:
            return JsonResponse({'error': 'Failed to retrieve location data.'}, status=location_error)

        # Extract the forecast URL
        forecast_url = location_data['properties']['forecast']

        # Fetch forecast data
        forecast_data, forecast_error = get_forecast(forecast_url)
        if forecast_error:
            return JsonResponse({'error': 'Failed to retrieve forecast data.'}, status=forecast_error)

        return JsonResponse({'forecast': forecast_data})

    except ValueError:
        return JsonResponse({'error': 'Invalid latitude or longitude.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An internal server error occurred.'}, status=500)

def get_nws_hourly_forecast(request, latitude, longitude):
    try:
        lat = float(latitude)
        lon = float(longitude)

        # Get location data
        location_data, location_error = get_weather_location(lat, lon)
        if location_error:
            return JsonResponse({'error': 'Failed to retrieve location data.'}, status=location_error)

        # Extract the hourly forecast URL
        forecast_hourly_url = location_data['properties']['forecastHourly']

        # Fetch hourly forecast data
        hourly_forecast_data, hourly_error = get_forecast_hourly(forecast_hourly_url)
        if hourly_error:
            return JsonResponse({'error': 'Failed to retrieve hourly forecast data.'}, status=hourly_error)

        return JsonResponse({'hourly_forecast': hourly_forecast_data})

    except ValueError:
        return JsonResponse({'error': 'Invalid latitude or longitude.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'An internal server error occurred.'}, status=500)
