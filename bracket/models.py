from django.db import models
from django.core.exceptions import ValidationError

class Team(models.Model):
    name = models.CharField(max_length=200, unique=True)
    vote_count = models.IntegerField()

    def clean(self):
        if self.vote_count < 0:
            raise ValidationError('Vote count should not be negative.')
    def __str__(self):
        return self.name 

class Matchup(models.Model):
    team1 = models.ForeignKey("Team", related_name = 'team1', on_delete=models.CASCADE)
    team2 = models.ForeignKey("Team", related_name = 'team2', on_delete=models.CASCADE)
    def getWinner(self):
        return team1 if team1.vote_count > team2.vote_count else team2
    def clean(self):
        if self.team1 == self.team2:
            raise ValidationError('Teams should be different.')