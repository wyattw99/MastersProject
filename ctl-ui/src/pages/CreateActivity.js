import * as React from 'react';
import { useState } from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormLabel from '@mui/material/FormLabel';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import MenuItem from '@mui/material/MenuItem';

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
export default function CreateActivity() {
    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

        var hasHeartRate = true;
        if (data.getAvgHeartrate !== '' && data.getMaxHeartrate !== '') {
            hasHeartRate = false;
        }

        console.log(localStorage.getItem("csrfToken"))
        console.log(dayjs(data.get('date')).format("YYYY-MM-DD hh:mm:ss.00000+00:00"))
        if (data.get('activityType') === "run") {
            axios.post(`http://127.0.0.1:8000/external/newActivity`, null, {
                withCredentials: true,
                params: {
                    athleteID: localStorage.getItem("athleteID"),
                    type: data.get("activityType"),
                    description: data.get('description'),
                    name: data.get('title'),
                    movingTime: data.get('movingTime'),
                    elapsedTime: data.get('elapsedTime'),
                    startDate: dayjs(data.get('date')).format("YYYY-MM-DD hh:mm:ss.00000+00:00"), //2024-04-15 03:26:03.262689+00:00
                    distance: data.get('distance'),
                    hasHeartrate: String(hasHeartRate).charAt(0).toUpperCase() + String(hasHeartRate).slice(1),
                    avgHeartrate: data.get('avgHeartrate'), // if hasHeartrate is true
                    maxHeartrate: data.get('maxHeartrate'), // if hasHeartrate is true
                    manual: 'True',
                    maxPace: data.get('maxSpeed'), // if run
                    averageCadence: data.get('avgCadence'), // if run
                },
                headers: {
                    'X-CSRFToken': localStorage.getItem("csrfToken"),
                }
            })
                .then((response) => {
                    console.log(response);
                    if (response.status === 200) {
                        window.location.href = "/activity-view";
                    }
                }).catch(err => {
                    console.log(err);
                });
        }
        else {
            axios.post(`http://127.0.0.1:8000/external/newActivity`, null, {
                withCredentials: true,
                params: {
                    athleteID: localStorage.getItem("athleteID"),
                    type: data.get("activityType"),
                    description: data.get('description'),
                    name: data.get('title'),
                    movingTime: data.get('movingTime'),
                    elapsedTime: data.get('elapsedTime'),
                    startDate: dayjs(data.get('date')).format("YYYY-MM-DD hh:mm:ss.00000+00:00"),
                    distance: data.get('distance'),
                    hasHeartrate: String(hasHeartRate).charAt(0).toUpperCase() + String(hasHeartRate).slice(1),
                    avgHeartrate: data.get('avgHeartrate'), // if hasHeartrate is true
                    maxHeartrate: data.get('maxHeartrate'), // if hasHeartrate is true
                    manual: 'True',
                    maxSpeed: data.get('maxSpeed') // if bike or swim or other
                },
                headers: {
                    'X-CSRFToken': localStorage.getItem("csrfToken"),
                }
            })
                .then((response) => {
                    console.log(response);
                    window.location.href = "/activity-view";
                }).catch(err => {
                    console.log(err);
                });
        }
    };

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
                            display: 'flex',
                            flexDirection: 'column',
                            alignItems: 'center',
                            opacity: 0.8,
                        }}
                    >
                        <Typography component="h1" variant="h5" sx={{ marginTop: 5 }}>
                            New Activity
                        </Typography>
                        <Box component="form" noValidate onSubmit={handleSubmit} autoComplete="off" sx={{ mt: 3, width: 300 }}>
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="title"
                                label="Title"
                                name="title"
                                size="small"
                            />
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                select
                                name="activityType"
                                label="Activity Type"
                                defaultValue="other"
                                id="activityType"
                            >
                                {types.map((option) => (
                                    <MenuItem key={option.value} value={option.value}>
                                        {option.label}
                                    </MenuItem>
                                ))}
                            </TextField>
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                name="description"
                                label="Description"
                                id="description"
                                size="small"
                                multiline
                                maxRows={4}
                            />
                            <LocalizationProvider dateAdapter={AdapterDayjs}>
                                <DemoContainer components={['DatePicker']}>
                                    <DatePicker label="Date" name="date" defaultValue={date} />
                                </DemoContainer>
                            </LocalizationProvider>
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="movingTime"
                                label="Moving Time (Seconds)"
                                name="movingTime"
                                size="small"
                            />
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="elapsedTime"
                                label="Elapsed Time (Seconds)"
                                name="elapsedTime"
                                size="small"
                            />
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="distance"
                                label="Distance (Meters)"
                                name="distance"
                                size="small"
                            />
                            <TextField
                                margin="normal"
                                fullWidth
                                id="avgHeartrate"
                                label="Average Heart Rate (bpm)"
                                name="avgHeartrate"
                                size="small"
                            />
                            <TextField
                                margin="normal"
                                fullWidth
                                id="maxHeartrate"
                                label="Max Heart Rate (bpm)"
                                name="maxHeartrate"
                                size="small"
                            />
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="maxSpeed"
                                label="Max Pace or Speed (meters/second)"
                                name="maxSpeed"
                                size="small"
                            />
                            <TextField
                                margin="normal"
                                fullWidth
                                id="avgCadence"
                                label="Average Cadence (For Runs)"
                                name="avgCadence"
                                size="small"
                            />
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                sx={{ mt: 3, mb: 2, marginBottom: 5 }}
                            >
                                Upload Activity
                            </Button>
                        </Box>
                    </Box>
                </Container>
            </Box>
        </Box>
    );
}