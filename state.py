import requests
import json
state='CA'

response=requests.get(f'https://api.weather.gov/alerts/active?area={state}').json()
# print(response)
response_better=json.dumps(response,indent=2)
print(response_better)

for x in response['features']:
    print(x['properties']['areaDesc'])
    # print(x['properties']['headLine'])
    print(x['properties']['description'])
    print('\n*********\n')