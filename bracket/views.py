from django.shortcuts import render, get_object_or_404
from .models import *
from .forms import *

# Create your views here.
def home(request):
    return render(request, "home.html", {'matchups': Matchup.objects.all(), 'campaigns': Campaign.objects.all()})

def panel(request):
    if request.method == 'POST':
        if "submit_matchup" in request.POST:
            form = DropDownMenuTeams(request.POST)
            if form.is_valid():
                form.save()
        elif "submit_team" in request.POST:
            team = Team()
            team.name = request.POST['name']
            team.vote_count = request.POST['votes']
            team.save()

    return render(request, "admin.html", {'teams': Team.objects.all(), 'matchups': Matchup.objects.all(), 'campaigns': Campaign.objects.all(), 'form': DropDownMenuTeams()})

def team(request, name):
    team = get_object_or_404(Team,name=name)
    return render(request, "teampage.html", { "team": team, 'matchups': Matchup.objects.all(), 'campaigns': Campaign.objects.all(), })

def view404(request, exception=None):
    return render(request, "error.html")


def matchup(request, id):
    match = get_object_or_404(Matchup, id=id)
    return render(request, "matchup.html", {"id": id, "team1": match.team1, "team2": match.team2, 'matchups': Matchup.objects.all(), 'campaigns': Campaign.objects.all(), "deadline": match.deadline})

def campaign(request, id):
    campaign = get_object_or_404(Campaign, id=id)
    
    votecount = 0
    for team in campaign.teams.all():
        votecount += team.vote_count

    if votecount > 100:
        votecount = 100
        
    return render(request, "campaign.html", {"id": id, "teams": campaign.teams.all(), "info": campaign.info, "name": campaign.name, 'deadline': campaign.deadline, 'matchups': Matchup.objects.all(), 'campaigns': Campaign.objects.all(), 'votecountPercent': votecount, 'votecount': votecount})

def teamslist(request):
    teams = Team.objects.all()
    return render(request, "teamslist.html", {"teams": teams, 'matchups': Matchup.objects.all(), 'campaigns': Campaign.objects.all(),})
