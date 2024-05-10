import * as React from 'react';
import { useState } from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Divider from '@mui/material/Divider';
import { styled, alpha } from '@mui/material/styles';
import InputBase from '@mui/material/InputBase';
import SearchIcon from '@mui/icons-material/Search';

import axios from "axios"

const Search = styled('div')(({ theme }) => ({
    position: 'relative',
    borderRadius: theme.shape.borderRadius,
    backgroundColor: alpha(theme.palette.common.white, 0.15),
    '&:hover': {
        backgroundColor: alpha(theme.palette.common.white, 0.25),
    },
    marginRight: theme.spacing(2),
    marginLeft: 0,
    width: '100%',
    [theme.breakpoints.up('sm')]: {
        marginLeft: theme.spacing(3),
        width: 'auto',
    },
}));

const SearchIconWrapper = styled('div')(({ theme }) => ({
    padding: theme.spacing(0, 2),
    height: '100%',
    position: 'absolute',
    pointerEvents: 'none',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
}));

const StyledInputBase = styled(InputBase)(({ theme }) => ({
    color: 'inherit',
    '& .MuiInputBase-input': {
        padding: theme.spacing(1, 1, 1, 0),
        // vertical padding + font size from searchIcon
        paddingLeft: `calc(1em + ${theme.spacing(4)})`,
        transition: theme.transitions.create('width'),
        width: '100%',
        [theme.breakpoints.up('md')]: {
            width: '20ch',
        },
    },
}));

export default function TeamSetup() {
    const [newTeam, setNewTeam] = useState(true);

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

        function redirect() {
            console.log("SUCCESS")
            console.log(localStorage.getItem("teamID"))
            console.log(localStorage.getItem("coachID"))
            localStorage.clear()
            window.location.href = "/"
        }
        function createCoach() {
            axios.post("http://127.0.0.1:8000/external/newCoach", null, {
                params: {
                    userId: localStorage.getItem("userID"),
                    teamId: localStorage.getItem("teamID")
                }
            })
                .then((response) => {
                    localStorage.setItem("coachID", response.data.coachId);
                    console.log(response)
                    if (response.status === 200) {
                        redirect();
                    }
                }).catch(err => {
                    console.log(err);
                });
        }

        if (newTeam) {
            axios.post("http://127.0.0.1:8000/external/newTeam", null, {
                params: {
                    teamName: data.get('teamName')
                }
            })
                .then((response) => {
                    console.log(response)
                    if (response.status === 200) {
                        localStorage.setItem("teamID", data.get('teamName'));
                        localStorage.setItem("teamID", response.data.teamId);
                        createCoach();
                    }
                }).catch(err => {
                    console.log(err);
                });
            console.log({
                newTeam: data.get('teamName')
            });
        }
        else {
            axios.get(`http://127.0.0.1:8000/external/getTeam/${data.get('joinTeam')}/`)
                .then((response) => {
                    console.log(response)
                    if (response.status === 200) {
                        localStorage.setItem("teamName", data.get('joinTeam'));
                        localStorage.setItem("teamID", response.data.teamId);
                        createCoach();
                    }
                }).catch(err => {
                    console.log(err);
                });
            console.log({
                joinTeam: data.get('joinTeam')
            });
        }
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
                    Team Setup
                </Typography>
                <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3, width: 300 }}>
                    <Typography component="h1" variant="h6">
                        Create New Team
                    </Typography>
                    <TextField
                        margin="normal"
                        fullWidth
                        id="teamName"
                        label="Team Name"
                        name="teamName"
                        autoComplete="off"
                        size="small"
                    />
                    <Button
                        fullWidth
                        type="submit"
                        variant="contained"
                        color="light"
                        sx={{ mt: 3, mb: 3}}
                    >
                        Create Team
                    </Button>
                    <Divider>OR</Divider>
                    <Typography component="h1" variant="h6" sx={{ marginTop: 2, marginBottom: 2 }}>
                        Join Existing Team
                    </Typography>
                    <Search>
                        <SearchIconWrapper>
                            <SearchIcon />
                        </SearchIconWrapper>
                        <StyledInputBase
                            placeholder="Search teams..."
                            inputProps={{ 'aria-label': 'search' }}
                            name="joinTeam"
                        />
                    </Search>
                    <Button
                        fullWidth
                        onClick={() => setNewTeam(false)}
                        type="submit"
                        variant="contained"
                        color="light"
                        sx={{ mt: 4, mb: 2, marginBottom: 5 }}
                    >
                        Select Team
                    </Button>
                </Box>
            </Box>
        </Container>
    );
}