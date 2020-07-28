from django import forms
from .models import *

class DropDownMenuTeams(forms.Form):
    team1 = forms.ModelChoiceField(queryset = Team.objects.all())
    team2 = forms.ModelChoiceField(queryset = Team.objects.all())