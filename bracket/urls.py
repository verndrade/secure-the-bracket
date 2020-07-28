from django.urls import path
from . import views

app_name = 'bracket'
urlpatterns = [
    path('', views.home, name="home"),
    path('panel', views.panel, name="panel"),
    path('team/<slug:name>', views.team, name="teams"),
]
