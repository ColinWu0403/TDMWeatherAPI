from django.shortcuts import render
from django.http import JsonResponse
from .weather_service import fetch_current_weather_data, fetch_forecast_weather_data, fetch_history_weather_data
from .nws_service import get_weather_location, get_forecast, get_forecast_hourly
import os
import json
import requests

# The base URL of your SensorThings server
SENSORTHINGS_BASE_URL = 'https://labs.waterdata.usgs.gov/sta/v1.1/'

def get_combined_observations(request, location):
    json_file_path = os.path.join(os.path.dirname(__file__), 'locations.json')

    # Load the JSON data with the list of locations
    try:
        with open(json_file_path, 'r') as f:
            location_data = json.load(f)
        if location.title() not in location_data:
            return JsonResponse({'error': 'Location not found in defined locations.'}, status=404)
    except FileNotFoundError:
        return JsonResponse({'error': 'Locations file not found.'}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Error decoding locations file.'}, status=500)

    # Initialize combined data dictionary
    combined_data = {}

    # Get USGS Observations
    try:
        state = location_data[location.title()]['State']
        county = location_data[location.title()]['County']
        usgs_url = f'https://labs.waterdata.usgs.gov/sta/v1.1/Things?$filter=properties/state eq \'{state}\' and substringof(tolower(\'{county}\'), tolower(properties/county))&$select=@iot.id,description&$expand=Datastreams($select=@iot.id,description,unitOfMeasurement;$expand=Observations($select=result,phenomenonTime;$orderby=phenomenonTime desc;$top=1))'
        usgs_response = requests.get(usgs_url)
        usgs_response.raise_for_status()
        combined_data['USGS'] = usgs_response.json()
    except requests.exceptions.RequestException as e:
        combined_data['USGS'] = {'error': str(e)}
        
    # Get Current Weather from WeatherAPI
    try:
        weather_current_data = fetch_current_weather_data(location)
        combined_data['WeatherAPI_Current'] = weather_current_data if weather_current_data else {'error': 'No current weather data'}
    except Exception as e:
        combined_data['WeatherAPI_Current'] = {'error': str(e)}

    # Get Forecast Weather from WeatherAPI
    try:
        weather_forecast_data = fetch_forecast_weather_data(location, days="1")
        combined_data['WeatherAPI_Forecast'] = weather_forecast_data if weather_forecast_data else {'error': 'No forecast weather data'}
    except Exception as e:
        combined_data['WeatherAPI_Forecast'] = {'error': str(e)}

    # Get NWS Forecast
    try:
        nws_location_data, location_error = get_weather_location(location)
        if location_error:
            combined_data['NWS_Forecast'] = {'error': 'Failed to retrieve location data for NWS'}
        else:
            forecast_url = nws_location_data['properties']['forecast']
            nws_forecast_data, forecast_error = get_forecast(forecast_url)
            combined_data['NWS_Forecast'] = nws_forecast_data if not forecast_error else {'error': 'Failed to retrieve forecast data'}
    except Exception as e:
        combined_data['NWS_Forecast'] = {'error': str(e)}

    # Get NWS Hourly Forecast
    try:
        if nws_location_data:
            forecast_hourly_url = nws_location_data['properties']['forecastHourly']
            nws_hourly_data, hourly_error = get_forecast_hourly(forecast_hourly_url)
            combined_data['NWS_Hourly_Forecast'] = nws_hourly_data if not hourly_error else {'error': 'Failed to retrieve hourly forecast data'}
    except Exception as e:
        combined_data['NWS_Hourly_Forecast'] = {'error': str(e)}

    return JsonResponse(combined_data)
  

# def get_observations(request, location):
#     json_file_path = os.path.join(os.path.dirname(__file__), 'locations.json')

#     # Load the JSON data
#     with open(json_file_path, 'r') as f:
#         data = json.load(f)
    
#     state = data[location.title()]['State']
#     county = data[location.title()]['County']
#     # Construct the URL to fetch observations for a specific sensor
#     url = f'https://labs.waterdata.usgs.gov/sta/v1.1/Things?$filter=properties/state eq \'{state}\' and substringof(tolower(\'{county}\'), tolower(properties/county))&$select=@iot.id,description&$expand=Datastreams($select=@iot.id,description,unitOfMeasurement;$expand=Observations($select=result,phenomenonTime;$orderby=phenomenonTime desc;$top=1))'
    
#     try:
#         response = requests.get(url)
#         # Check if the request was successful
#         response.raise_for_status()
#         data = response.json()
#         return JsonResponse(data)
#     except requests.exceptions.RequestException as e:
#         return JsonResponse({'error': str(e)}, status=500)

def get_weather_current(request, location):
    # Fetch weather data using the weather_service.py function
    data = fetch_current_weather_data(location)
    
    if data:
        return JsonResponse(data)  # Return the data as JSON response
    else:
        return JsonResponse({'error': 'Unable to fetch weather data'}, status=500)

def get_weather_forecast(request, location, days="1"):
    # Fetch weather data using the weather_service.py function
    data = fetch_forecast_weather_data(location, days)
    
    if data:
        return JsonResponse(data)  # Return the data as JSON response
    else:
        return JsonResponse({'error': 'Unable to fetch weather data'}, status=500)

def get_weather_history(request, location, dt):
    # Fetch weather data using the weather_service.py function
    data = fetch_history_weather_data(location, dt)
    
    if 'error' in data:
        return JsonResponse(data, status=400)
    elif data:
        return JsonResponse(data)  # Return the data as JSON response
    else:
        return JsonResponse({'error': 'Unable to fetch weather data'}, status=500)

def get_nws_forecast(request, location):
    try:
        # Get location data
        location_data, location_error = get_weather_location(location)
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

def get_nws_hourly_forecast(request, location):
    try:

        # Get location data
        location_data, location_error = get_weather_location(location)
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
