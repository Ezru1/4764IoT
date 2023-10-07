import requests

x = requests.get('http://api.weatherapi.com/v1/')
print(x.status_code) 