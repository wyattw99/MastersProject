from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    isCoach = models.BooleanField(default=False)
    isAthlete = models.BooleanField(default=False)
       
class Team(models.Model):
    teamId = models.AutoField(primary_key=True)
    teamName = models.CharField(max_length=50, null=False, blank=False)    
    
class TrainingGroups(models.Model):
    groupId = models.AutoField(primary_key=True)
    groupName = models.CharField(max_length=50, null=False, blank=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='trainingGroups')    
    
class Athlete(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='athlete_profile')
    athleteId = models.BigAutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='athletes', null=True, blank=True)
    pending = models.BooleanField(default=True)
    birthday = models.DateField(null=False, blank=False)
    schoolYear = models.CharField(max_length=20, null=False)  
    trainingGroups = models.ManyToManyField(TrainingGroups, related_name='athletes')
    
class Coach(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='coach_profile')
    coachId = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='coaches')