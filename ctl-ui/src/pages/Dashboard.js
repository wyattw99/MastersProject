import * as React from 'react';
import { useState, useEffect } from "react";
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import MuiDrawer from '@mui/material/Drawer';
import Box from '@mui/material/Box';
import MuiAppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import List from '@mui/material/List';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import IconButton from '@mui/material/IconButton';
import Badge from '@mui/material/Badge';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Paper from '@mui/material/Paper';
import Link from '@mui/material/Link';
import MenuIcon from '@mui/icons-material/Menu';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import NotificationsIcon from '@mui/icons-material/Notifications';
import { mainListItems, secondaryListItems } from './components/listItems';
import Button from '@mui/material/Button';

import axios from "axios"

const drawerWidth = 240;

const AppBar = styled(MuiAppBar, {
    shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
    zIndex: theme.zIndex.drawer + 1,
    transition: theme.transitions.create(['width', 'margin'], {
        easing: theme.transitions.easing.sharp,
        duration: theme.transitions.duration.leavingScreen,
    }),
    ...(open && {
        marginLeft: drawerWidth,
        width: `calc(100% - ${drawerWidth}px)`,
        transition: theme.transitions.create(['width', 'margin'], {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.enteringScreen,
        }),
    }),
}));

const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
    ({ theme, open }) => ({
        '& .MuiDrawer-paper': {
            position: 'relative',
            whiteSpace: 'nowrap',
            width: drawerWidth,
            transition: theme.transitions.create('width', {
                easing: theme.transitions.easing.sharp,
                duration: theme.transitions.duration.enteringScreen,
            }),
            boxSizing: 'border-box',
            ...(!open && {
                overflowX: 'hidden',
                transition: theme.transitions.create('width', {
                    easing: theme.transitions.easing.sharp,
                    duration: theme.transitions.duration.leavingScreen,
                }),
                width: theme.spacing(7),
                [theme.breakpoints.up('sm')]: {
                    width: theme.spacing(9),
                },
            }),
        },
    }),
);

// TODO remove, this demo shouldn't need to reset the theme.
const defaultTheme = createTheme();
export default function Dashboard() {
    const [open, setOpen] = React.useState(true);
    const toggleDrawer = () => {
        setOpen(!open);
    };


    useEffect(() => {
        handleClick();
    }, []);

    function handleClick() {
        console.log(localStorage.getItem("userID"));
        axios.get(`http://127.0.0.1:8000/external/getUser/${localStorage.getItem("userID")}/`, {
            'withCredentials': 'true',
        })
        .then((response) => {
            console.log(response)
            if (response.status === 200) {
                console.log("SUCCESS");
                console.log(response.data.username)
            }
        }).catch(err => {
            console.log(err);
        });
    }

    return (
        <ThemeProvider theme={defaultTheme}>
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
                    <Toolbar />
                    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
                        <Typography variant="h2" align="center" > Dashboard </Typography>
                        {/*<Grid container spacing={3}>*/}
                        {/*    */}{/* Chart */}
                        {/*    <Grid item xs={12} md={8} lg={9}>*/}
                        {/*        <Paper*/}
                        {/*            sx={{*/}
                        {/*                p: 2,*/}
                        {/*                display: 'flex',*/}
                        {/*                flexDirection: 'column',*/}
                        {/*                height: 240,*/}
                        {/*            }}*/}
                        {/*        >*/}
                        {/*            <Chart />*/}
                        {/*        </Paper>*/}
                        {/*    </Grid>*/}
                        {/*    */}{/* */}
                        {/*    <Grid item xs={12} md={4} lg={3}>*/}
                        {/*        <Paper*/}
                        {/*            sx={{*/}
                        {/*                p: 2,*/}
                        {/*                display: 'flex',*/}
                        {/*                flexDirection: 'column',*/}
                        {/*                height: 240,*/}
                        {/*            }}*/}
                        {/*        >*/}
                        {/*            <Deposits />*/}
                        {/*        </Paper>*/}
                        {/*    </Grid>*/}
                        {/*    */}{/* */}
                        {/*    <Grid item xs={12}>*/}
                        {/*        <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>*/}
                        {/*            */}{/*<Orders />*/}
                        {/*            <Button*/}
                        {/*                onClick={handleClick}*/}
                        {/*                type="submit"*/}
                        {/*                fullWidth*/}
                        {/*                variant="contained"*/}
                        {/*                sx={{ mt: 3 }}*/}
                        {/*            >*/}
                        {/*                Test Token*/}
                        {/*            </Button>*/}
                        {/*        </Paper>*/}
                        {/*    </Grid>*/}
                        {/*</Grid>*/}
                    </Container>
                </Box>
            </Box>
        </ThemeProvider>
    );
}