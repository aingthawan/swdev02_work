import requests

# Lat-Lon of New York
URL = "https://weather.com/weather/today/l/40.75,-73.98"
print("\nRequesting . . .")
resp = requests.get(URL)

# print status
# 200 is successfully done
print("Request Status : ",resp.status_code)
# print(resp.text)