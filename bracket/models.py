from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from django.utils.text import slugify

class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    vote_count = models.IntegerField(default=0)
    team_image = models.ImageField(upload_to='bracket/static/uploads', blank=True, null=True, default = 'bracket/static/default-team-img.jpg')
    slug = models.SlugField(unique=True, default="")
    def clean(self):
        if self.vote_count < 0:
            raise ValidationError('Vote count should not be negative.')
    def __str__(self):
        return self.name 
    def save(self, *args, **kwargs): 
        self.slug = slugify(self.name) 
        super(Team, self).save(*args, **kwargs) 

class Matchup(models.Model):
    team1 = models.ForeignKey("Team", related_name = 'team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey("Team", related_name = 'team2', on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, default="")
    def getWinner(self):
        return self.team1 if self.team1.vote_count > self.team2.vote_count else self.team2
    def clean(self):
        if self.team1 == self.team2:
            raise ValidationError('Teams should be different.')
    def __str__(self):
        return self.team1.name + ' vs. ' + self.team2.name 
    def save(self, *args, **kwargs): 
        self.slug = slugify(self) 
        super(Matchup, self).save(*args, **kwargs) 


class Campaign(models.Model):
    name = models.TextField(max_length=200, unique=True)
    matchups = models.ManyToManyField(Matchup)
    info = models.TextField(max_length=500)
    deadline = models.DateTimeField(default=datetime(2020, 11, 3, 1))
    slug = models.SlugField(unique=True, default="")
    goal = models.IntegerField(default=100)
    def __str__(self):
        return self.name 
    def clean(self):
        if self.goal < 1:
            raise ValidationError('Goal should be positive.')
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)  
        super(Campaign, self).save(*args, **kwargs) 