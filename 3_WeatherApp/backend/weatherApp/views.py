from django.shortcuts import render
from dotenv import load_dotenv
import os, requests
from .models import City
from .forms import CityForm

def index_view(request):
    # load the env file
    load_dotenv()
    # get the api key
    API_KEY = os.getenv("WEATHER_API_KEY")
    # openweather api
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid={}'
    
    # get all cities
    cities = City.objects.all()
    # prepare the blank form
    form = CityForm()
    
    # if the user attempts a search
    if request.method == "POST":
        form = CityForm(request.POST)
        # check if the form is valid
        if form.is_valid():
            form.save()
        
    weather_data = []
    
    for city in cities:
        city_weather = requests.get(url.format(city, API_KEY)).json()
    
        weather = {
            'city' : city,
            'temperature' : convert_farenhit_to_celcius(city_weather['main']['temp']),
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }
        
        weather_data.append(weather)
    
    context = {
        'weather_data' : weather_data,
        "form": form,
    }
    
    return render(
        request,
        "weatherApp/index.html",
        context
    )
    
def convert_farenhit_to_celcius(temp: int) -> int:
    
    res = (temp-32) * (5/9)
    
    return round(res)