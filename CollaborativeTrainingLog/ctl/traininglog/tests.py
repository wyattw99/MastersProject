from django.test import TestCase, Client
from django.urls import reverse
#from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import StravaAPI, User, Athlete, Team, Coach, Workout, TrainingGroup
from django.core.exceptions import ObjectDoesNotExist

# Create your tests here.

#To run automated tests please manually create a stravaAPI Connection in views.py or see below instructions, 
#all tests will fail as they use a sample database that does not contain the api clientId and secret
#Comment out views.py line 578, uncomment line 577 views.py, uncomment line 85 settings.py

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
        
    def testCreateCoach(self):
        username = 'testCoach'
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
        self.assertTrue(user.username == 'testCoach')
        
    def testCreateAthlete(self):
        username = 'testAthlete'
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
        self.assertTrue(user.username == 'testAthlete')
        
    def testGetUser(self):
        client = Client()
        client.login(username='testUser', password='testPassword')
        url = reverse('traininglog:getUser', kwargs={'userID': self.user.id})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['username'] == 'testUser')
        client.logout()
        
    def testUpdateUser(self):
        client = Client()
        client.login(username='testUser', password='testPassword')
        email = 'test@test.com'
        first_name = 'Updated'
        last_name = 'Updated'
        paramString = f'?first_name={first_name}&last_name={last_name}&email={email}'
        url = reverse('traininglog:updateUser', kwargs={'userID':self.user.id})+paramString
        response = client.put(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'User updated successfully')
        updatedUser = User.objects.get(id=self.user.id)
        self.assertEqual(updatedUser.email, 'test@test.com')
        self.assertEqual(updatedUser.first_name, 'Updated')
        
    def testDeleteUser(self):
        client = Client()
        client.login(username='testUser', password='testPassword')
        url = reverse('traininglog:deleteUser', kwargs={'userID': self.user.id})
        response = client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'User deleted successfully')
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
        
class AthleteTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testAthlete1', password='testPassword')
    
    def testCreateAthlete(self):
        birthday ='2000-01-01'
        schoolYear= 'Senior'
        userID = self.user.id
        paramString = f'?birthday={birthday}&schoolYear={schoolYear}&userID={userID}'
        url = reverse('traininglog:newAthlete')+paramString
        response = self.client.post(url)
        responseAthleteId = response.json()['athleteId']
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Athlete created successfully')
        athlete = Athlete.objects.get(athleteId=responseAthleteId)
        self.assertTrue(athlete.schoolYear == 'Senior')

    def testGetAthlete(self):
        athlete = Athlete.objects.create(user = self.user, birthday='2000-01-01', schoolYear='Senior')
        client = Client()
        client.login(username='testAthlete1', password='testPassword')
        url = reverse('traininglog:getAthlete', kwargs={'athleteID' :athlete.athleteId})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], athlete.athleteId)

    def testUpdateAthlete(self):
        athlete = Athlete.objects.create(user = self.user, birthday='2000-01-01', schoolYear='Senior')
        client = Client()
        client.login(username='testAthlete1', password='testPassword')
        birthday ='1990-01-01'
        schoolYear= 'Freshman'
        userID = self.user.id
        paramString = f'?birthday={birthday}&schoolYear={schoolYear}&userID={userID}'
        url = reverse('traininglog:updateAthlete', kwargs={'athleteID': athlete.athleteId})+paramString
        response = client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Athlete updated successfully')

    def testDeleteAthlete(self):
        athlete = Athlete.objects.create(user = self.user, birthday='2000-01-01', schoolYear='Senior')
        client = Client()
        client.login(username='testAthlete1', password='testPassword')
        url = reverse('traininglog:deleteAthlete', kwargs={'athleteID': athlete.athleteId})
        response = client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Athlete deleted successfully')
        
class CoachTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testCoach1', password='testPassword')
        self.team = Team.objects.create(teamName='test team')
    
    def testCreateCoach(self):
        teamId = self.team.teamId
        userId = self.user.id
        paramString = f'?userId={userId}&teamId={teamId}'
        url = reverse('traininglog:newCoach')+paramString
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Coach created successfully')

    def testGetCoach(self):
        coach = Coach.objects.create(user = self.user, team = self.team)
        client = Client()
        client.login(username='testCoach1', password='testPassword')
        url = reverse('traininglog:getCoach', kwargs={'coachID' :coach.coachId})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['id'], coach.coachId)

    def testDeleteCoach(self):
        coach = Coach.objects.create(user = self.user, team = self.team)
        client = Client()
        client.login(username='testCoach1', password='testPassword')
        url = reverse('traininglog:deleteCoach', kwargs={'coachID' :coach.coachId})
        response = client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Coach deleted successfully')
    
class TeamTestCase(TestCase):
    def setUp(self):
        self.team = Team.objects.create(teamName='test team')
        self.user = User.objects.create_user(username='testUser', password='testPassword')
    
    def testCreateTeam(self):
        teamName = 'test team'
        paramString = f'?teamName={teamName}'
        url = reverse('traininglog:newTeam')+paramString
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Team created successfully')

    def testGetTeam(self):
        team = Team.objects.create(teamName='test get team')
        client = Client()
        client.login(username='testUser', password='testPassword')
        url = reverse('traininglog:getTeam', kwargs={'teamName' :team.teamName})
        response = client.get(url)
        self.assertEqual(response.json()['teamId'], team.teamId)

    def testDeleteTeam(self):
        team = Team.objects.create(teamName='test team')
        client = Client()
        client.login(username='testUser', password='testPassword')
        url = reverse('traininglog:deleteTeam', kwargs={'teamID' :team.teamId})
        response = client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Team deleted successfully') 
        
class RosterTestCase(TestCase):
    #only manual test of roster view
    def setUp(self):
        self.team = Team.objects.create(teamName='roster team')
        self.user = User.objects.create_user(username='testUser', password='testPassword')
        #self.athlete = Athlete.objects.create(user=self.user, birthday='2000-01-01', schoolYear='Senior')
    
    def testAddToTeam(self):
        athlete = Athlete.objects.create(user=self.user, birthday='2000-01-01', schoolYear='Senior')
        client = Client()
        client.login(username='testUser', password='testPassword')
        teamId = self.team.teamId
        url = reverse('traininglog:addToTeam', kwargs={'athleteID': athlete.athleteId})+f'?teamId={teamId}'
        response = client.post(url)
        athlete.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Athlete added to team successfully')
        self.assertEqual(athlete.team.teamId, teamId)
    
    def testApproveAthlete(self):
        athlete = Athlete.objects.create(user=self.user, birthday='2000-01-01', schoolYear='Senior')
        athlete.team = self.team
        client = Client()
        client.login(username='testUser', password='testPassword')
        url = reverse('traininglog:approveAthlete', kwargs={'athleteID': athlete.athleteId})
        response = client.post(url)
        athlete.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Athlete approved successfully')
        self.assertFalse(athlete.pending)
        
    def removeAthlete(self):
        athlete = Athlete.objects.create(user=self.user, birthday='2000-01-01', schoolYear='Senior')
        athlete.team = self.team
        athlete.pending = False
        client = Client()
        client.login(username='testUser', password='testPassword')
        url = reverse('traininglog:removeAthleteFromTeam', kwargs={'athleteID': athlete.athleteId})
        response = client.post(url)
        athlete.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Athlete removed from team successfully')
        self.assertTrue(athlete.pending)
        self.assertEqual(athlete.team, None)
        
class WorkoutTestCase(TestCase):
    #only manual tests for get workouts by athlete and coach by range
    def setUp(self):
        self.team = Team.objects.create(teamName='test team')
        self.athleteUser = User.objects.create_user(username='testAthlete1', password='testPassword')
        self.coachUser = User.objects.create_user(username='testCoach1', password='testPassword')
        self.athlete = Athlete.objects.create(user=self.athleteUser, birthday='2000-01-01', schoolYear='Senior')
        self.coach = Coach.objects.create(user = self.coachUser, team = self.team)
        
    def testCreateWorkout(self):
        client = Client()
        client.login(username='testCoach1', password='testPassword')
        paramsString = f'?coachID={self.coach.coachId}&description=TestDescription&date=2024-05-10&title=TestTitle'
        url = reverse('traininglog:newWorkout')+paramsString
        response = client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Workout created successfully')
        responseId = response.json()['workoutID']
        workout = Workout.objects.get(workoutId=responseId)
        self.assertEqual(workout.title, 'TestTitle')
        
    def testAssignToAthlete(self):
        client = Client()
        client.login(username='testCoach1', password='testPassword')
        workout = Workout.objects.create(coach=self.coach, title='TestTitle', assignedDate='2024-05-10', description='TestDescription')
        paramString = f'?workoutID={workout.workoutId}&numAthletes=1&athleteIDs={self.athlete.athleteId}'
        url = reverse('traininglog:assignToAthletes')+paramString
        response = client.put(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Athletes Assigned to Workout')
        self.athlete.refresh_from_db()
        workouts = self.athlete.assignedWorkouts.all()
        self.assertEquals(workouts[0].workoutId, workout.workoutId)
        
    def testGetWorkout(self):
        client = Client()
        client.login(username='testCoach1', password='testPassword')
        workout = Workout.objects.create(coach=self.coach, title='TestTitle', assignedDate='2024-05-10', description='TestDescription')
        workout.athletes.add(self.athlete)
        url = reverse('traininglog:getWorkout', kwargs={'workoutID': workout.workoutId})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['workoutID'], workout.workoutId)
        
    def testRemoveAthleteFromWorkout(self):
        client = Client()
        client.login(username='testCoach1', password='testPassword')
        workout = Workout.objects.create(coach=self.coach, title='TestTitle', assignedDate='2024-05-10', description='TestDescription')
        workout.athletes.add(self.athlete)
        paramString = f'?athleteID={self.athlete.athleteId}'
        url = reverse('traininglog:removeAthlete', kwargs={'workoutID': workout.workoutId})+paramString
        response =client.put(url)
        self.athlete.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Athlete Removed from Workout')
        workouts = self.athlete.assignedWorkouts.all()
        self.assertFalse(workouts.exists())
        
    def testEditWorkout(self):
        client = Client()
        client.login(username='testCoach1', password='testPassword')
        workout = Workout.objects.create(coach=self.coach, title='TestTitle', assignedDate='2024-05-10', description='TestDescription')
        paramString = '?title=UpdatedTitle&description=UpdatedDescription&assignedDate=2024-05-11'
        url = reverse('traininglog:editWorkout', kwargs={'workoutID': workout.workoutId})+paramString
        response = client.put(url)
        workout.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Workout updated successfully')
        self.assertTrue(workout.title,'UpdatedTitle')
        
    def testCopyWorkout(self):
        client = Client()
        client.login(username='testCoach1', password='testPassword')
        workout = Workout.objects.create(coach=self.coach, title='TestTitle', assignedDate='2024-05-10', description='TestDescription')
        paramString = '?newTitle=CopiedTitle&newDate=2024-05-12'
        url = reverse('traininglog:copyWorkout', kwargs={'workoutID': workout.workoutId})+paramString
        response = client.post(url)
        responseId = response.json()['workoutID']
        newWorkout = Workout.objects.get(workoutId=responseId)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Workout copied successfully')
        self.assertEqual(newWorkout.title, 'CopiedTitle')
        
    def testDeleteWorkout(self):
        client = Client()
        client.login(username='testCoach1', password='testPassword')
        workout = Workout.objects.create(coach=self.coach, title='TestTitle', assignedDate='2024-05-10', description='TestDescription')
        url = reverse('traininglog:deleteWorkout', kwargs={'workoutID': workout.workoutId})
        response = client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Workout deleted successfully')
        try:
            deletedWorkout = Workout.objects.get(workoutId=workout.workoutId)
        except ObjectDoesNotExist:
            deletedWorkout = None
        self.assertIsNone(deletedWorkout)
        
class GroupTestCase(TestCase):
    #manual tests for getting groups by team
    def setUp(self):
        self.team = Team.objects.create(teamName = 'test team')
        self.user = User.objects.create_user(username='testUser', password='testPassword')
        self.athlete = Athlete.objects.create(user=self.user, birthday='2000-01-01', schoolYear='Senior')
        
    def testCreateGroup(self):
        client = Client()
        client.login(username='testUser', password='testPassword')
        paramString = f'?groupName=TestGroup&teamID={self.team.teamId}'
        url = reverse('traininglog:newTrainingGroup')+paramString
        response = client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Group created successfully')
        group = TrainingGroup.objects.get(groupId=response.json()['groupId'])
        self.assertEqual(group.groupName,'TestGroup')
        
    def testAddAthleteToGroup(self):
        group = TrainingGroup.objects.create(groupName='TestGroup', team=self.team)
        client = Client()
        client.login(username='testUser', password='testPassword')
        paramString = f'?groupID={group.groupId}'
        url = reverse('traininglog:addToTrainingGroup', kwargs={'athleteID': self.athlete.athleteId})+paramString
        response = client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Athlete added to group successfully')
        athletes = group.athletes.all()
        self.assertEquals(athletes[0].athleteId, self.athlete.athleteId)
        
    def testGetGroup(self):
        group = TrainingGroup.objects.create(groupName='TestGroup', team=self.team)
        client = Client()
        client.login(username='testUser', password='testPassword')
        url = reverse('traininglog:getTrainingGroup', kwargs={'groupID': group.groupId})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['groupName'], 'TestGroup')
        
    def testRemoveAthleteFromGroup(self):
        group = TrainingGroup.objects.create(groupName='TestGroup', team=self.team)
        self.athlete.trainingGroups.add(group)
        client = Client()
        client.login(username='testUser', password='testPassword')
        paramString = f'?groupID={group.groupId}'
        url = reverse('traininglog:removeFromTrainingGroup', kwargs={'athleteID': self.athlete.athleteId})+paramString
        response = client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Athlete removed from team successfully')
        groups = self.athlete.trainingGroups.all()
        self.assertFalse(groups.exists())
        
    def testDeleteGroup(self):
        group = TrainingGroup.objects.create(groupName='TestGroup', team=self.team)
        client = Client()
        client.login(username='testUser', password='testPassword')
        url = reverse('traininglog:deleteTrainingGroup', kwargs={'groupID':group.groupId})
        response = client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('message' in response.json() and response.json()['message'] == 'Group deleted successfully')
        try:
            deletedGroup = TrainingGroup.objects.get(groupId=group.groupId)
        except ObjectDoesNotExist:
            deletedGroup = None
        self.assertIsNone(deletedGroup)
        
#manual tests for all strava, activity, stats, and comment calls