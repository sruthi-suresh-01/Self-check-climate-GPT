import requests
import schedule
import time

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

def store_alerts_in_file(zip_codes, alerts_by_zip):
    with open('weather_alerts.txt', 'w') as file:
        for zip_code in zip_codes:
            alerts = alerts_by_zip[zip_code]
            file.write(f"Zip Code: {zip_code}\n")
            if isinstance(alerts, list):
                for alert in alerts:
                    file.write(f"  Headline: {alert['properties']['headline']}\n")
                    file.write(f"  Area: {alert['properties']['areaDesc']}\n")
                    file.write(f"  Description: {alert['properties']['description']}\n")
                    file.write("\n")
            else:
                file.write("  No geographic data found\n")
            file.write("\n")

def main(zip_codes, opencage_api_key):
    alerts_by_zip = {}
    for zip_code in zip_codes:
        lat, lon = get_coordinates(zip_code, opencage_api_key)
        if lat and lon:
            alerts = get_weather_alerts(lat, lon)
            alerts_by_zip[zip_code] = alerts
        else:
            alerts_by_zip[zip_code] = "No geographic data found"
    store_alerts_in_file(zip_codes, alerts_by_zip)
    print("Alerts stored successfully.")

# List of zip codes
zip_codes = ['92507', '60304', '77590']
opencage_api_key = 'c7cca7e08657441a8b6de18c87f21a2f'  

# Schedule the job every 4 hours
schedule.every(4).hours.do(main, zip_codes, opencage_api_key)

# Run the scheduling in a loop
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute to run the scheduled task
