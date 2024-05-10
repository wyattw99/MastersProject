# Collaborative Training Log (CPSC-69100 Master's Project)

For convenience and utility, the proposed Collaborative Training Log web application acts as a hub where athletes and coaches can easily share details pertaining to their training. Coaches can enter mileage requirements, workout repetitions and goal splits, and any extra notes they have for a given day. In return, the athletes can upload activities manually or sync them from Strava (via API) and provide daily feedback. This application will include a calendar view for progress tracking and planning and a summary view where the coach can quickly access all feedback for a particular day. The coach will also be given the ability to create training groups where all athletes in the same group can be assigned the same workouts and mileage. Athletes will have similar views, but only for their own activities. There will also be screens, both a coach and athlete version, for entering daily training information. 

## React Front-End

### Scripts (run these within the ctl-ui directory)

#### Install dependencies
#### `npm install`

#### Run App in development mode:
#### `npm start`

### Libraries/Frameworks

Components are utilized from the React framework Material-UI

## Django Back-End

### Dependencies
Please see requirements.txt
To install:
#### `pip install -r requirements.txt`

### Running Server
Navigate to CollaborativeTrainingLog\ctl

Call:
#### `python manage.py runserver`

The server will be running on 127.0.0.1:8000

#### Automated Testing
To run the automated tests please see the instructions in \traininglog\tests.py to configure the project

Once the project is set up call

#### `python manage.py test traininglog`

