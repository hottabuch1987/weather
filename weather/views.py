import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import City
from rest_framework.views import APIView


weather_data = {}

def get_weather(request):
    cities = City.objects.filter(user=request.user).order_by('-search_count')
    context = {'cities': cities, 'weather_data': weather_data}
    return render(request, 'weather/index.html', context)


def add_city(request):
    global weather_data
    try:
        city_name = request.POST['city']
    except KeyError:
        return JsonResponse({'error': 'Invalid request'})

    try:
        existing_city = City.objects.filter(name=city_name, user=request.user).first()
        if existing_city:
            existing_city.search_count += 1
            existing_city.save()
        else:
  
            city = City(name=city_name, user=request.user)
            city.save()

        api_url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {
            "name": city_name
        }
        response = requests.get(api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            latitude = data['results'][0]['latitude']
            longitude = data['results'][0]['longitude']

            api_url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": latitude,
                "longitude": longitude,
                "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum",
                "hourly": ["temperature_2m", "precipitation"],
                "current": ["temperature_2m"]
            }
            response = requests.get(api_url, params=params)

            if response.status_code == 200:
                weather_data[city_name] = response.json()
            else:
                print(f"Failed to get data for city {city_name}. Error code: {response.status_code}")
        else:
            print(f"Failed to get geographical coordinates for city {city_name}. Error code: {response.status_code}")

    except KeyError:
        print(f"Geographical coordinates for city {city_name} not found.")
    except requests.RequestException as e:
        print(f"Error making API request: {e}")

    return redirect('weather')


class CitySearchCountAPIView(APIView):
    def get(self, request, city_id):
        try:
            city = City.objects.get(id=city_id)
            city_data = {
                "city_id": city_id,
                "search_count": city.search_count,
                "city_name": city.name
            }
            if request.user.is_authenticated:
                city_data["user"] = request.user.username
            return JsonResponse(city_data)
        except City.DoesNotExist:
            return JsonResponse({"error": f"City with id {city_id} does not exist"}, status=404)
