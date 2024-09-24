import requests

def get_zip_code(lat, lon, api_key):
    """Fetch zip code using OpenCage Geocoder API."""
    url = f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key={api_key}"
    response = requests.get(url).json()
    # Check if results are available and postcode exists
    if response['results']:
        return response['results'][0]['components'].get('postcode')
    else:
        return "Zip code not found"  # Return a default message or handle as needed

# Fetch the IP address
ip_address = requests.get('http://api.ipify.org').text
print(ip_address)

# Fetch geographical data based on IP address
geo_data = requests.get(f'http://ip-api.com/json/{ip_address}').json()
print(geo_data)

# Extract latitude and longitude
lat = geo_data['lat']
lon = geo_data['lon']

print(lat)
print(lon)

# Attempt to fetch zip code from initial API, fallback to OpenCage if empty
zip_code = geo_data['zip'] or get_zip_code(lat, lon, 'your_opencage_api_key')  # Replace 'your_opencage_api_key' with your actual API key

# Fetch weather alerts for the given location
response = requests.get(f'https://api.weather.gov/alerts?point={lat},{lon}').json()
print(f'Alerts: {len(response["features"])}')

# Open a text file for writing the alerts and IP data
with open('alert.txt', 'w') as file:
    # Writing IP and geographical information
    file.write(f"IP Address: {ip_address}\n")
    file.write("Geographical Information:\n")
    file.write(f"  Country: {geo_data['country']}\n")
    file.write(f"  Country Code: {geo_data['countryCode']}\n")
    file.write(f"  Region: {geo_data['regionName']}\n")
    file.write(f"  City: {geo_data['city']}\n")
    file.write(f"  Zip Code: {zip_code}\n")
    file.write(f"  Latitude: {lat}\n")
    file.write(f"  Longitude: {lon}\n")
    file.write(f"  Timezone: {geo_data['timezone']}\n")
    file.write(f"  ISP: {geo_data['isp']}\n")
    file.write(f"  AS: {geo_data['as']}\n")
    file.write("\n")

    # Writing alerts
    for x in response['features']:
        file.write(f"Headline: {x['properties']['headline']}\n")
        file.write(f"Area: {x['properties']['areaDesc']}\n")
        file.write(f"Description: {x['properties']['description']}\n")
        file.write("\n")
