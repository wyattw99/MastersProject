import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';

import axios from 'axios';
import Cookies from 'js-cookie';

axios.defaults.withCredentials = true
export default function LogIn() {
    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

        function getCoach() {
            axios.get(`http://127.0.0.1:8000/external/getCoach/${localStorage.getItem("coachID")}/`, {
                'withCredentials': 'true',
            })
                .then((response) => {
                    console.log(response)
                    if (response.status === 200) {
                        console.log(response);
                        localStorage.setItem("teamID", response.data.teamID)
                        getTeamName();
                    }
                }).catch(err => {
                    console.log(err);
                });
        }

        function getAthlete() {
            axios.get(`http://127.0.0.1:8000/external/getAthlete/${localStorage.getItem("athleteID")}/`, {
                'withCredentials': 'true',
            })
                .then((response) => {
                    console.log(response);
                    if (response.status === 200) {
                        localStorage.setItem("teamID", response.data.teamID)
                        getTeamName();
                    }
                }).catch(err => {
                    console.log(err);
                });
        }

        function getTeamName() {
            if (localStorage.getItem("teamID") !== 'null' && localStorage.getItem("teamID") !== 'undefined') {
                console.log(localStorage.getItem("teamID"));
                axios.get(`http://127.0.0.1:8000/external/getTeamId/${localStorage.getItem("teamID")}/`)
                    .then((response) => {
                        console.log(response)
                        if (response.status === 200) {
                            localStorage.setItem("teamName", response.data.teamName);
                        }
                        else {
                            localStorage.setItem("teamID", null);
                            localStorage.setItem("teamName", null);
                        }
                        window.location.href = "/dashboard";
                    }).catch(err => {
                        console.log(err);
                        localStorage.setItem("teamID", null);
                        localStorage.setItem("teamName", null);
                    });
            }
            else {
                localStorage.setItem("teamID", null);
                localStorage.setItem("teamName", null);
                window.location.href = "/dashboard";
            }
        }

        axios.post("http://127.0.0.1:8000/external/login", null, {
            withCredentials: true,
            params: {
                username: data.get('username'),
                password: data.get('password')
            }
        })
            .then((response) => {
                console.log(response);
                localStorage.setItem("userID", response.data.userId);
                localStorage.setItem("athleteID", response.data.athleteId);
                localStorage.setItem("coachID", response.data.coachId);
                localStorage.setItem("csrfToken", Cookies.get('csrftoken'))
                if (localStorage.getItem("athleteID") === 'undefined') {
                    localStorage.setItem("athleteID", null);
                    localStorage.setItem("isAthlete", false);
                    getCoach();
                }
                if (localStorage.getItem("coachID") === 'undefined') {
                    localStorage.setItem("coachID", null);
                    localStorage.setItem("isAthlete", true)
                    getAthlete();
                }
            }).catch(err => {
                console.log(err);
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
                    Log In
                </Typography>
                <Box component="form" onSubmit={handleSubmit} noValidate autoComplete="off" sx={{ mt: 1, width: 300 }}>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        id="username"
                        label="Username"
                        name="username"
                    />
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="password"
                        label="Password"
                        type="password"
                        id="password"
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="light"

                        sx={{
                            mt: 3, mb: 2}}
                    >
                        Log In
                    </Button>
                    <Divider>OR</Divider>
                    <Button
                        fullWidth
                        variant="contained"
                        href="/create-account"
                        sx={{ mt: 3, mb: 2, marginBottom: 5}}
                    >
                        Create Account
                    </Button>
                </Box>
            </Box>
        </Container>
    );
}