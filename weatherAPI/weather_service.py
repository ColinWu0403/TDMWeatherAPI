import requests
from django.conf import settings

def fetch_current_weather_data(city: str):
    """
    Fetch weather data for a given city from WeatherAPI.com.

    Args:
        city (str): The city name to fetch weather data for.

    Returns:
        dict: The JSON response from WeatherAPI.com or an error message.
    """
    api_key = settings.WEATHER_API_KEY
    base_url = "http://api.weatherapi.com/v1/current.json"

    params = {
        'key': api_key,
        'q': city,
        'aqi': 'yes',  # Air Quality Index, optional
        'alerts': 'yes' 
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        return {'error': f'HTTP error occurred: {http_err}'}
    except requests.exceptions.ConnectionError as conn_err:
        return {'error': f'Connection error occurred: {conn_err}'}
    except requests.exceptions.Timeout as timeout_err:
        return {'error': f'Timeout error occurred: {timeout_err}'}
    except requests.exceptions.RequestException as req_err:
        return {'error': f'An error occurred: {req_err}'}

def fetch_forecast_weather_data(city: str):
    """
    Fetch forecast data for a given city from WeatherAPI.com.

    Args:
        city (str): The city name to fetch weather data for.

    Returns:
        dict: The JSON response from WeatherAPI.com or an error message.
    """
    api_key = settings.WEATHER_API_KEY
    base_url = "http://api.weatherapi.com/v1/forecast.json"

    params = {
        'key': api_key,
        'q': city,
        'aqi': 'yes',  # Air Quality Index, optional
        'alerts': 'yes' 
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return data
    except requests.exceptions.HTTPError as http_err:
        return {'error': f'HTTP error occurred: {http_err}'}
    except requests.exceptions.ConnectionError as conn_err:
        return {'error': f'Connection error occurred: {conn_err}'}
    except requests.exceptions.Timeout as timeout_err:
        return {'error': f'Timeout error occurred: {timeout_err}'}
    except requests.exceptions.RequestException as req_err:
        return {'error': f'An error occurred: {req_err}'}
