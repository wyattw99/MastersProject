from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import JsonResponse
from django.core.serializers import serialize
from django.middleware import csrf
from .models import User, Athlete, Coach, Team

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





#calls for training groups





#calls for strava





#calls for activities





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
        except User.DoesNotExist:
            return JsonResponse({'error': 'Team does not exist'}, status=404)
    else:
        return JsonResponse({'message': 'Only DELETE requests are allowed'}, status=405)
        