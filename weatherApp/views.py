from django.shortcuts import render
import os
import requests

# Create your views here.

def home(request):
    return render(request, "home.html",)

def weather(request):
    city_id = request.POST['cityname'].capitalize()
    API_KEY = os.environ.get("WEATHER_API_KEY")  # get the API key from the environment variable
    url = "https://api.openweathermap.org/data/2.5/" \
          "weather?q={}&appid={}&units=metric".format(city_id.casefold(), API_KEY)
    r = requests.get(url)
    data = r.json()

    try:
        temperature = int(data["main"]["temp"])
        weather_description = data["weather"][0]["description"].title()
        humidity = data["main"]["humidity"]
        icon = data["weather"][0]["icon"]
        max_temp = int(data["main"]["temp_max"])
        min_temp = int(data["main"]["temp_min"])
        wind = int(data["wind"]["speed"])
        iconlink = "http://openweathermap.org/img/w/{}.png".format(icon)
        return render(request, "result.html",
                      {"cityname": city_id, "temperature": temperature, "description": weather_description,
                       "humidity": humidity, "icon": icon, "maxTemp": max_temp, "minTemp": min_temp, "wind": wind, "iconurl":iconlink})

    except:
        city_not_found = "I could Not find the weather for '{}', Please try another City".format(city_id)
        return render(request, "resultnotFound.html", {"notFound":city_not_found})

