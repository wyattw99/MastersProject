import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';

import axios from 'axios';

axios.defaults.withCredentials = true
export default function APICalls() {

    // roster management
    function addAthleteToTeam() {
        axios.post(`http://127.0.0.1:8000/external/addToTeam/${localStorage.getItem("athleteID")}/`, null, {
            withCredentials: true,
            params: {
                teamId: 1,
            }
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }
    function approveAthlete() {
        axios.post(`http://127.0.0.1:8000/external/approveAthlete/${localStorage.getItem("athleteID")}/`, null, {
            withCredentials: true,
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }
    function removeAthleteFromTeam() {
        axios.post(`http://127.0.0.1:8000/external/removeFromTeam/${localStorage.getItem("athleteID")}/`, null, {
            withCredentials: true,
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }
    function viewTeamRoster() {
        axios.get(`http://127.0.0.1:8000/external/viewRoster/${localStorage.getItem("teamID")}/`, {
            withCredentials: true,
        })
            .then((response) => {
                console.log(response);
                
            }).catch(err => {
                console.log(err);
            });
    }

    // training groups
    function createTrainingGroup() {
        axios.post(`http://127.0.0.1:8000/external/newTrainingGroup`, null, {
            withCredentials: true,
            params: {
                groupName: "groupName",
            }
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }
    function getTrainingGroup() {
        axios.get(`http://127.0.0.1:8000/external/getTrainingGroup/groupID/`, {
            withCredentials: true,
        })
            .then((response) => {
                console.log(response);

            }).catch(err => {
                console.log(err);
            });
    }
    function deleteTrainingGroup() {
        axios.delete(`http://127.0.0.1:8000/external/deleteTrainingGroup/groupID/`, {
            withCredentials: true,
        })
            .then((response) => {
                console.log(response);

            }).catch(err => {
                console.log(err);
            });
    }
    function addAthleteToGroup() {
        axios.post(`http://127.0.0.1:8000/external/addAthleteToGroup/athleteID/`, null, {
            withCredentials: true,
            params: {
                groupID: 1,
            }
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }
    function removeAthleteFromGroup() {
        axios.post(`http://127.0.0.1:8000/external/removeAthleteFromGroup/athleteID/`, null, {
            withCredentials: true,
            params: {
                groupID: 1,
            }
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }

    // workouts
    function createWorkout() {
        axios.post(`http://127.0.0.1:8000/external/newWorkout`, null, {
            withCredentials: true,
            params: {
                coachID: 1,
                description: "description",
                date: dayjs(data.get('date')).format("YYYY-MM-DD"),
                title: "title",
            }
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }
    function getWorkout() {
        axios.get(`http://127.0.0.1:8000/external/getWorkout/workoutID/`, {
            withCredentials: true,
        })
            .then((response) => {
                console.log(response);

            }).catch(err => {
                console.log(err);
            });
    }
    function editWorkout() {
        axios.post(`http://127.0.0.1:8000/external/editWorkout/workoutID`, null, {
            withCredentials: true,
            params: {
                title: "title",
                description: "description",
                date: dayjs(data.get('date')).format("YYYY-MM-DD"),
            }
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }
    function copyWorkout() {
        axios.post(`http://127.0.0.1:8000/external/copyWorkout/workoutID`, null, {
            withCredentials: true,
            params: {
                newDate: dayjs(data.get('date')).format("YYYY-MM-DD"),
                newTitle: "title",
            }
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }
    function deleteWorkout() {
        axios.delete(`http://127.0.0.1:8000/external/deleteWorkout/workoutID/`, {
            withCredentials: true,
        })
            .then((response) => {
                console.log(response);

            }).catch(err => {
                console.log(err);
            });
    }
    function assignToAthletes() {
        axios.put(`http://127.0.0.1:8000/external/assignToAthletes`, null, {
            withCredentials: true,
            params: {
                workoutID: 1,
                numAthletes: "description",
                athleteIDs: IDlist,
            }
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }
    function removeAthletesFromWorkout() {
        axios.put(`http://127.0.0.1:8000/external/removeAthlete/workoutID/`, null, {
            withCredentials: true,
            params: {
                athleteID: 1,
            }
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }
    function getAthleteWorkouts() {
        axios.get(`http://127.0.0.1:8000/external/getWorkoutsRange/athleteID/`, {
            withCredentials: true,
            params: {
                rangeStart: dayjs(data.get('start')).format("YYYY-MM-DD"),
                rangeEnd: dayjs(data.get('start')).format("YYYY-MM-DD"),
            }
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }
    function getCoachWorkouts() {
        axios.get(`http://127.0.0.1:8000/external/getWorkoutsRange/coachID/`, {
            withCredentials: true,
            params: {
                rangeStart: dayjs(data.get('start')).format("YYYY-MM-DD"),
                rangeEnd: dayjs(data.get('start')).format("YYYY-MM-DD"),
            }
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }

    // activities
    function createActivity() {
        axios.post(`http://127.0.0.1:8000/external/newActivity`, null, {
            withCredentials: true,
            params: {
                athleteID: 1,
                type: "type",
                description: "description",
                name: "name",
                movingTime: 300,
                elapsedTime: 300,
                startDate: dayjs(data.get('date')),
                distance: 1609,
                hasHeartrate: true,
                avgHeartrate: 160, // if hasHeartrate is true
                maxHeartrate: 180, // if hasHeartrate is true
                manual: true,
                maxPace: 5.8, // if run
                averageCadence: 180, // if run
                maxSpeed: 6 // if bike or swim or other
            }
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }
    function getActivity() {
        axios.get(`http://127.0.0.1:8000/external/getActivity/activityID/`, {
            withCredentials: true,
            params: {
                activityType: "run",
            }
        })
            .then((response) => {
                console.log(response);

            }).catch(err => {
                console.log(err);
            });
    }
    function updateActivity() {
        axios.put(`http://127.0.0.1:8000/external/editActivity/activityID/`, null, {
            withCredentials: true,
            params: {
                type: "type",
                name: "name",
                description: "description",
                movingTime: 300,
                elapsedTime: 300,
                startDate: dayjs(data.get('date')),
                distance: 1609,
                hasHeartrate: true,
                avgHeartrate: 160, // if hasHeartrate is true
                maxHeartrate: 180, // if hasHeartrate is true
                manual: true,
                averagePage: 5.36, // if run
                maxPace: 5.8, // if run
                averageCadence: 180, // if run
                averageSpeed: 5.36, // if bike or swim or other
                maxSpeed: 6 // if bike or swim or other
            }
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }
    function deleteActivity() {
        axios.delete(`http://127.0.0.1:8000/external/deleteActivity/activityID/`, {
            withCredentials: true,
            params: {
                activityType: "run",
            }
        })
            .then((response) => {
                console.log(response);

            }).catch(err => {
                console.log(err);
            });
    }
    function getAthleteActivitiesRange() {
        axios.get(`http://127.0.0.1:8000/external/getAthleteActivitiesRange/athleteID/`, {
            withCredentials: true,
            params: {
                activityType: "run", // remove this to return all activities
                rangeStart: dayjs(data.get('start')).format("YYYY-MM-DD"),
                rangeEnd: dayjs(data.get('start')).format("YYYY-MM-DD"),
            }
        })
            .then((response) => {
                console.log(response);

            }).catch(err => {
                console.log(err);
            });
    }
    function getAthleteActivities() {
        axios.get(`http://127.0.0.1:8000/external/getAthleteActivities/athleteID/`, {
            withCredentials: true,
            params: {
                activityType: "run", // remove this to return all activities
            }
        })
            .then((response) => {
                console.log(response);

            }).catch(err => {
                console.log(err);
            });
    }

    // comments
    function createComment() {
        axios.post(`http://127.0.0.1:8000/external/createComment`, null, {
            withCredentials: true,
            params: {
                activityType: "run",
                activityID: 1,
                text: "Good job!",

            }
        })
            .then((response) => {
                console.log(response);
            }).catch(err => {
                console.log(err);
            });
    }
    function getComments() {
        axios.get(`http://127.0.0.1:8000/external/getComments/activityID/`, {
            withCredentials: true,
            params: {
                activityType: "run",
            }
        })
            .then((response) => {
                console.log(response);

            }).catch(err => {
                console.log(err);
            });
    }
    function deleteComment() {
        axios.delete(`http://127.0.0.1:8000/external/deleteComment/commentID/`, {
            withCredentials: true,
        })
            .then((response) => {
                console.log(response);

            }).catch(err => {
                console.log(err);
            });
    }

    // stats
    function getAthleteStats() {
        axios.get(`http://127.0.0.1:8000/external/getAthleteStats/athleteID/`, {
            withCredentials: true,
            params: {
                activityType: "run",
                rangeStart: dayjs(data.get('start')).format("YYYY-MM-DD"),
                rangeEnd: dayjs(data.get('start')).format("YYYY-MM-DD"),
            }
        })
            .then((response) => {
                console.log(response);

            }).catch(err => {
                console.log(err);
            });
    }

    // strava
    function getAccessToken() {
        axios.get(`http://127.0.0.1:8000/external/getAccessToken`, {
            withCredentials: true,
            params: {
                athleteID: 1,
            }
        })
            .then((response) => {
                console.log(response);

            }).catch(err => {
                console.log(err);
            });
    }
    function revokeStravaAccess() {
        axios.get(`http://127.0.0.1:8000/external/revokeStravaAccess`, {
            withCredentials: true,
            params: {
                athleteID: 1,
            }
        })
            .then((response) => {
                console.log(response);

            }).catch(err => {
                console.log(err);
            });
    }
    function syncStravaActivities() {
        axios.get(`http://127.0.0.1:8000/external/getStravaActivities`, {
            withCredentials: true,
            params: {
                athleteID: 1,
            }
        })
            .then((response) => {
                console.log(response);

            }).catch(err => {
                console.log(err);
            });
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

        addAthleteToTeam();
    };

    return (
        <Container component="main" maxWidth="xs">
            <CssBaseline />
            <Box boxShadow={12} bgcolor="#CEB4D5"
                sx={{
                    marginTop: 5,
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    opacity: 0.8,
                }}
            >
                <Typography component="h1" variant="h5" sx={{ marginTop: 5 }}>
                    API Calls
                </Typography>
                <Box component="form" onSubmit={handleSubmit} noValidate autoComplete="off" sx={{ mt: 1, width: 300 }}>
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="light"

                        sx={{
                            mt: 3, mb: 2
                        }}
                    >
                        Test Call
                    </Button>
                </Box>
            </Box>
        </Container>
    );
}