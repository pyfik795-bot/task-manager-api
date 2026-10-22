import requests

host = "google.com"



try:
     response = requests.get(
         f"https://{host}",
         timeout=5
    )

except requests as error:
     print(f"HTTP ошибка: {error}")

print(response)
