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

import axios from 'axios';
export default function CreateAccount() {
    const [loading, setLoading] = useState(false);

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        const isCoach = data.get('accountTypeRadio') === 'coach'
        const isAthlete = data.get('accountTypeRadio') === 'athlete'
        function redirect() {
            console.log("SUCCESS")
            console.log(isAthlete)
            console.log(isCoach)
            console.log(localStorage.getItem("userID"))
            if (isAthlete) {
                localStorage.setItem("athlete", true);
                console.log("athlete")
                window.location.href = "/athlete-setup"
            }
            if (isCoach) {
                localStorage.setItem("athlete", false);
                console.log("coach")
                window.location.href = "/team-setup"
            }
        }

        axios.post("http://127.0.0.1:8000/external/newUser", null, {
            params: {
                username: data.get('username'),
                password: data.get('password'),
                email: data.get('email'),
                isCoach: String(isCoach).charAt(0).toUpperCase() + String(isCoach).slice(1),
                isAthlete: String(isAthlete).charAt(0).toUpperCase() + String(isAthlete).slice(1),
                first_name: data.get('firstName'),
                last_name: data.get('lastName')
            }
        })
            .then((response) => {
                localStorage.setItem("userID", response.data.userId);
                console.log(response)
                if (response.status === 200) {
                    redirect();
                }
            }).catch(err => {
                console.log(err);
            });
        console.log({
            username: data.get('username'),
            password: data.get('password'),
            email: data.get('email'),
            isCoach: String(isCoach).charAt(0).toUpperCase() + String(isCoach).slice(1),
            isAthlete: String(isAthlete).charAt(0).toUpperCase() + String(isAthlete).slice(1),
            first_name: data.get('firstName'),
            last_name: data.get('lastName'),
            userId: parseInt(localStorage.getItem("userID"))
        });
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
                    Create Account
                </Typography>
                <Box component="form" noValidate onSubmit={handleSubmit} autoComplete="off" sx={{ mt: 3, width: 300 }}>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="username"
                        label="Username"
                        name="username"
                        size="small"
                    />
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="password"
                        label="Password"
                        type="password"
                        id="password"
                        size="small"
                    />
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="firstName"
                        label="First Name"
                        name="firstName"
                        size="small"
                    />
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="lastName"
                        label="Last Name"
                        name="lastName"
                        size="small"
                    />
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="email"
                        label="Email"
                        name="email"
                        size="small"
                    />
                    <FormLabel id="accountType" >Account</FormLabel>
                    <RadioGroup
                        row
                        aria-labelledby="accountType"
                        name="accountTypeRadio"
                    >
                        <FormControlLabel value="athlete" control={<Radio size="small" />} label="Athlete" />
                        <FormControlLabel value="coach" control={<Radio size="small" />} label="Coach" />
                    </RadioGroup>
                    <Button
                        onClick={() => setLoading(true)}
                        type="submit"
                        fullWidth
                        variant="contained"
                        sx={{ mt: 3, mb: 2, marginBottom: 5 }}
                    >
                        Continue
                    </Button>
                </Box>
            </Box>
        </Container>
    );
}