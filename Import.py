import requests

data = requests.get("https://api.iextrading.com/1.0/deep?symbols=amzn")
#print(data.status_code)
#print(data.headers)
print(data.json())