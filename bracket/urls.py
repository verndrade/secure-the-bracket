from django.urls import path
from . import views

app_name = 'bracket'
urlpatterns = [
    path('', views.home, name="home"),
    path('panel', views.panel, name="panel"),
    path('team/<slug:name>', views.team, name="teams"),
    path('matchup/<slug:id>', views.matchup, name="matchup"),
    path('campaign/<slug:id>', views.campaign, name="campaign"),
    path('teamslist', views.teamslist, name="teamslist")
]
