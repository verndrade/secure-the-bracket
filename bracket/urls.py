from django.urls import path
from . import views

app_name = 'bracket'
urlpatterns = [
    path('', views.index, name="index"),
    path('team/<slug:slug>', views.team, name="teams"),
    path('matchup/<slug:slug>', views.matchup, name="matchup"),
    path('campaign/<slug:slug>', views.campaign, name="campaign"),
    path('teamslist', views.teamslist, name="teamslist"),
    path('admin', views.admin, name="admin")
]
