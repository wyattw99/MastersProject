# -*- coding: utf-8 -*-
"""
Created on Mon May  6 16:37:48 2024

@author: wwolf
"""
from traininglog.models import User, Athlete, Coach, Team, Workout, TrainingGroup, Activity, Run, Bike, Swim, Other, Comment, StravaLogin, StravaAPI
import requests
import time

def stravaIdExists(stravaId, activityType, athlete):
    idFound = False
    if activityType == 'run':
        activities = athlete.runs.all()
    elif activityType == 'bike':
        activities = athlete.bikes.all()
    elif activityType == 'swim':
        activities = athlete.bikes.all()
    else:
        activities = athlete.otherActivites.all()
    for activity in activities:
        if activity.stravaId == str(stravaId):
            idFound = True
            break
    return idFound

def createStravaActivity(athlete, activityType, name, distance, movingTime, elapsedTime, startDate, hasHeartrate, avgHeartrate, maxHeartrate, manual, stravaManual, hasGps, avgSpeed, maxSpeed, avgCadence, stravaId):
    if activityType == 'run':
        try:
            newActivity = Run.objects.create(name=name, athlete=athlete, activityType=activityType, movingTime=movingTime, elapsedTime=elapsedTime, 
                                             distance=distance, hasHeartrate=hasHeartrate, averageHeartrate=avgHeartrate, 
                                             maxHeartrate=maxHeartrate, manual=manual, hasGps=hasGps,
                                             averagePace=avgSpeed, maxPace=maxSpeed, averageCadence=avgCadence, startDate=startDate, stravaId=stravaId)
            newActivity.save()
            return newActivity.activityId
        except Exception as e:
            return str(e)
    elif activityType == 'bike':
        try: 
            newActivity = Bike.objects.create(name=name, athlete=athlete, activityType=activityType, movingTime=movingTime, elapsedTime=elapsedTime, 
                                             distance=distance, hasHeartrate=hasHeartrate, averageHeartrate=avgHeartrate, 
                                             maxHeartrate=maxHeartrate, manual=manual, hasGps=hasGps,
                                             averagePace=avgSpeed, maxPace=maxSpeed, startDate=startDate, stravaId=stravaId)
            newActivity.save()
            return newActivity.activityId
        except Exception as e:
            return str(e)
    elif activityType == 'swim':
         try: 
             newActivity = Swim.objects.create(name=name, athlete=athlete, activityType=activityType, movingTime=movingTime, elapsedTime=elapsedTime, 
                                              distance=distance, hasHeartrate=hasHeartrate, averageHeartrate=avgHeartrate, 
                                              maxHeartrate=maxHeartrate, manual=manual, hasGps=hasGps,
                                              averagePace=avgSpeed, maxPace=maxSpeed, startDate=startDate,stravaId=stravaId)
             newActivity.save()
             return newActivity.activityId
         except Exception as e:
             return str(e)
    else:
         try: 
             newActivity = Other.objects.create(name=name, athlete=athlete, activityType=activityType, movingTime=movingTime, elapsedTime=elapsedTime, 
                                              distance=distance, hasHeartrate=hasHeartrate, averageHeartrate=avgHeartrate, 
                                              maxHeartrate=maxHeartrate, manual=manual, hasGps=hasGps,
                                              averagePace=avgSpeed, maxPace=maxSpeed, startDate=startDate,stravaId=stravaId)
             newActivity.save()
             return newActivity.activityId
         except Exception as e:
             return str(e)
         
def tokenRefresh(login, apiConnection):
    url = "https://www.strava.com/api/v3/oauth/token"
    payload = {
        "client_id": apiConnection.clientId,
        "client_secret": apiConnection.clientSecret,
        "grant_type": "refresh_token",
        "refresh_token": login.stravaRefreshToken
        }
    refreshResponse = requests.post(url, data=payload)
    refreshData = refreshResponse.json()
    login.stravaTokenType = refreshData['token_type']
    login.stravaExpiration = refreshData['expires_at']
    login.stravaRefreshToken = refreshData['refresh_token']
    login.stravaAccessToken = refreshData['access_token']
    login.save()
    
def tokenExpired(login):
    expiration = login.stravaExpiration
    currentTime = time.time()
    if currentTime > expiration:
        return True
    else:
        return False
    
def exchangeAuthorizationToken(athlete, stravaConnection, authorizationCode, authorizationScope):
    clientId = str(stravaConnection.clientId)
    clientSecret = str(stravaConnection.clientSecret)
    
    tokenUrl = 'https://www.strava.com/oauth/token'
    payload = {
        'client_id': clientId,
        'client_secret': clientSecret,
        'code': authorizationCode,
        'grant_type': 'authorization_code'
    }
    tokenData = {}
    if athlete.stravaLogin is None:
        try:
            response = requests.post(tokenUrl, data=payload)
            tokenData = response.json()
            athleteData = tokenData['athlete']
            stravaID = athleteData['id']
            stravaUserName = athleteData['username']
            stravaTokenType = tokenData['token_type']
            stravaExpiration = tokenData['expires_at']
            stravaRefreshToken = tokenData['refresh_token']
            stravaAccessToken = tokenData['access_token']
            newStravaLogin = StravaLogin.objects.create(stravaUserName=stravaUserName, stravaID=stravaID, stravaTokenType=stravaTokenType, 
                                                        stravaExpiration=stravaExpiration, stravaRefreshToken=stravaRefreshToken, 
                                                        stravaAccessToken=stravaAccessToken, stravaAuthorizationCode=authorizationCode, stravaAuthorizationScope=authorizationScope)
            newStravaLogin.save()
            athlete.stravaLogin = newStravaLogin
            athlete.save()
            return True, "Account Linked, please close this page"
        except Exception as e:
            return False, str(e)
    else:
        try:
            stravaLogin = athlete.stravaLogin
            response = requests.post(tokenUrl, data=payload)
            tokenData = response.json()
            stravaLogin.stravaTokenType = tokenData['token_type']
            stravaLogin.stravaExpiration = tokenData['expires_at']
            stravaLogin.stravaRefreshToken = tokenData['refresh_token']
            stravaLogin.stravaAccessToken = tokenData['access_token']
            stravaLogin.stravaAuthorizationCode = authorizationCode
            stravaLogin.stravaAuthorizationScope = authorizationScope
            stravaLogin.save()
            return True, "Account Linked, please close this page"
        except Exception as e:
            return False, str(e)
    