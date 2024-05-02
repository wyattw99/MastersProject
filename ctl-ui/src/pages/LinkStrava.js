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
export default function LinkStrava() {
    //const [loading, setLoading] = useState(false);

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

        axios.post("http://127.0.0.1:8000/external/", null, {
            params: {
                item: data.get('item'),
            }
        })
            .then((response) => {
                console.log(response)
                if (response.status === 200) {
                    localStorage.setItem("stravaToken", response.data.stravaToken);
                }
            }).catch(err => {
                console.log(err);
            });
        console.log({
            item: data.get('item'),
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
                            Link Strava Account
                        </Typography>
                        <Box component="form" noValidate onSubmit={handleSubmit} autoComplete="off" sx={{ mt: 3, width: 300 }}>
                            <TextField
                                margin="normal"
                                required
                                fullWidth
                                id="item"
                                label="Item"
                                name="item"
                                size="small"
                            />
                            <Button
                                //onClick={() => setLoading(true)}
                                type="submit"
                                fullWidth
                                variant="contained"
                                sx={{ mt: 3 }}
                            >
                                Link
                            </Button>
                            <Typography variant="subtitle1" sx={{ marginTop: 1, marginBottom: 5, textAlign: "center" }}>
                                (You will be redirected to Strava)
                            </Typography>
                        </Box>
                    </Box>
                </Container>
            </Box>
        </Box>
    );
}