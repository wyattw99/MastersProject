from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

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
    
class TrainingGroup(models.Model):
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
    trainingGroups = models.ManyToManyField(TrainingGroup, related_name='athletes')
    stravaLogin = models.OneToOneField(StravaLogin, on_delete=models.SET_NULL, null=True, blank=True)
    
class Coach(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='coachProfile')
    coachId = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='coaches')
    
class Workout(models.Model):
    workoutId = models.AutoField(primary_key=True)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='createdWorkouts')
    athletes = models.ManyToManyField(Athlete, related_name='assignedWorkouts')
    description = models.TextField()
    title = models.CharField(max_length=30, default='Workout')
    assignedDate = models.DateField(default=timezone.now, null=False)

class Activity(models.Model):
    activityId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    activityType = models.CharField(max_length=30)
    description = models.TextField()
    movingTime = models.FloatField()
    elapsedTime = models.FloatField()
    stravaId = models.CharField(max_length=30)
    startDate = models.DateTimeField(default=timezone.now(), null=False)
    distance = models.FloatField()
    hasHeartrate = models.BooleanField(default=False)
    averageHeartrate = models.IntegerField(null=True, blank=True)
    maxHeartrate = models.IntegerField(null=True, blank=True)
    stravaManual = models.BooleanField(default=False)
    manual = models.BooleanField(default=True)
    hasGps = models.BooleanField(default=False)

    def __str__(self):
        return f"Id: {self.activityId}, Activity: {self.name}, Type: {self.activityType}, Time: {self.movingTime}, Start Date: {self.startDate}, Distance: {self.distance}"    
    
    class Meta:
        abstract = True
        
class Bike(Activity):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name="bikes")
    averageSpeed = models.FloatField()
    maxSpeed = models.FloatField()
    
    def jsonFormattedStr(self):
        return {
        'athlete': str(self.athlete.athleteId),
        'activityType': 'bike',
        'name': self.name,
        'description': self.description,
        'movingTime': str(self.movingTime),
        'elapsedTime': str(self.elapsedTime),
        'startDate': str(self.startDate),
        'distance': str(self.distance),
        'averageHeartrate': str(self.averageHeartrate),
        'maxHeartrate': str(self.maxHeartrate),
        'averageSpeed': str(self.averageSpeed),
        'maxSpeed': str(self.maxSpeed)
        }
    
class Run(Activity):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name="runs")
    averagePace = models.FloatField()
    maxPace = models.FloatField()
    averageCadence = models.FloatField()
    
    def jsonFormattedStr(self):
        return {
        'athlete': str(self.athlete.athleteId),
        'activityType': 'run',
        'name': self.name,
        'description': self.description,
        'movingTime': str(self.movingTime),
        'elapsedTime': str(self.elapsedTime),
        'startDate': str(self.startDate),
        'distance': str(self.distance),
        'averageHeartrate': str(self.averageHeartrate),
        'maxHeartrate': str(self.maxHeartrate),
        'averagePace': str(self.averagePace),
        'maxSpeed': str(self.maxPace),
        'averageCadence': str(self.averageCadence)
        }
    
class Swim(Activity):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name="swims")
    averageSpeed = models.FloatField()
    maxSpeed = models.FloatField()
    
    def jsonFormattedStr(self):
        return {
        'athlete': str(self.athlete.athleteId),
        'activityType': 'swim',
        'name': self.name,
        'description': self.description,
        'movingTime': str(self.movingTime),
        'elapsedTime': str(self.elapsedTime),
        'startDate': str(self.startDate),
        'distance': str(self.distance),
        'averageHeartrate': str(self.averageHeartrate),
        'maxHeartrate': str(self.maxHeartrate),
        'averageSpeed': str(self.averageSpeed),
        'maxSpeed': str(self.maxSpeed)
        }
    
class Other(Activity):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE, related_name="otherActivites")
    averageSpeed = models.FloatField()
    maxSpeed = models.FloatField()
    
    def jsonFormattedStr(self):
        return {
        'athlete': str(self.athlete.athleteId),
        'activityType': 'other',
        'name': self.name,
        'description': self.description,
        'movingTime': str(self.movingTime),
        'elapsedTime': str(self.elapsedTime),
        'startDate': str(self.startDate),
        'distance': str(self.distance),
        'averageHeartrate': str(self.averageHeartrate),
        'maxHeartrate': str(self.maxHeartrate),
        'averageSpeed': str(self.averageSpeed),
        'maxSpeed': str(self.maxSpeed)
        }
    

    