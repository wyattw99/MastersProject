from django.test import TestCase
from django.urls import reverse
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import StravaAPI, User

# Create your tests here.
class LoginTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testUser', password='testPassword')

        
    def testLoginandLogout(self):
        #test login
        loginUrl = reverse('traininglog:login') + '?username=testUser&password=testPassword'
        response = self.client.post(loginUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Login successful')
        #test logut
        logoutUrl = reverse('traininglog:logout')
        response = self.client.post(logoutUrl)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Logout successful')
        
class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testUser', password='testPassword')
        self.user.isCoach = True
        self.user.isAthlete = False
        self.user.save()
        
    def testCreateCoach(self):
        username = 'test'
        password = 'test'
        email = 'test@test.com'
        first_name = 'test'
        last_name = 'test'
        isCoach = True
        isAthlete = False
        paramString = f'?username={username}&password={password}&email={email}&isCoach={isCoach}&isAthlete={isAthlete}&first_name={first_name}&last_name={last_name}'
        url = reverse('traininglog:newUser')+paramString
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'User created successfully')
        responseUserId = response.json()['userId']
        user = User.objects.get(id=responseUserId)
        print(user.username)
        self.assertTrue(user.username == 'test')
        
