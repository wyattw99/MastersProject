from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User, Athlete, Coach, Team, Workout, TrainingGroup, Run, Bike, Swim, Other, Comment, StravaAPI
from django.db.models import Q
from django.utils import timezone
import requests
from datetime import datetime
import time
from .utils.stravaUtils import stravaIdExists, createStravaActivity, tokenRefresh, tokenExpired, exchangeAuthorizationToken
from django.conf import settings


# Create your views here.
@csrf_exempt
def getCookies(request):
    cookies = request.COOKIES
    print(cookies)
    return JsonResponse({'cookies': cookies})

@csrf_exempt
def loginRequest(request):
    if request.method == 'POST':
        username = request.GET.get('username')
        password = request.GET.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.isAthlete is True and user.isCoach is True:
                response = JsonResponse({'message': 'Login successful', 'userId': user.id, 'athleteId': user.athleteProfile.athleteId, 'coachId': user.coachProfile.coachId})
            elif user.isAthlete is True:
                response = JsonResponse({'message': 'Login successful', 'userId': user.id, 'athleteId': user.athleteProfile.athleteId})
            elif user.isCoach is True:
                response = JsonResponse({'message': 'Login successful', 'userId': user.id, 'coachId': user.coachProfile.coachId})
            else:
                response = JsonResponse({'message': 'Login successful', 'userId': user.id, 'login message': 'admin login'})
            
            return response
          
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
def logoutRequest(request):
    if request.method == 'POST':
        try:
            logout(request)
            response = JsonResponse({'message': 'Logout successful'})
            response.delete_cookie('csrftoken')
            return response
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
    
# @csrf_exempt
# def logoutRequest(request):
#     if request.method == 'POST':
#         try:
#             logout(request)
#             return JsonResponse({'message': 'Logout successful'})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
    
  

      
#calls for user
@csrf_exempt
def createUser(request):
    if request.method == 'POST':
        username = request.GET.get('username')
        password = request.GET.get('password')
        first_name = request.GET.get('first_name')
        last_name = request.GET.get('last_name')
        email = request.GET.get('email')
        isCoach = request.GET.get('isCoach')
        isAthlete = request.GET.get('isAthlete')
        
        try:
            newUser = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
            newUser.isCoach = isCoach
            newUser.isAthlete = isAthlete
            newUser.save()
            return JsonResponse({'message': 'User created successfully', 'userId': newUser.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
@login_required
def getUser(request, userID):
    if request.method == 'GET':
        try:
            user = User.objects.get(id=userID)
            userData = {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'isCoach': user.isCoach,
                    'isAthlete': user.isAthlete,
                }
            try:
                if user.isCoach:
                    return JsonResponse({'userData': userData, 'coachId': user.coachProfile.coachId, 'teamId': user.coachProfile.team})
                elif user.isAthlete:
                    return JsonResponse({'userData': userData, 'athleteId': user.athleteProfile.athleteId, 'teamId': user.athleteProfile.team})
                else:
                    return JsonResponse(userData)
            except Exception as e:
                return JsonResponse(userData)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
    
@login_required
def updateUser(request, userID):
    if request.method == 'POST' or request.method == 'PUT':
        try:
            user = User.objects.get(id=userID)
            user.email = request.GET.get('email', user.email)
            user.first_name = request.GET.get('first_name', user.first_name)
            user.last_name = request.GET.get('last_name', user.last_name)
            user.save()
            return JsonResponse({'message': 'User updated successfully', 'userId': user.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST or PUT requests are allowed'}, status=405)

@login_required
def deleteUser(request, userID):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=userID)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'})
        except Exception as e:
           return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only DELETE requests are allowed'}, status=405)




     
#calls for athlete  
@csrf_exempt
def createAthlete(request):
    if request.method == 'POST':
        birthday = request.GET.get('birthday')
        schoolYear = request.GET.get('schoolYear')
        userID = request.GET.get('userID')
        user = User.objects.get(id=userID)
        try:
            newAthlete = Athlete.objects.create(user=user, birthday=birthday, schoolYear=schoolYear)
            newAthlete.save()
            return JsonResponse({'message': 'Athlete created successfully', 'athleteId': newAthlete.athleteId})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@login_required
def getAthlete(request, athleteID):
    if request.method == 'GET':
        try:
            athlete = Athlete.objects.get(athleteId=athleteID)
            if athlete.team is None:
                athleteData = {
                        'id': athlete.athleteId,
                        'birthday': athlete.birthday,
                        'schoolYear': athlete.schoolYear,
                        'teamID': athlete.team,
                        'userID': athlete.user.id
                    }
            else:
                athleteData = {
                        'id': athlete.athleteId,
                        'birthday': athlete.birthday,
                        'schoolYear': athlete.schoolYear,
                        'teamID': athlete.team.teamId,
                        'userID': athlete.user.id
                    }
            return JsonResponse(athleteData)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Athlete does not exist'}, status=405)
    
@login_required
def updateAthlete(request, athleteID):
    if request.method == 'POST' or request.method == 'PUT':
        try:
            athlete = Athlete.objects.get(athleteId = athleteID)
            athlete.birthday = request.GET.get('birthday', athlete.birthday)
            athlete.schoolYear = request.GET.get('schoolYear',athlete.schoolYear)
            athlete.save()
            return JsonResponse({'message': 'Athlete updated successfully', 'athleteId': athlete.athleteId})
        except Exception as e:
           return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST or PUT requests are allowed'}, status=405)
    
@login_required
def deleteAthlete(request, athleteID):
    if request.method == 'DELETE':
        try:
            athlete = Athlete.objects.get(athleteId=athleteID)
            athlete.delete()
            return JsonResponse({'message': 'Athlete deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only DELETE requests are allowed'}, status=405)
        




#calls for coach
@csrf_exempt
def createCoach(request):
    if request.method == 'POST':
        userId = request.GET.get('userId')
        user = User.objects.get(id=userId)
        teamId = request.GET.get('teamId')
        team = Team.objects.get(teamId=teamId)
        try:
            newCoach = Coach.objects.create(user=user, team=team)
            newCoach.save()
            return JsonResponse({'message': 'Coach created successfully', 'coachId': newCoach.coachId})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message', 'Only POST requests are allowed'}, status=405)

@login_required
def getCoach(request, coachID):
    if request.method == 'GET':
        try:
            coach = Coach.objects.get(coachId=coachID)
            user = coach.user
            userID = user.id
            team = coach.team
            teamID = team.teamId
            coachData = {
                    'id': coach.coachId,
                    'teamID': teamID,
                    'userID': userID,
                }
            return JsonResponse(coachData)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
    
@login_required
def deleteCoach(request, coachID):
    if request.method == 'DELETE':
        try:
            coach = Coach.objects.get(coachId=coachID)
            coach.delete()
            return JsonResponse({'message': 'Coach deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only DELETE requests are allowed'}, status=405)




    
#calls for workouts
@login_required
def createWorkout(request):
    if request.method == 'POST':
        coachID = request.GET.get("coachID")
        description = request.GET.get("description")
        assignedDate = request.GET.get("date")
        title = request.GET.get("title")
        try:
            newWorkout = Workout.objects.create(coach=Coach.objects.get(coachId=coachID), title=title, assignedDate=assignedDate, description=description)
            newWorkout.save()
            return JsonResponse({'message': 'Workout created successfully',
                                 'workoutID': newWorkout.workoutId})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message', 'Only POST requests are allowed'}, status=405)
    
@login_required
def assignToAthletes(request):
    if request.method == 'PUT':
        workout = Workout.objects.get(workoutId = request.GET.get("workoutID"))
        numAthletes = int(request.GET.get("numAthletes"))
        try:
            if numAthletes > 1:
                athleteIDs = request.GET.get("athleteIDs").split(",")   
                athletes = Athlete.objects.filter(pk__in=athleteIDs)
                for athlete in athletes:
                    workout.athletes.add(athlete)
                workout.save()
                return JsonResponse({'message': 'Athletes Assigned to Workout'})     
            else:
                athleteIDs = request.GET.get("athleteIDs")
                athletes = Athlete.objects.get(athleteId=athleteIDs)
                workout.athletes.add(athletes)
                workout.save()
                return JsonResponse({'message': 'Athletes Assigned to Workout'})
        except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message', 'Only Put requests are allowed'}, status=405)

@login_required
def getWorkout(request, workoutID):
    if request.method == 'GET':
        try:
            workout = Workout.objects.get(workoutId=workoutID)
            assignedAthletes = workout.athletes.all()
            assignedAthletes = [{
                'athleteID' : athlete.athleteId,
                'firstName': athlete.user.first_name,
                'lastName': athlete.user.last_name
            } for athlete in assignedAthletes]
            
            data = {
                'workoutID': workout.workoutId,
                'title': workout.title,
                'description': workout.description,
                'assignedDate': workout.assignedDate,
                'coachID': workout.coach.coachId,
                'assignedAthletes': assignedAthletes
            }
            
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
    
@login_required
def removeAthleteFromWorkout(request, workoutID):
    if request.method == 'PUT':
        workout = Workout.objects.get(workoutId=workoutID)
        athlete = Athlete.objects.get(athleteId=request.GET.get("athleteID"))
        try:
            workout.athletes.remove(athlete)
            workout.save()
            return JsonResponse({'message': 'Athlete Removed from Workout'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        else:
            return JsonResponse({'message', 'Only PUT requests are allowed'}, status=405)
        
@login_required
def editWorkout(request, workoutID):
    if request.method == 'PUT' or request.method == 'POST':
        try:
            workout = Workout.objects.get(workoutId = workoutID)
            workout.title = request.GET.get('title', workout.title)
            workout.description = request.GET.get('description', workout.description)
            workout.assignedDate = request.GET.get('assignedDate', workout.assignedDate)
            return JsonResponse({'message': 'Workout updated successfully',
                                 'workoutID': workout.workoutId})
        except Exception as e:
           return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST or PUT requests are allowed'}, status=405)
    
@login_required
def copyWorkout(request, workoutID):
    if request.method == 'POST':
        workout = Workout.objects.get(workoutId = workoutID)
        newDate = request.GET.get("newDate")
        newTitle = request.GET.get("newTitle")
        try:
            newWorkout = Workout.objects.create(coach=workout.coach,title = newTitle, description=workout.description, assignedDate=newDate)
            newWorkout.save()
            return JsonResponse({'message': 'Workout copied successfully',
                                 'workoutID': newWorkout.workoutId})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message', 'Only POST requests are allowed'}, status=405)
    
@login_required
def deleteWorkout(request, workoutID):
    if request.method == 'DELETE':
        try:
            workout = Workout.objects.get(workoutId=workoutID)
            workout.delete()
            return JsonResponse({'message': 'Workout deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
       return JsonResponse({'message': 'Only DELETE requests are allowed'}, status=405) 
   
@login_required
def getAthleteWorkouts(request,athleteID):
    if request.method == 'GET':
        athlete = Athlete.objects.get(athleteId=athleteID)
        
        rangeStart = request.GET.get("rangeStart")
        rangeEnd = request.GET.get("rangeEnd")
        workoutData= {}
        
        try:
            dateFilter = Q(assignedDate__range=(rangeStart, rangeEnd))|Q(assignedDate=rangeEnd)
            workouts = athlete.assignedWorkouts.filter(dateFilter).order_by('assignedDate')
            workoutData = [{
                'workoutID': workout.workoutId,
                'title': workout.title,
                'description': workout.description,
                'assignedDate': workout.assignedDate,
                'coachID': workout.coach.coachId 
                } for workout in workouts]
            assignedWorkouts = {
                'assignedWorkouts': workoutData
            }
            return JsonResponse(assignedWorkouts)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
        
@login_required
def getCoachWorkouts(request,coachID):
    if request.method == 'GET':
        coach = Coach.objects.get(coachId=coachID)
        
        rangeStart = request.GET.get("rangeStart")
        rangeEnd = request.GET.get("rangeEnd")
        workoutData= {}
        
        try:
            dateFilter = Q(assignedDate__range=(rangeStart, rangeEnd))
            workouts = coach.createdWorkouts.filter(dateFilter).order_by('assignedDate')
            workoutData = [{
                'workoutID': workout.workoutId,
                'title': workout.title,
                'description': workout.description,
                'assignedDate': workout.assignedDate,
                'coachID': workout.coach.coachId,
                'assignedAthletes': [{
                    'athleteID' : athlete.athleteId,
                    'firstName': athlete.user.first_name,
                    'lastName': athlete.user.last_name
                } for athlete in workout.athletes.all()]
            } for workout in workouts]
            assignedWorkouts = {
                'assignedWorkouts': workoutData
            }
            return JsonResponse(assignedWorkouts)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)    
  



  
#calls for training groups
@login_required
def createTrainingGroup(request):
    if request.method == 'POST':
        groupName = request.GET.get('groupName')
        team = Team.objects.get(teamId=request.GET.get('teamID'))
        try:
            newGroup = TrainingGroup.objects.create(groupName=groupName,team=team)
            newGroup.save()
            return JsonResponse({'message': 'Group created successfully', 'groupId': newGroup.groupId})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
    
@login_required
def getTrainingGroup(request, groupID):
    if request.method == 'GET':
        group = TrainingGroup.objects.get(groupId=groupID)
        try:
            athletes = group.athletes.all()
            athleteData = [{
                    'firstName': athlete.user.first_name,
                    'lastName': athlete.user.last_name,
                    'athleteID': athlete.athleteId
                } for athlete in athletes]
            groupData = {
                    'groupId': group.groupId,
                    'groupName': group.groupName,
                    'athletes': athleteData
                }
        except Exception as e:
            print(e)
            groupData = {
                    'groupId': group.groupId,
                    'groupName': group.groupName,
                    'athletes': ''
                }
        return JsonResponse(groupData)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
    
@login_required
def deleteTrainingGroup(request, groupID):
    if request.method == 'DELETE':
        try:
            group = TrainingGroup.objects.get(groupId=groupID)
            group.delete()
            return JsonResponse({'message': 'Group deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only DELETE requests are allowed'}, status=405)
    
@login_required
def addAthleteToGroup(request, athleteID):
    if request.method == 'POST' or request.method == 'PUT':
        try:
            athlete = Athlete.objects.get(athleteId = athleteID)
            group = TrainingGroup.objects.get(groupId=request.GET.get('groupID'))
            athlete.trainingGroups.add(group)
            athlete.save()
            return JsonResponse({'message': 'Athlete added to group successfully'})
        except Exception as e:
           return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST or PUT requests are allowed'}, status=405)

@login_required
def removeAthleteFromGroup(request, athleteID):
    if request.method == 'POST' or request.method == 'PUT':
        try:
            athlete = Athlete.objects.get(athleteId = athleteID)
            athlete.trainingGroups.remove(request.GET.get("groupID"))
            athlete.save()
            return JsonResponse({'message': 'Athlete removed from team successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST or PUT requests are allowed'}, status=405)

@login_required
def getTeamsGroups(request, teamID):
    if request.method == 'GET':
        try:
            team = Team.objects.get(teamId=teamID)
            groups = team.trainingGroups.all()
            groupsJson = []
            for group in groups:
               groupData = {
                   'groupName': group.groupName,
                   'groupId': group.groupId
                   }
               groupsJson.append(groupData)
            return JsonResponse({'groups': groupsJson})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)



#calls for strava
stravaConnection = StravaAPI.objects.get(APIid=settings.STRAVA_API_CONNECTION_ID)
#stravaConnection = StravaAPI.objects.create(clientId='0000', clientSecret='xxxxxxxxxxxxxxxxxxxxxx') #used to run tests, will not connect to strava
@login_required
def getAccessToken(request):
    athlete = Athlete.objects.get(athleteId=request.GET.get('athleteID'))
    scopes = 'activity:read_all'
    clientId = str(stravaConnection.clientId)
    redirectURI = f'http://127.0.0.1:8000/external/{athlete.athleteId}/exchangeToken'
    stravaAuthURL = f'http://www.strava.com/oauth/authorize?client_id={clientId}&response_type=code&redirect_uri={redirectURI}&approval_prompt=force&scope={scopes}'
    return JsonResponse({'redirectURL': stravaAuthURL})

@login_required
def getStravaActivities(request):
    activitiesData = {}
    try:
        athlete = Athlete.objects.get(athleteId=request.GET.get("athleteID"))
        stravaLogin = athlete.stravaLogin
        if tokenExpired(stravaLogin):
            tokenRefresh(stravaLogin, stravaConnection)
        rangeStart = datetime.strptime(request.GET.get('rangeStart'),"%Y-%m-%d")
        rangeEnd = datetime.strptime(request.GET.get('rangeEnd'),"%Y-%m-%d")
        epochStart = time.mktime(rangeStart.timetuple())
        epochEnd = time.mktime(rangeEnd.timetuple())
        activitiesUrl = f'https://www.strava.com/api/v3/athlete/activities?before={epochEnd}&after={epochStart}&page=1&per_page=56"'
        stravaAccessToken = stravaLogin.stravaAccessToken
        headers = {'Authorization': f'Bearer {stravaAccessToken}'}
        activitiesResponse = requests.get(activitiesUrl, headers=headers)
        activitiesData = activitiesResponse.json()
        databaseActivities = []
        for activity in activitiesData:
            preExistingActivity = False
            stravaId = activity['id']
            activityType = activity['type'].lower()
            preExistingActivity = stravaIdExists(stravaId, activityType, athlete)
            if preExistingActivity:
                continue
            else:
                name = activity['name']
                distance = activity['distance']
                movingTime = activity['moving_time']
                elapsedTime = activity['elapsed_time']
                startDate = activity['start_date_local']
                hasHeartrate = activity['has_heartrate']
                if hasHeartrate == True:
                    avgHeartrate = activity['average_heartrate']
                    maxHeartrate = activity['max_heartrate']
                else:
                    avgHeartrate = 0.0
                    maxHeartrate = 0.0
                manual = activity['manual']
                if manual == True:
                    stravaManual = True
                    hasGps = False
                    if activityType == 'run':
                        avgCadence = 0
                else:
                    stravaManual = False
                    hasGps = True
                    if activityType == 'run':
                        avgCadence = activity['average_cadence']
                avgSpeed = activity['average_speed']
                maxSpeed = activity['max_speed']
                activityId = createStravaActivity(athlete, activityType, name, distance, movingTime, elapsedTime, startDate, hasHeartrate, avgHeartrate, maxHeartrate, manual, stravaManual, hasGps, avgSpeed, maxSpeed, avgCadence, stravaId)
                activityData = {'name': name, 'activityId': activityId}
                databaseActivities.append(activityData)
        return JsonResponse({'message': 'Strava activities added to database', 'databaseActivities': databaseActivities})
    except Exception as e:
        return JsonResponse({'error': str(e), 'stravaResponse': activitiesData}, status=500)
    
@login_required
def revokeStravaAccess(request):
    revokeData = {}
    try:
        athlete = Athlete.objects.get(athleteId=request.GET.get('athleteID'))
        stravaLogin = athlete.stravaLogin
        tokenRefresh(stravaLogin, stravaConnection)
        stravaAccessToken = stravaLogin.stravaAccessToken
        revokeUrl = 'https://www.strava.com/oauth/deauthorize'
        params = {"access_token": stravaAccessToken}
        revokeReponse = requests.post(revokeUrl, params=params)
        revokeData = revokeReponse.json()
        stravaLogin.delete()
        return JsonResponse(revokeData)
    except Exception as e:
        return JsonResponse({'error': str(e), 'stravaResponse': revokeData}, status=500)
    
@csrf_exempt
def exchangeToken(request, athleteID):
    try:
        athlete = Athlete.objects.get(athleteId = athleteID)
        code = request.GET.get('code', '')
        scope = request.GET.get('scope', '')
        successfulExchange, exchangeMessage = exchangeAuthorizationToken(athlete, stravaConnection, code, scope)
        if successfulExchange == True:
            return JsonResponse({'Status': 'linked', 'message': exchangeMessage})
        elif successfulExchange == False:
            return JsonResponse({'Status': 'Please Try Again', 'message': exchangeMessage})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)



#calls for activities
@login_required
def createActivity(request):
    if request.method == 'POST':
        athlete = Athlete.objects.get(athleteId=request.GET.get("athleteID"))
        activityType = request.GET.get("type")
        description = request.GET.get("description")
        name = request.GET.get("name")
        movingTime = float(request.GET.get("movingTime"))#should be in seconds
        elapsedTime = float(request.GET.get("elapsedTime"))#should be in seconds
        startDate = request.GET.get("startDate") #"2024-04-15 03:26:03.262689+00:00"
        distance = float(request.GET.get("distance")) #should be in meters
        hasHeartrate = request.GET.get("hasHeartrate")
        if hasHeartrate == True:
            avgHeartrate = request.GET.get("avgHeartrate")
            maxHeartrate = request.GET.get("maxHeartrate")
        else:
            avgHeartrate = 0.0
            maxHeartrate = 0.0
        manual = request.GET.get("manual")
        if manual == False:
            hasGps = True
        else:
            hasGps = False
        if activityType == "run":
            averagePace = distance/movingTime
            maxPace = float(request.GET.get("maxPace"))
            
            averageCadence = float(request.GET.get("averageCadence"))
            try:
                newActivity = Run.objects.create(name=name, athlete=athlete, activityType=activityType, description=description, movingTime=movingTime, elapsedTime=elapsedTime, 
                                                 distance=distance, hasHeartrate=hasHeartrate, averageHeartrate=avgHeartrate, 
                                                 maxHeartrate=maxHeartrate, manual=manual, hasGps=hasGps,
                                                 averagePace=averagePace, maxPace=maxPace, averageCadence=averageCadence, startDate=startDate)
                newActivity.save()
                return JsonResponse({'message': 'Run created successfully',
                                     'activityId': newActivity.activityId})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
                
        elif activityType == "bike":
            averageSpeed = distance/movingTime
            maxSpeed = float(request.GET.get("maxSpeed"))
            try:
                newActivity = Bike.objects.create(name=name, athlete=athlete, activityType=activityType, description=description, movingTime=movingTime, elapsedTime=elapsedTime, 
                                                 distance=distance, hasHeartrate=hasHeartrate, averageHeartrate=avgHeartrate, 
                                                 maxHeartrate=maxHeartrate, manual=manual, hasGps=hasGps,
                                                 averageSpeed=averageSpeed, maxSpeed=maxSpeed, startDate=startDate)
                newActivity.save()
                return JsonResponse({'message': 'Bike created successfully',
                                     'activityId': newActivity.activityId})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        elif activityType == "swim":
            averageSpeed = distance/movingTime
            maxSpeed = float(request.GET.get("maxSpeed"))
            try:
                newActivity = Swim.objects.create(name=name, athlete=athlete, activityType=activityType, description=description, movingTime=movingTime, elapsedTime=elapsedTime, 
                                                 distance=distance, hasHeartrate=hasHeartrate, averageHeartrate=avgHeartrate, 
                                                 maxHeartrate=maxHeartrate, manual=manual, hasGps=hasGps,
                                                 averageSpeed=averageSpeed, maxSpeed=maxSpeed, startDate=startDate)
                newActivity.save()
                return JsonResponse({'message': 'Swim created successfully',
                                     'activityId': newActivity.activityId})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            activityType = "other"
            averageSpeed = distance/movingTime
            maxSpeed = float(request.GET.get("maxSpeed"))
            try:
                newActivity = Other.objects.create(name=name, athlete=athlete, activityType=activityType, description=description, movingTime=movingTime, elapsedTime=elapsedTime, 
                                                 distance=distance, hasHeartrate=hasHeartrate, averageHeartrate=avgHeartrate, 
                                                 maxHeartrate=maxHeartrate, manual=manual, hasGps=hasGps,
                                                 averageSpeed=averageSpeed, maxSpeed=maxSpeed, startDate=startDate)
                newActivity.save()
                return JsonResponse({'message': 'Other activity created successfully',
                                     'activityId': newActivity.activityId})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)  
    
@login_required
def getAthleteActivitiesRange(request, athleteID):
    if request.method == 'GET':
        athlete = Athlete.objects.get(athleteId=athleteID)
        
        activityType = request.GET.get("activityType")
        rangeStart = request.GET.get("rangeStart")
        rangeEnd = request.GET.get("rangeEnd")
        bikeData = {}
        runData = {}
        swimData = {}
        otherData = {}
        
        try:
            dateFilter = Q(startDate__gte=rangeStart, startDate__lte=rangeEnd) | Q(startDate__date=rangeEnd)
            bikeActivities = athlete.bikes.filter(dateFilter).order_by('startDate')
            bikeData = [str(activity) for activity in bikeActivities]
            runActivities = athlete.runs.filter(dateFilter).order_by('startDate')
            runData = [str(activity) for activity in runActivities]
            swimActivities =  athlete.swims.filter(dateFilter).order_by('startDate')
            swimData = [str(activity) for activity in swimActivities]
            otherActivities =  athlete.otherActivites.filter(dateFilter).order_by('startDate')
            otherData = [str(activity) for activity in otherActivities]
            if activityType == "bike":
                return JsonResponse({'bikeData': bikeData})
            elif activityType == "run":
               return JsonResponse({'runData': runData})
            elif activityType == "swim":
              return JsonResponse({'swimData': swimData})
            elif activityType == "other":
               return JsonResponse({'otherData': otherData})
            else:
                allActivitiesData = {
                'bikeData': bikeData,
                'runData': runData,
                'swimData': swimData,
                'otherData': otherData
                }
                return JsonResponse(allActivitiesData)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
    
@login_required
def getAthleteActivities(request, athleteID):
    if request.method == 'GET':
        athlete = Athlete.objects.get(athleteId=athleteID)
        
        activityType = request.GET.get("activityType")
        try:
            bikeActivities = sorted(athlete.bikes.all(), key=lambda activity: activity.startDate)
            bikeData = [str(activity) for activity in bikeActivities]
            runActivities =  sorted(athlete.runs.all(), key=lambda activity: activity.startDate)
            runData = [str(activity) for activity in runActivities]
            swimActivities =  sorted(athlete.swims.all(), key=lambda activity: activity.startDate)
            swimData = [str(activity) for activity in swimActivities]
            otherActivities =  sorted(athlete.otherActivites.all(), key=lambda activity: activity.startDate)
            otherData = [str(activity) for activity in otherActivities]
            if activityType == "bike":
                return JsonResponse({'bikeData': bikeData})
            elif activityType == "run":
               return JsonResponse({'runData': runData})
            elif activityType == "swim":
              return JsonResponse({'swimData': swimData})
            elif activityType == "other":
               return JsonResponse({'otherData': otherData})
            else:
                allActivitiesData = {
                'bikeData': bikeData,
                'runData': runData,
                'swimData': swimData,
                'otherData': otherData
                }
                return JsonResponse(allActivitiesData)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
        
@login_required
def getActivity(request,activityID):
    if request.method == 'GET':
        activityType = request.GET.get("activityType")
       
        try:
             if activityType == "run":
                 activity = Run.objects.get(activityId=activityID)
                 activityData = activity.jsonFormattedStr()
             elif activityType == "bike":
                 activity = Bike.objects.get(activityId=activityID)
                 activityData = activity.jsonFormattedStr()
             elif activity == "swim":
                 activity = Swim.objects.get(activityId=activityID)
                 activityData = activity.jsonFormattedStr()
             else:
                 activity = Other.objects.get(activityId=activityID)
                 activityData = activity.jsonFormattedStr()
             return JsonResponse(activityData)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
    
@login_required
def deleteActivity(request,activityID):
    if request.method == 'DELETE':
        
        try:
            activityType = request.GET.get("activityType")
            if activityType == "run":
                activity = Run.objects.get(activityId=activityID)
            elif activityType == "bike":
                activity = Bike.objects.get(activityId=activityID)
            elif activityType == "swim":
                activity = Swim.objects.get(activityId=activityID)
            else:
                activity = Other.objects.get(activityId=activityID)
            activity.delete()
            return JsonResponse({'message': 'Activity deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only DELETE requests are allowed'}, status=405)

@login_required
def updateActivity(request, activityID):
    if request.method == 'PUT':
        activityType = request.GET.get("activityType")
        if activityType == "run":
            activity = Run.objects.get(activityId=activityID)
        elif activityType == "bike":
            activity = Bike.objects.get(activityId=activityID)
        elif activityType == "swim":
            activity = Swim.objects.get(activityId=activityID)
        else:
            activity = Other.objects.get(activityId=activityID)
        try:
            activity.name = request.GET.get('name', activity.name)
            activity.description = request.GET.get('description', activity.description)
            activity.movingTime = request.GET.get('movingTime', activity.movingTime)
            activity.elapsedTime = request.GET.get('elapsedTime', activity.elapsedTime)
            activity.startDate = request.GET.get('startDate', activity.startDate)
            activity.distance = request.GET.get('distance', activity.distance)
            hasHeartrate = request.GET.get('hasHeartrate')
            if hasHeartrate == True:
                activity.hasHeartrate = True
                activity.avgHeartrate = request.GET.get("avgHeartrate")
                activity.maxHeartrate = request.GET.get("maxHeartrate")
            else:
                activity.avgHeartrate = 0.0
                activity.maxHeartrate = 0.0
            manual = request.GET.get("manual")
            if manual == False:
                activity.manual = False
                activity.hasGps = True
            else:
                activity.manual = True
                activity.hasGps = False
            if activity.activityType == "bike":
                activity.averageSpeed = request.GET.get('averageSpeed', activity.averageSpeed)
                activity.maxSpeed = request.GET.get('maxSpeed', activity.maxSpeed)
            elif activity.activityType == "run":
                activity.averagePace = request.GET.get('averagePace', activity.averagePace)
                activity.maxPace = request.GET.get('maxPace', activity.maxPace)
                activity.averageCadence = request.GET.get('averageCadence', activity.averageCadence)
            elif activity.activityType == "swim":
                activity.averageSpeed = request.GET.get('averageSpeed', activity.averageSpeed)
                activity.maxSpeed = request.GET.get('maxSpeed', activity.maxSpeed)
            elif activity.activityType == "other":
                activity.averageSpeed = request.GET.get('averageSpeed', activity.averageSpeed)
                activity.maxSpeed = request.GET.get('maxSpeed', activity.maxSpeed)
            activity.save()
            
            return JsonResponse({'message': 'Activity updated successfully', 'activityId': activity.activityId})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only PUT requests are allowed'}, status=405)





#calls for comments
@login_required
def createComment(request):
    if request.method == 'POST':
        activityType = request.GET.get('activityType')
        activityID = request.GET.get('activityID')
        commentText = request.GET.get('text')
        dateTime = timezone.now()
        try:
            if activityType=='bike':
                activity = Bike.objects.get(activityId=activityID)
                newComment = Comment.objects.create(text=commentText, postDate=dateTime, bikeActivity=activity)
            elif activityType=='run':
                activity = Run.objects.get(activityId=activityID)
                newComment = Comment.objects.create(text=commentText, postDate=dateTime, runActivity=activity)
            elif activityType=='swim':
                activity = Swim.objects.get(activityId=activityID)
                newComment = Comment.objects.create(text=commentText, postDate=dateTime, SwimActivity=activity)
            else:
                activity = Other.objects.get(activityId=activityID)
                newComment = Comment.objects.create(text=commentText, postDate=dateTime, otherActivity=activity)
            newComment.save()
            
            return JsonResponse({'message': 'Comment created successfully',
                                     'commentId': newComment.commentId})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405) 
    
@login_required
def deleteComment(request, commentID):
    if request.method == 'DELETE':
        try:
            comment = Comment.objects.get(commentId=commentID)
            comment.delete()
            return JsonResponse({'message': 'Comment deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only DELETE requests are allowed'}, status=405)
    
@login_required
def getComments(request, activityID):
 if request.method == 'GET':
     activityType = request.GET.get("activityType")
     try:
          if activityType == "run":
              activity = Run.objects.get(activityId=activityID)
          elif activityType == "bike":
              activity = Bike.objects.get(activityId=activityID)
          elif activity == "swim":
              activity = Swim.objects.get(activityId=activityID)
          else:
              activity = Other.objects.get(activityId=activityID)
          comments = activity.comments.order_by('postDate')
          commentsJson = []
          for comment in comments:
              commentData = {
                  'commentId': comment.commentId,
                  'text': comment.text}
              commentsJson.append(commentData)
          return JsonResponse({'comments': commentsJson})
     except Exception as e:
         return JsonResponse({'error': str(e)}, status=500)
 else:
     return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)





#calls for getting stats
@login_required
def getAthleteStats(request, athleteID):
    if request.method == 'GET':
        athlete = Athlete.objects.get(athleteId=athleteID)
        activityType = request.GET.get("activityType")
        rangeStart = request.GET.get("rangeStart")
        rangeEnd = request.GET.get("rangeEnd")
        bikeData = {}
        runData = {}
        swimData = {}
        otherData = {}
        try:
            dateFilter = Q(startDate__gte=rangeStart, startDate__lte=rangeEnd) | Q(startDate__date=rangeEnd)
            bikeActivities = athlete.bikes.filter(dateFilter)
            bikeDistance = bikeTime = bikeAverageHeartrate = bikeNumHeartrate = temp = 0
            for activity in bikeActivities:
                numBikes = len(bikeActivities)
                bikeDistance = bikeDistance + activity.distance
                bikeTime = bikeTime + activity.movingTime
                bikeAverageSpeed = bikeDistance/bikeTime #meters/second
                if activity.hasHeartrate:
                    bikeNumHeartrate = bikeNumHeartrate + 1
                    temp = temp + activity.averageHeartrate
                    bikeAverageHeartrate = temp/bikeNumHeartrate
                bikeData = {'numBikes': numBikes,
                                     'Distance': bikeDistance,
                                     'Time': bikeTime,
                                     'averageSpeed': bikeAverageSpeed,
                                     'averageDistance': bikeDistance/numBikes,
                                     'averageHeartrate': bikeAverageHeartrate}
            runActivities =  athlete.runs.filter(dateFilter)
            runDistance = runTime = runAverageHeartrate = runNumHeartrate = temp = 0
            for activity in runActivities:
                numRuns = len(runActivities)
                runDistance = runDistance + activity.distance
                runTime = runTime + activity.movingTime
                runAveragePace = runDistance/runTime #meters/second
                if activity.hasHeartrate:
                    runNumHeartrate = runNumHeartrate + 1
                    temp = temp + activity.averageHeartrate
                    runAverageHeartrate = temp/runNumHeartrate
                runData = {'numRuns': numRuns,
                                     'Distance': runDistance,
                                     'Time': runTime,
                                     'averagePace': runAveragePace,
                                     'averageDistance': runDistance/numRuns,
                                     'averageHeartrate': runAverageHeartrate}
            swimActivities =  athlete.swims.filter(dateFilter)
            swimDistance = swimTime = swimAverageHeartrate = swimNumHeartrate = temp = 0
            for activity in swimActivities:
                numSwims = len(swimActivities)
                swimDistance = swimDistance + activity.distance
                swimTime = swimTime + activity.movingTime
                swimAverageSpeed = swimDistance/swimTime #meters/second
                if activity.hasHeartrate:
                    swimNumHeartrate = swimNumHeartrate + 1
                    temp = temp + activity.averageHeartrate
                    swimAverageHeartrate = temp/swimNumHeartrate
                swimData = {'numSwims': numSwims,
                                     'Distance': swimDistance,
                                     'Time': swimTime,
                                     'averageSpeed': swimAverageSpeed,
                                     'averageDistance': swimDistance/numSwims,
                                     'averageHeartrate': swimAverageHeartrate}
            otherActivities =  athlete.otherActivites.filter(dateFilter)
            otherDistance = otherTime = otherAverageHeartrate = otherNumHeartrate = temp = 0
            for activity in otherActivities:
                numOthers = len(otherActivities)
                otherDistance = otherDistance + activity.distance
                otherTime = otherTime + activity.movingTime
                otherAverageSpeed = otherDistance/otherTime #meters/second
                if activity.hasHeartrate:
                    otherNumHeartrate = otherNumHeartrate + 1
                    temp = temp + activity.averageHeartrate
                    otherAverageHeartrate = temp/otherNumHeartrate
                otherData = {'numOthers': numOthers,
                                     'Distance': otherDistance,
                                     'Time': otherTime,
                                     'averageSpeed': otherAverageSpeed,
                                     'averageDistance': otherDistance/numOthers,
                                     'averageHeartrate': otherAverageHeartrate}
            if activityType == "bike":
                return JsonResponse({'bikeDate': bikeData})
            elif activityType == "run":
               return JsonResponse({'runData': runData})
            elif activityType == "swim":
              return JsonResponse({'swimData': swimData})
            elif activityType == "other":
               return JsonResponse({'otherData': otherData})
            else:
                allActivitiesData = {
                'bikeData': bikeData,
                'runData': runData,
                'swimData': swimData,
                'otherData': otherData
                }
                return JsonResponse(allActivitiesData)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)





#calls for rosters
@login_required
def addAthleteToTeam(request, athleteID):
    if request.method == 'POST' or request.method == 'PUT':
        try:
            athlete = Athlete.objects.get(athleteId = athleteID)
            athlete.team = Team.objects.get(teamId=request.GET.get('teamId'))
            athlete.save()
            return JsonResponse({'message': 'Athlete added to team successfully'})
        except Exception as e:
           return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST or PUT requests are allowed'}, status=405)
    
@login_required
def approveAthlete(request, athleteID):
    if request.method == 'POST' or request.method == 'PUT':
        try:
            athlete = Athlete.objects.get(athleteId=athleteID)
            athlete.pending = False
            athlete.save()
            return JsonResponse({'message': 'Athlete approved successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST or PUT requests are allowed'}, status=405)
    
@login_required
def removeAthleteFromTeam(request, athleteID):
    if request.method == 'POST' or request.method == 'PUT':
        try:
            athlete = Athlete.objects.get(athleteId = athleteID)
            athlete.pending = True
            athlete.team = None
            athlete.save()
            return JsonResponse({'message': 'Athlete removed from team successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST or PUT requests are allowed'}, status=405)
    
@login_required
def viewRoster(request, teamID):
    if request.method == 'GET':
        team = Team.objects.get(teamId=teamID)
        approvedAthletes = Athlete.objects.filter(team=team, pending=False)
        pendingAthletes = Athlete.objects.filter(team=team, pending=True)
        approvedRoster = [{
            'firstName': athlete.user.first_name,
            'lastName': athlete.user.last_name,
            'birthday': athlete.birthday,
            'schoolyear': athlete.schoolYear,
            'athleteId': athlete.athleteId
            }for athlete in approvedAthletes]
        pendingRoster = [{
            'firstName': athlete.user.first_name,
            'lastName': athlete.user.last_name,
            'birthday': athlete.birthday,
            'schoolyear': athlete.schoolYear,
            'athleteId': athlete.athleteId
            }for athlete in pendingAthletes]
        roster = {
            'approved': approvedRoster,
            'pending': pendingRoster
            }
        return JsonResponse(roster)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)





#calls for teams
@csrf_exempt
def createTeam(request):
    if request.method == 'POST':
        teamName = request.GET.get('teamName')
        try:
            newTeam = Team.objects.create(teamName=teamName)
            newTeam.save()
            return JsonResponse({'message': 'Team created successfully', 'teamId': newTeam.teamId})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
def getTeam(request, teamName):
    if request.method == 'GET':
        try:
            team = Team.objects.get(teamName=teamName)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        try:
            coaches = Coach.objects.filter(team=team)
            coachData = [{
                    'firstName': coach.user.first_name,
                    'lastName': coach.user.last_name
                } for coach in coaches]
            teamData = {
                    'teamId': team.teamId,
                    'teamName': team.teamName,
                    'coaches': coachData
                }
        except Exception as e:
            print(e)
            teamData = {
                    'teamId': team.teamId,
                    'teamName': team.teamName,
                    'coaches': ''
                }
        return JsonResponse(teamData)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
        
@login_required
def getTeamById(request, teamID):
    if request.method == 'GET':
        try:
            team = Team.objects.get(teamId=teamID)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        try:
            coaches = Coach.objects.filter(team=team)
            coachData = [{
                    'firstName': coach.user.first_name,
                    'lastName': coach.user.last_name
                } for coach in coaches]
            teamData = {
                    'teamId': team.teamId,
                    'teamName': team.teamName,
                    'coaches': coachData
                }
        except Exception as e:
            print(e)
            teamData = {
                    'teamId': team.teamId,
                    'teamName': team.teamName,
                    'coaches': ''
                }
        return JsonResponse(teamData)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
    
@login_required
def deleteTeam(request, teamID):
    if request.method == 'DELETE':
        try:
            team = Team.objects.get(teamId=teamID)
            team.delete()
            return JsonResponse({'message': 'Team deleted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only DELETE requests are allowed'}, status=405)
        