from django.urls import path
from . import views

app_name = 'bracket'
urlpatterns = [
    path('', views.home, name="home"),
]
