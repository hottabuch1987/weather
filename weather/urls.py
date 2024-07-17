# weather/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_weather, name='weather'),
    path('add', views.add_city, name='add_city'),
 
    path('city-search/<int:city_id>/', views.CitySearchCountAPIView.as_view(), name='city_search'),
]
