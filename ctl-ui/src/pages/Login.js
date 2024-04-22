import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';

import axios from 'axios';

export default function LogIn() {
    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        axios.post("http://127.0.0.1:8000/external/login", null, {
            params: {
                username: data.get('username'),
                password: data.get('password')
            }
        })
            .then((response) => {
                localStorage.setItem("csrfToken", response.data.csrf_token);
                window.location.href = "/dashboard"
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