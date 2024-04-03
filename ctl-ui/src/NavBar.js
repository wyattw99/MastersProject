import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import { createTheme, ThemeProvider } from '@mui/material/styles';

import loginImage from "./mainlogin.png"
export default function NavBar() {
    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static" color="dark">
                <Toolbar>
                    {(window.location.pathname !== "/" && window.location.pathname !== "/create-account" && window.location.pathname !== "/athlete-setup") && (
                        <IconButton
                            size="large"
                            edge="start"
                            aria-label="menu"
                            color="light"
                            sx={{ mr: 2 }}
                        >
                            <MenuIcon />
                        </IconButton>
                    )}
                    <Typography variant="h6" component="div" sx={{ flexGrow: 1}}>
                        Collaborative Training Log
                    </Typography>
                    {window.location.pathname !== "/" && (
                        <Button
                            href="/"
                        >
                            Logout
                        </Button>
                    )}
                </Toolbar>
            </AppBar>
            {(window.location.pathname === "/" || window.location.pathname === "/create-account" || window.location.pathname === "/athlete-setup") && (
                <Box component="div"
                    sx={{
                        position: 'absolute',
                        width: '100%',
                        height: '100%',
                        backgroundImage: `url(${loginImage})`,
                        backgroundPosition: 'center',
                        backgroundSize: 'cover',
                        backgroundRepeat: 'no-repeat'
                    }}
                />
            )}
        </Box>
    );
}