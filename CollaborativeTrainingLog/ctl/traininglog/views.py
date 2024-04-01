from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.http import JsonResponse
from django.core.serializers import serialize
from django.middleware import csrf
from .models import User, Athlete, Coach

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
        return JsonResponse({'error': 'User does not exist'}, status=404)
    
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
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
    else:
        return JsonResponse({'message': 'Only POST or PUT requests are allowed'}, status=405)

    
@csrf_exempt
def deleteUser(request, userID):
    if request.method == 'DELETE':
        try:
            user = User.objects.get(id=userID)
            user.delete()
            return JsonResponse({'message': 'User deleted successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
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
        user = athlete.user
        userID = user.id
        athleteData = {
                'id': athlete.athleteId,
                'birthday': athlete.birthday,
                'schoolYear': athlete.schoolYear,
                'teamID': athlete.team,
                'userID': userID,
            }
            
        return JsonResponse(athleteData)
    else:
        return JsonResponse({'error': 'Athlete does not exist'}, status=404)
    
@csrf_exempt
def updateAthlete(request, athleteID):
    if request.method == 'POST' or request.method == 'PUT':
        try:
            athlete = Athlete.objects.get(athleteId = athleteID)
            athlete.birthday = request.GET.get('birthday', athlete.birthday)
            athlete.schoolYear = request.GET.get('schoolYear',athlete.schoolYear)
            athlete.save()
            return JsonResponse({'message': 'Athlete updated successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Athlete does not exist'}, status=404)
    else:
        return JsonResponse({'message': 'Only POST or PUT requests are allowed'}, status=405)
    
@csrf_exempt
def deleteAthlete(request, athleteID):
    if request.method == 'DELETE':
        try:
            athlete = Athlete.objects.get(athleteId=athleteID)
            athlete.delete()
            return JsonResponse({'message': 'Athlete deleted successfully'})
        except User.DoesNotExist:
            return JsonResponse({'error': 'Athlete does not exist'}, status=404)
    else:
        return JsonResponse({'message': 'Only DELETE requests are allowed'}, status=405)
        

#calls for coach
# @csrf_exempt
# def createCoach(request):
#     if request.method == 'POST':
#         user = request.GET('user')
#         team = request.GET.get('team')
#         newCoach = Coach.objects.create(user=user, team=team)
#         newCoach.save()
#         return JsonResponse({'message': 'Coach created successfully'})
#     else:
#         return JsonResponse({'message', 'Only POST requests are allowed'}, status=405)
    