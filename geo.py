import requests


ip_address=requests.get('http://api.ipify.org').text
print(ip_address)

geo_data=requests.get(f'http://ip-api.com/json/{ip_address}').json()
print(geo_data)

lat=geo_data['lat']
lon=geo_data['lon']

print(lat)
print(lon)
response=requests.get(f'https://api.weather.gov/alerts?point={lat},{lon}').json()
print(f'Alerts:{len(response['features'])}')

file=open('alert.html','w')
for x in response['features']:
    file.write(f"<h1>{x['properties']['headline']}</h1>")
    file.write(f"<h3>{x['properties']['areaDesc']}</h3>")
    file.write(f"<p>{x['properties']['description']}</p>")
file.close()