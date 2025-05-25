import requests

def get_weather(city, api_key):
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()
        weather = data['weather'][0]['main']
        return weather
    except:
        return "Unknown"
