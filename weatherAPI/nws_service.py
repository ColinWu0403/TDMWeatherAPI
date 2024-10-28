import requests

def get_weather_location(latitude, longitude):
    """Fetch location data from NWS API."""
    location_url = f"https://api.weather.gov/points/{latitude},{longitude}"
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
