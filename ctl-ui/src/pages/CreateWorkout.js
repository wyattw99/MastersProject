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

import dayjs from 'dayjs';
import axios from 'axios';

const date = dayjs();
export default function CreateWorkout() {
    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        function redirect() {
            console.log("SUCCESS")
        }

        axios.post("http://127.0.0.1:8000/external/newWorkout", null, {
            headers: {
                'X-CSRFToken': localStorage.getItem("csrfToken"),
            },
            params: {
                coachID: localStorage.getItem("coachID"),
                description: data.get('description'),
                date: dayjs(data.get('date')).format("YYYY-MM-DD"),
                title: data.get('title')
            }
        })
            .then((response) => {
                console.log(response)
                if (response.status === 200) {
                    window.location.href = "/workout-view";
                }
            }).catch(err => {
                console.log(err);
            });
        console.log({
            coachID: localStorage.getItem("coachID"),
            description: data.get('description'),
            date: dayjs(data.get('date')).format("YYYY-MM-DD"),
            title: data.get('title')
        });
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
                            Create Workout
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
                            <Button
                                type="submit"
                                fullWidth
                                variant="contained"
                                sx={{ mt: 3, mb: 2, marginBottom: 5 }}
                            >
                                Create Workout
                            </Button>
                        </Box>
                    </Box>
                </Container>
            </Box>
        </Box>
    );
}