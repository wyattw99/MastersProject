import * as React from 'react';
import { useState } from 'react';
import { experimentalStyled as styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Unstable_Grid2';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Container from '@mui/material/Container';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import MenuItem from '@mui/material/MenuItem';
import Divider from '@mui/material/Divider';

import dayjs from 'dayjs';
import axios from 'axios';

const date = dayjs();

const types = [
    {
        value: 'run',
        label: 'Run',
    },
    {
        value: 'bike',
        label: 'Bike',
    },
    {
        value: 'swim',
        label: 'Swim',
    },
    {
        value: 'other',
        label: 'Other',
    },
];

const Item = styled(Paper)(({ theme }) => ({
    backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
    ...theme.typography.body2,
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
}));

export default function WorkoutView() {
    const [submitted, setSubmitted] = useState(false);
    const [workouts, setWorkouts] = useState([]);

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

        if (localStorage.getItem("isAthlete") === 'true') {
            axios.get(`http://127.0.0.1:8000/external/getWorkoutsRange/${localStorage.getItem("athleteID")}/`, {
                withCredentials: true,
                params: {
                    rangeStart: dayjs(data.get('startDate')).format("YYYY-MM-DD"),
                    rangeEnd: dayjs(data.get('endDate')).format("YYYY-MM-DD"),
                }
            })
                .then((response) => {
                    console.log(response);
                    setWorkouts(response.data.assignedWorkouts);
                }).catch(err => {
                    console.log(err);
                });
        }
        if (localStorage.getItem("isAthlete") === 'false') {
            axios.get(`http://127.0.0.1:8000/external/getCoachWorkoutsRange/${localStorage.getItem("coachID")}/`, {
                withCredentials: true,
                params: {
                    rangeStart: dayjs(data.get('startDate')).format("YYYY-MM-DD"),
                    rangeEnd: dayjs(data.get('endDate')).format("YYYY-MM-DD"),
                }
            })
                .then((response) => {
                    console.log(response);
                    console.log(response.data.assignedWorkouts);
                    setWorkouts(response.data.assignedWorkouts);
                }).catch(err => {
                    console.log(err);
                });
        }
    }

    return (
        <Box sx={{ display: 'flex' }}>
            <Box
                component="main"
                sx={{
                    backgroundColor: (theme) =>
                        theme.palette.mode === 'light'
                            ? theme.palette.grey[100]
                            : theme.palette.grey[900],
                    flexGrow: 1,
                    height: '100vh',
                    overflow: 'auto',
                }}
            >
                <Container component="main" maxWidth="xs">
                    <CssBaseline />
                    <Box boxShadow={12}
                        sx={{
                            marginTop: 5,
                            mb: 2,
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            opacity: 0.8,
                        }}
                    >
                        <Typography component="h1" variant="h5" sx={{ marginTop: 5 }}>
                            Select Workout Range
                        </Typography>
                        <Box component="form" noValidate onSubmit={handleSubmit} autoComplete="off" sx={{ mt: 3, width: 300 }}>
                            <LocalizationProvider dateAdapter={AdapterDayjs}>
                                <DemoContainer components={['DatePicker']}>
                                    <DatePicker label="Start Date" name="startDate" defaultValue={date} />
                                </DemoContainer>
                            </LocalizationProvider>
                            <LocalizationProvider dateAdapter={AdapterDayjs}>
                                <DemoContainer components={['DatePicker']}>
                                    <DatePicker label="End Date" name="endDate" defaultValue={date} />
                                </DemoContainer>
                            </LocalizationProvider>
                            {/*<TextField*/}
                            {/*    margin="normal"*/}
                            {/*    required*/}
                            {/*    fullWidth*/}
                            {/*    select*/}
                            {/*    name="activityType"*/}
                            {/*    label="Activity Type"*/}
                            {/*    defaultValue="other"*/}
                            {/*    id="activityType"*/}
                            {/*>*/}
                            {/*    {types.map((option) => (*/}
                            {/*        <MenuItem key={option.value} value={option.value}>*/}
                            {/*            {option.label}*/}
                            {/*        </MenuItem>*/}
                            {/*    ))}*/}
                            {/*</TextField>*/}
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                sx={{ mt: 3, mb: 3 }}
                            >
                                View Workouts
                            </Button>
                            {(localStorage.getItem("isAthlete") === 'false') && (
                                <Container>
                                    <Divider>OR</Divider>
                                    <Button
                                        href="/create-workout"
                                        fullWidth
                                        variant="contained"
                                        sx={{ mt: 3, mb: 2, marginBottom: 5 }}
                                    >
                                        Create New Workout
                                        </Button>
                                </Container>
                            )}
                        </Box>
                    </Box>
                </Container>
                <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
                    {workouts.map((workout) => (
                        <Grid xs={2} sm={4} md={4} key={workout.workoutID}>
                            <Item>
                                <Typography>{workout.title}</Typography>
                                <Typography>Description:{workout.description}</Typography>
                                <Typography>{workout.assignedDate}</Typography>
                            </Item>
                        </Grid>
                    ))}
                </Grid>
            </Box>
        </Box>
    );
}