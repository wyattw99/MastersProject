from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import JsonResponse
from django.middleware import csrf
from .models import User, Athlete, Coach, Team, Workout, TrainingGroup, Activity, Run, Bike, Swim, Other

# Create your views here.
@csrf_exempt
def loginRequest(request):
    if request.method == 'POST':
        username = request.GET.get('username')
        print(username)
        password = request.GET.get('password')
        print(password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            csrf_token = csrf.get_token(request)
            return JsonResponse({'message': 'Login successful', 'csrf_token': csrf_token})
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
    
        
    
    
        
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
            return JsonResponse({'message': 'User created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
def getUser(request, userID):
    if request.method == 'GET':
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
            
        return JsonResponse(userData)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
    
@csrf_exempt
def updateUser(request, userID):
    if request.method == 'POST' or request.method == 'PUT':
        try:
            user = User.objects.get(id=userID)
            user.email = request.GET.get('email', user.email)
            user.first_name = request.GET.get('first_name', user.first_name)
            user.last_name = request.GET.get('last_name', user.last_name)
            user.save()
            return JsonResponse({'message': 'User updated successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST or PUT requests are allowed'}, status=405)

@csrf_exempt
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
            return JsonResponse({'message': 'Athlete created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def getAthlete(request, athleteID):
    if request.method == 'GET':
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
    else:
        return JsonResponse({'message': 'Athlete does not exist'}, status=405)
    
@csrf_exempt
def updateAthlete(request, athleteID):
    if request.method == 'POST' or request.method == 'PUT':
        try:
            athlete = Athlete.objects.get(athleteId = athleteID)
            athlete.birthday = request.GET.get('birthday', athlete.birthday)
            athlete.schoolYear = request.GET.get('schoolYear',athlete.schoolYear)
            athlete.save()
            return JsonResponse({'message': 'Athlete updated successfully'})
        except Exception as e:
           return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST or PUT requests are allowed'}, status=405)
    
@csrf_exempt
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
            return JsonResponse({'message': 'Coach created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message', 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def getCoach(request, coachID):
    if request.method == 'GET':
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
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
    
@csrf_exempt
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
@csrf_exempt
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
    
@csrf_exempt
def assignToAthletes(request):
    if request.method == 'PUT':
        workout = Workout.objects.get(workoutId = request.GET.get("workoutID"))
        numAthletes = int(request.GET.get("numAthletes"))
        if numAthletes > 1:
            athleteIDs = request.GET.get("athleteIDs").split(",")   
            athletes = Athlete.objects.filter(pk__in=athleteIDs)  
        else:
            athleteIDs = request.GET.get("athleteIDs")
            athletes = Athlete.objects.get(athleteId=athleteIDs)
        try:
            for athlete in athletes:
                workout.athletes.add(athlete)
            workout.save()
            return JsonResponse({'message': 'Athletes Assigned to Workout'})     
        except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message', 'Only Put requests are allowed'}, status=405)

@csrf_exempt
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
    
@csrf_exempt
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
        
@csrf_exempt
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
    
@csrf_exempt
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
    
@csrf_exempt
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
        
   
    
   
    
#calls for training groups
@csrf_exempt
def createTrainingGroup(request):
    if request.method == 'POST':
        groupName = request.GET.get('groupName')
        team = Team.objects.get(teamId=request.GET.get('teamID'))
        try:
            newGroup = TrainingGroup.objects.create(groupName=groupName,team=team)
            newGroup.save()
            return JsonResponse({'message': 'Group created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
def getTrainingGroup(request, groupID):
    if request.method == 'GET':
        group = TrainingGroup.objects.get(groupId=groupID)
        try:
            athletes = group.athletes.all()
            athleteData = [{
                    'firstName': athlete.user.first_name,
                    'lastName': athlete.user.last_name
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
    
@csrf_exempt
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
    
@csrf_exempt
def addAthleteToGroup(request, athleteID):
    if request.method == 'POST' or request.method == 'PUT':
        try:
            athlete = Athlete.objects.get(athleteId = athleteID)
            athlete.trainingGroups = TrainingGroup.objects.get(groupId=request.GET.get('groupID'))
            athlete.save()
            return JsonResponse({'message': 'Athlete added to group successfully'})
        except Exception as e:
           return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST or PUT requests are allowed'}, status=405)

@csrf_exempt
def removeAthleteFromGroup(request, athleteID):
    if request.method == 'POST' or request.method == 'PUT':
        try:
            athlete = Athlete.objects.get(athleteId = athleteID)
            athlete.trainingGroups.remove(request.Get.get("groupID"))
            athlete.save()
            return JsonResponse({'message': 'Athlete removed from team successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST or PUT requests are allowed'}, status=405)





#calls for strava





#calls for activities
@csrf_exempt
def createActivity(request):
    if request.method == 'POST':
        athlete = Athlete.objects.get(athleteId=request.GET.get("athleteID"))
        activityType = request.GET.get("type")
        description = request.GET.get("description")
        name = request.GET.get("name")
        movingTime = request.GET.get("movingTime")
        elapsedTime = request.GET.get("elapsedTime")
        #startDate = request.GET.get("startDate")
        distance = request.GET.get("distance") #should be in meters
        hasHeartrate = request.GET.get("heartrate")
        if hasHeartrate:
            avgHeartrate = request.GET.get("avgHeartrate")
            maxHeartrate = request.GET.get("maxHeartrate")
        else:
            avgHeartrate = None
            maxHeartrate = None
        manual = request.GET.get("manual")
        if not manual:
            hasGps = True
        else:
            hasGps = False
        if activityType == "run":
            averagePace = request.GET.get("averagePace")
            maxPace = request.GET.get("maxPace")
            averageCadence = request.GET.get("averageCadence")
            try:
                newActivity = Run.objects.create(name=name, athlete=athlete, activityType=activityType, description=description, movingTime=movingTime, elapsedTime=elapsedTime, 
                                                 distance=distance, hasHeartRate=hasHeartrate, averageHeartrate=avgHeartrate, 
                                                 maxHeartrate=maxHeartrate, manual=manual, hasGps=hasGps,
                                                 averagePace=averagePace, maxPace=maxPace, averageCadence=averageCadence)
                newActivity.save()
                return JsonResponse({'message': 'Run created successfully',
                                     'activityId': newActivity.activityId})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
                
        elif activityType == "bike":
            averageSpeed = request.GET.get("averageSpeed")
            maxSpeed = request.GET.get("maxSpeed")
            try:
                newActivity = Bike.objects.create(name=name, athlete=athlete, activityType=activityType, description=description, movingTime=movingTime, elapsedTime=elapsedTime, 
                                                 distance=distance, hasHeartRate=hasHeartrate, averageHeartrate=avgHeartrate, 
                                                 maxHeartrate=maxHeartrate, manual=manual, hasGps=hasGps,
                                                 averageSpeed=averageSpeed, maxSpeed=maxSpeed)
                newActivity.save()
                return JsonResponse({'message': 'Bike created successfully',
                                     'activityId': newActivity.activityId})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        elif activityType == "swim":
            averageSpeed = request.GET.get("averageSpeed")
            maxSpeed = request.GET.get("maxSpeed")
            try:
                newActivity = Other.objects.create(name=name, athlete=athlete, activityType=activityType, description=description, movingTime=movingTime, elapsedTime=elapsedTime, 
                                                 distance=distance, hasHeartRate=hasHeartrate, averageHeartrate=avgHeartrate, 
                                                 maxHeartrate=maxHeartrate, manual=manual, hasGps=hasGps,
                                                 averageSpeed=averageSpeed, maxSpeed=maxSpeed)
                newActivity.save()
                return JsonResponse({'message': 'Swimm created successfully',
                                     'activityId': newActivity.activityId})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            activityType = "other"
            averageSpeed = request.GET.get("averageSpeed")
            maxSpeed = request.GET.get("maxSpeed")
            try:
                newActivity = Other.objects.create(name=name, athlete=athlete, activityType=activityType, description=description, movingTime=movingTime, elapsedTime=elapsedTime, 
                                                 distance=distance, hasHeartRate=hasHeartrate, averageHeartrate=avgHeartrate, 
                                                 maxHeartrate=maxHeartrate, manual=manual, hasGps=hasGps,
                                                 averageSpeed=averageSpeed, maxSpeed=maxSpeed)
                newActivity.save()
                return JsonResponse({'message': 'Other activity created successfully',
                                     'activityId': newActivity.activityId})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)  
    
@csrf_exempt
def getAthleteActivities(request, athleteID):
    if request.method == 'GET':
        athlete = Athlete.objects.get(athleteId=request.GET.get("athleteID"))
        activityType = request.GET.get("activityType")
        try:
            bikeActivities = athlete.bikes
            bikeData = [str(activity) for activity in bikeActivities]
            runActivities = athlete.runs
            runData = [str(activity) for activity in runActivities]
            swimActivities = athlete.swims
            swimData = [str(activity) for activity in swimActivities]
            otherActivities = athlete.otherActivities
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
        
@csrf_exempt
def getActivity(request,activityID):
    if request.method == 'GET':
        activity = Activity.objects.get(activityId=activityID)
        try:
            activityData = activity.jsonFormattedStr()
            return JsonResponse(activityData)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only GET requests are allowed'}, status=405)
    


    


#calls for comments





#calls for getting stats





#calls for rosters
@csrf_exempt
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
    
@csrf_exempt
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
    
@csrf_exempt
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
    
@csrf_exempt
def viewRoster(request, teamID):
    if request.method == 'GET':
        team = Team.objects.get(teamId=teamID)
        approvedAthletes = Athlete.objects.filter(team=team, pending=False)
        pendingAthletes = Athlete.objects.filter(team=team, pending=True)
        approvedRoster = [{
            'firstName': athlete.user.first_name,
            'lastName': athlete.user.last_name,
            'birthday': athlete.birthday,
            'schoolyear': athlete.schoolYear
            }for athlete in approvedAthletes]
        pendingRoster = [{
            'firstName': athlete.user.first_name,
            'lastName': athlete.user.last_name,
            'birthday': athlete.birthday,
            'schoolyear': athlete.schoolYear
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
            return JsonResponse({'message': 'Team created successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'message': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
def getTeam(request, teamName):
    if request.method == 'GET':
        team = Team.objects.get(teamName=teamName)
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
    
@csrf_exempt
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
        