from django.urls import path
from . import views

app_name = 'bracket'
urlpatterns = [
    path('', views.index, name="index"),
    path('team/<slug:slug>', views.team, name="teams"),
    path('register/<slug:slug>', views.register, name="register"),
    path('absentee/<slug:slug>', views.absentee, name="absentee"),
    path('verifyRegistration/<slug:slug>', views.verifyRegistration, name="verifyRegistration"),
    path('matchup/<slug:slug>', views.matchup, name="matchup"),
    path('campaign/<slug:slug>', views.campaign, name="campaign"),
    path('teamslist', views.teamslist, name="teamslist"),
    path('admin', views.admin, name="admin")
]
