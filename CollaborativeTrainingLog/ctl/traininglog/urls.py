# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 11:20:51 2024

@author: wwolf
"""

from django.urls import path
from . import views

app_name='traininglog'


urlpatterns = [
    path("login",views.loginRequest, name="login"),
    
    #urls for users
    path("newUser",views.createUser, name="newUser"),
    path("getUser/<int:userID>/", views.getUser, name="getUser"),
    path("updateUser/<int:userID>/",views.updateUser, name="updateUser"),
    path("deleteUser/<int:userID>/",views.deleteUser, name = "deleteUser"),
    
    #urls for athletes
    path("newAthlete",views.createAthlete, name="newAthlete"),
    path("getAthlete/<int:athleteID>/",views.getAthlete, name="getAthlete"),
    path("updateAthlete/<int:athleteID>/",views.updateAthlete, name="updateAthlete"),
    path("deleteAthlete/<int:athleteID>/", views.deleteAthlete, name="deleteAthlete"),
    
    #urls for coaches
    path("newCoach",views.createCoach,name="newCoach"),
    path("getCoach/<int:coachID>/",views.getCoach, name="getCoach"),
    path("deleteCoach/<int:coachID>/",views.deleteCoach, name="deleteCoach"),
    
    #urls for workouts
    path("newWorkout", views.createWorkout, name="newWorkout"),
    path("assignToAthletes", views.assignToAthletes, name="assignToAthletes"),
    path("getWorkout/<int:workoutID>/", views.getWorkout, name="getWorkout"),
    path("removeAthlete/<int:workoutID>/", views.removeAthleteFromWorkout, name="removeAthlete"),
    path("editWorkout/<int:workoutID>/", views.editWorkout, name="editWorkout"),
    path("copyWorkout/<int:workoutID>/", views.copyWorkout, name="copyWorkout"),
    path("deleteWorkout/<int:workoutID>/",views.deleteWorkout, name="deleteWorkout"),
    
    #urls for training groups
    path("newTrainingGroup",views.createTrainingGroup, name="newGroup"),
    path("getTrainingGroup/<int:groupID>/",views.getTrainingGroup, name="getGroup"),
    path("deleteTrainingGroup/<int:groupID>/", views.deleteAthlete, name="deleteGroup"),
    path("addAthleteToGroup/<int:athleteID>/", views.addAthleteToGroup, name="addToGroup"),
    path("removeAthleteFromGroup/<int:athleteID>/", views.removeAthleteFromGroup, name="removeFromGroup"),
    
    #urls for strava
    
    #urls for activities
    path("newActivity",views.createActivity, name="newActivity"),
    path("getAthleteActivities/<int:athleteID>/",views.getAthleteActivities, name="getAthleteActivities"),
    path("getActivity/<int:activityID>/", views.getActivity, name="getActivity"),
    path("deleteActivity/<int:activityID>/",views.deleteActivity, name="deleteActivity"),
    path("editActivity/<int:activityID>/",views.updateActivity, name="updateActivity"),
    
    #urls for comments
    path("createComment",views.createComment, name="createComment"),
    path("deleteComment/<int:commentID>/", views.deleteComment, name="deleteComment"),
    path("getComments/<int:activityID/", views.getComments, name="getComments"),
    
    #urls for getting stats
    path("getAthleteStats/<int:athleteID>/", views.getAthleteStats, name="getAthleteStats"),
    
    #urls for rosters
    path("addToTeam/<int:athleteID>/",views.addAthleteToTeam, name="addToTeam"),
    path("approveAthlete/<int:athleteID>/", views.approveAthlete, name="approveAthlete"),
    path("removeFromTeam/<int:athleteID>/", views.removeAthleteFromTeam, name="removeAthlete"),
    path("viewRoster/<int:teamID>/", views.viewRoster, name="viewRoster"),
    
    #urls for teams
    path("newTeam",views.createTeam, name="newTeam"),
    path("getTeam/<str:teamName>/", views.getTeam, name="getTeam"),
    path("deleteTeam/<int:teamID>/",views.deleteTeam, name="deleteTeam"),
]