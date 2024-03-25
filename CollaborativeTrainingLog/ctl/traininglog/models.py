from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class StravaAPI(models.Model):
    APIid = models.AutoField(primary_key=True)
    clientId = models.CharField(max_length=100)
    clientSecret = models.CharField(max_length=100)
    
class StravaLogin(models.Model):
    loginId = models.AutoField(primary_key=True)
    stravaUserName = models.CharField(max_length=50)
    stravaID = models.CharField(max_length=50)
    stravaTokenType = models.CharField(max_length=50)
    stravaExpiration = models.IntegerField()
    stravaRefreshToken = models.CharField(max_length=50)
    stravaAccessToken = models.CharField(max_length=50)
    stravaAuthorizationCode = models.CharField(max_length=50)

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
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='athleteProfile')
    athleteId = models.BigAutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, related_name='athletes', null=True, blank=True)
    pending = models.BooleanField(default=True)
    birthday = models.DateField(null=False, blank=False)
    schoolYear = models.CharField(max_length=20, null=False)  
    trainingGroups = models.ManyToManyField(TrainingGroups, related_name='athletes')
    stravaLogin = models.OneToOneField(StravaLogin, on_delete=models.SET_NULL, null=True, blank=True)
    
class Coach(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='coachProfile')
    coachId = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='coaches')
    
class Workout(models.Model):
    workoutId = models.AutoField(primary_key=True)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='createdWorkouts')
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name='assignedWorkouts')
    description = models.TextField()

class Activity(models.Model):
    activityId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    movingTime = models.DurationField()
    elapsedTime = models.DurationField()
    stravaId = models.CharField(max_length=30)
    startDate = models.DateTimeField()
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    hasHeartrate = models.BooleanField(default=False)
    averageHeartrate = models.IntegerField(null=True, blank=True)
    maxHeartrate = models.IntegerField(null=True, blank=True)
    stravaManual = models.BooleanField(default=False)
    manual = models.BooleanField(default=False)
    hasGps = models.BooleanField(default=True)

    class Meta:
        abstract = True
        
class Bike(Activity):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name="bikes")
    averageSpeed = models.DecimalField(max_digits=5, decimal_places=2)
    maxSpeed = models.DecimalField(max_digits=5, decimal_places=2)
    
class Run(Activity):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name="runs")
    averagePace = models.DecimalField(max_digits=5, decimal_places=2)
    maxPace = models.DecimalField(max_digits=5, decimal_places=2)
    averageCadence = models.DecimalField(max_digits=3, decimal_places=2)
    
class Swim(Activity):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name="swims")
    averageSpeed = models.DecimalField(max_digits=5, decimal_places=2)
    maxSpeed = models.DecimalField(max_digits=5, decimal_places=2)
    
class Other(Activity):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name="otherActivites")
    averageSpeed = models.DecimalField(max_digits=5, decimal_places=2)
    maxSpeed = models.DecimalField(max_digits=5, decimal_places=2)
    activityType = models.CharField(max_length=50)
    

    