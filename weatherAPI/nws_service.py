import requests
import json
import os

def get_weather_location(location):
    """Fetch location data from NWS API."""
    
    file_path = os.path.join(os.path.dirname(__file__), "locations.json")
    with open(file_path) as f:
        location_coords = json.load(f)
    
    # Check if the location exists in the dictionary
    if location.lower() not in location_coords:
        return {'error': 'Location not found in the list of available locations.'}

    # Retrieve coordinates for the given location
    coords = location_coords[location.lower()]
    lat, lon = coords['lat'], coords['lon']
    
    location_url = f"https://api.weather.gov/points/{lat},{lon}"
    response = requests.get(location_url)

    if response.status_code != 200:
        return None, response.status_code

    return response.json(), None
  
def get_forecast(forecast_url):
    """Fetch forecast data from NWS API."""
    response = requests.get(forecast_url)

    if response.status_code != 200:
        return None, response.status_code

    return response.json(), None

def get_forecast_hourly(forecast_hourly_url):
    """Fetch hourly forecast data from NWS API."""
    response = requests.get(forecast_hourly_url)

    if response.status_code != 200:
        return None, response.status_code

    return response.json(), None
