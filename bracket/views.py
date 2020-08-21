from django.shortcuts import render, get_object_or_404, redirect
from .models import *

# Create your views here.
def index(request):
    return render(request, "index.html", { "campaigns": Campaign.objects.all(), "matchups": Matchup.objects.all() })

def admin(request):
    if request.method == 'POST':
        campaign = Campaign()
        campaign.name = request.POST['name']
        campaign.info = request.POST['info']
        campaign.goal = request.POST['goal']
        campaign.deadline = request.POST['deadline']
        try:
            campaign.save()
            for i in range(1,9,2):
                matchup = Matchup()
                team1 = Team()
                team2 = Team()
                team1.name = request.POST['team' + str(i)]
                team2.name = request.POST['team' + str(i+1)]
                team1.save()
                team2.save()
                matchup.team1 = team1
                matchup.team2 = team2
                matchup.save()
                campaign.matchups.add(matchup)
        except Exception as e:
            try:
                for i in campaign.matchups.all():
                    i.team1.delete()
                    i.team2.delete()
                    i.delete()
                campaign.delete()
                team1.delete()
            except:
                pass
            return render(request, "admin.html", {'fail':e})

    return render(request, "admin.html")

def team(request, slug):
    team = get_object_or_404(Team,slug=slug)
    if len(team.team1.all()):
        matchup = team.team1.all()[0]
    else:
        matchup = team.team2.all()[0]
    campaign = matchup.campaign_set.all()[0]
    return render(request, "teampage.html", { "team": team, 'deadline': matchup.deadline, 'campaign': campaign })

def view404(request, exception=None):
    return render(request, "error.html")

def register(request, slug):
    team = get_object_or_404(Team,slug=slug)
    return render(request, "register.html", { "team": team })

def matchup(request, slug):
    match = get_object_or_404(Matchup, slug=slug)
    return render(request, "matchup.html", {"team1": match.team1, "team2": match.team2, "deadline": match.campaign_set.all()[0].deadline})

def campaign(request, slug):
    campaign = get_object_or_404(Campaign, slug=slug)
    
    votecount = 0
    for matchup in campaign.matchups.all():
        votecount += matchup.team1.vote_count + matchup.team2.vote_count

    votecountPercent = votecount / campaign.goal * 100
    if votecountPercent > 100:
        votecountPercent = 100
        
    return render(request, "campaign.html", {'campaign': campaign, 'votecountPercent': votecountPercent, 'votecount': votecount})

def teamslist(request):
    teams = Team.objects.all()
    return render(request, "teamslist.html", {"teams": teams, 'matchups': Matchup.objects.all(), 'campaigns': Campaign.objects.all()})
