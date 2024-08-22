from django.shortcuts import render
from django.http import JsonResponse

from .models import City
from .forms import CityForm
from django.conf import settings

import os, requests
from iteration_utilities import unique_everseen

# WILL REFACTOR MOST OF THE VIEWS TO CLASS BASED VIEWS

def index_view(request):
    # get all cities
    cities = City.objects.all()
    # prepare the blank form
    form = CityForm()
    
    # # if the user attempts a search
    # if request.method == "POST":
    #     form = CityForm(request.POST)
    #     # check if the form is valid
    #     if form.is_valid():
    #         form.save()
        
    weather_data = get_weather_data(cities)
    
    context = {
        'weather_data' : weather_data,
        "form": form,
    }
    
    return render(
        request,
        "weatherApp/index.html",
        context
    )

def get_weather_data(cities) -> list:
    weather_data = []
    
    for city in cities:
        city_weather = requests.get(settings.API_URL.format(city, settings.API_KEY)).json()
    
        weather = {
            'city' : str(city),
            'temperature' : convert_farenhit_to_celcius(city_weather['main']['temp']),
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon']
        }
        
        weather_data.append(weather)
    
    return weather_data

def convert_farenhit_to_celcius(temp: int) -> int:
    
    res = (temp-32) * (5/9)
    
    return round(res)

def search_results(request):
    # on Djano 3.1 and higher, we will acquiring x-requested-with using get
    # and compare if it is XMLHttpRequest
    # on lower version, request.is_ajax() is a must.
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        search_query = request.POST.get("search_query")
        
        # check if the city is in the model database (will change soon)
        # temporary way to avoid errors in city searching through the API
        search_results = City.objects.filter(name__icontains=search_query)

        # check if the search query being passed by the ajax is less than 2 characters
        # and if no filtered resultes, get all available cities instead
        if (len(search_query) < 2 and len(search_results) <= 0):
            search_results = City.objects.all()
        
        # fetch the weather data from the api
        weather_data = get_weather_data(search_results)
        
        # everseen to avoid duplicate send to the frontend
        res = list(unique_everseen(weather_data))
        
        # return the result to the front-end
        return JsonResponse({"data": res})
    
    return JsonResponse()