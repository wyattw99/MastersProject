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
]