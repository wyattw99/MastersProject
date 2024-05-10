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

export default function JoinTeam() {
    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

        function joinTeam() {
            axios.post(`http://127.0.0.1:8000/external/addToTeam/${localStorage.getItem("athleteID")}/`, null, {
                withCredentials: true,
                params: {
                    teamId: localStorage.getItem("teamID"),
                },
                headers: {
                   'X-CSRFToken': localStorage.getItem("csrfToken"),
                }
            })
                .then((response) => {
                    console.log(response);
                    window.location.href = "/team-page";
                }).catch(err => {
                    console.log(err);
                });
        }

        axios.get(`http://127.0.0.1:8000/external/getTeam/${data.get('joinTeam')}/`)
            .then((response) => {
                console.log(response)
                if (response.status === 200) {
                    localStorage.setItem("teamName", data.get('joinTeam'));
                    localStorage.setItem("teamID", response.data.teamId);
                    joinTeam();
                }
            }).catch(err => {
                console.log(err);
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
                            Team Setup
                        </Typography>
                        <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3, width: 300 }}>
                            <Typography variant="subtitle1" sx={{marginBottom: 2 }}>
                                Ask your coach for your team name. Team names are case-sensitive.
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
                                type="submit"
                                variant="contained"
                                sx={{ mt: 4, mb: 2, marginBottom: 5 }}
                            >
                                Select Team
                            </Button>
                        </Box>
                    </Box>
                </Container>
            </Box>
        </Box>
    );
}