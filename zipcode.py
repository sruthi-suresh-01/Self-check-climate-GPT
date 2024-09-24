import requests

def get_coordinates(zip_code, api_key):
    """Convert zip code to latitude and longitude using OpenCage Geocoder."""
    url = f"https://api.opencagedata.com/geocode/v1/json?q={zip_code}&key={api_key}&countrycode=us"
    response = requests.get(url).json()
    if response['results']:
        lat = response['results'][0]['geometry']['lat']
        lon = response['results'][0]['geometry']['lng']
        return lat, lon
    return None, None

def get_weather_alerts(lat, lon):
    """Fetch weather alerts using latitude and longitude."""
    url = f"https://api.weather.gov/alerts?point={lat},{lon}"
    response = requests.get(url).json()
    return response['features']

def main(zip_codes, opencage_api_key):
    alerts_by_zip = {}
    for zip_code in zip_codes:
        lat, lon = get_coordinates(zip_code, opencage_api_key)
        if lat and lon:
            alerts = get_weather_alerts(lat, lon)
            alerts_by_zip[zip_code] = alerts
        else:
            alerts_by_zip[zip_code] = "No geographic data found"
    return alerts_by_zip

# Example usage
zip_codes = ['92507', '60304', '77590']  # List of zip codes
opencage_api_key = 'c7cca7e08657441a8b6de18c87f21a2f'  # Replace with your actual API key
alerts = main(zip_codes, opencage_api_key)
for zip_code, alert in alerts.items():
    print(f"Zip Code: {zip_code}, Alerts: {len(alert) if isinstance(alert, list) else alert}")

