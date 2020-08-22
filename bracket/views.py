from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import *
from django.views.generic import View
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth import login, logout
from django.utils.encoding import force_text, force_bytes
from django.utils.http import urlsafe_base64_decode
from .tokens import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('bracket:index')
        else:
            return redirect('bracket:index')

# Create your views here.
class SignUpView(View):
    def get(self, request, *args, **kwargs):
        # No signing up while logged in! Same for post()
        if request.user.is_authenticated:
            return redirect('bracket:index')
        return render(request, 'signup.html', {'form': SignUpForm()})

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('bracket:index')
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()
            current_site = get_current_site(request)
            subject = 'Welcome to the Voter Registration Bracket Challenge'
            message = render_to_string('emails/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return render(request, 'confirm.html', {'host': settings.EMAIL_HOST_USER, 'email': user.email})
        return render(request, 'signup.html', {'form': form, 'signup': True})

def index(request):
    return render(request, "index.html", { "campaigns": Campaign.objects.all(), "matchups": Matchup.objects.all() })

def admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
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
                    team1.team_image = request.FILES['team' + str(i) + 'image']
                    team2.name = request.POST['team' + str(i+1)]
                    team2.team_image = request.FILES['team' + str(i+1) + 'image']
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
    return redirect('bracket:index')

def team(request, slug):
    team = get_object_or_404(Team,slug=slug)
    if len(team.team1.all()):
        matchup = team.team1.all()[0]
    else:
        matchup = team.team2.all()[0]
    campaign = matchup.campaign_set.all()[0]
    return render(request, "teampage.html", { "team": team, 'deadline': matchup.campaign_set.all()[0].deadline, 'campaign': campaign })

def view404(request, exception=None):
    return render(request, "error.html")

def register(request, slug):
    team = get_object_or_404(Team,slug=slug)
    return render(request, "register.html", { "team": team })

def matchup(request, slug):
    matchup = get_object_or_404(Matchup, slug=slug)
    return render(request, "matchup.html", {"team1": matchup.team1, "team2": matchup.team2, "deadline": matchup.campaign_set.all()[0].deadline})

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

def logoutUser(request):
    logout(request)
    return redirect('bracket:index')
