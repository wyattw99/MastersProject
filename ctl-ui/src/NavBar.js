import * as React from 'react';
//import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import MuiAppBar from '@mui/material/AppBar';
import MuiDrawer from '@mui/material/Drawer';
import Drawer from '@mui/material/Drawer';
import { styled, createTheme, ThemeProvider } from '@mui/material/styles';
import Divider from '@mui/material/Divider';
import List from '@mui/material/List';
import Badge from '@mui/material/Badge';
import NotificationsIcon from '@mui/icons-material/Notifications';
import ChevronLeftIcon from '@mui/icons-material/ChevronLeft';
import { mainListItems, secondaryListItems } from './pages/components/listItems';

import loginImage from "./mainlogin.png"

const drawerWidth = 240;

//const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
//    ({ theme, open }) => ({
//        flexGrow: 1,
//        padding: theme.spacing(3),
//        transition: theme.transitions.create('margin', {
//            easing: theme.transitions.easing.sharp,
//            duration: theme.transitions.duration.leavingScreen,
//        }),
//        marginLeft: `-${drawerWidth}px`,
//        ...(open && {
//            transition: theme.transitions.create('margin', {
//                easing: theme.transitions.easing.easeOut,
//                duration: theme.transitions.duration.enteringScreen,
//            }),
//            marginLeft: 0,
//        }),
//    }),
//);

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

//const Drawer = styled(MuiDrawer, { shouldForwardProp: (prop) => prop !== 'open' })(
//    ({ theme, open }) => ({
//        '& .MuiDrawer-paper': {
//            position: 'relative',
//            whiteSpace: 'nowrap',
//            width: drawerWidth,
//            transition: theme.transitions.create('width', {
//                easing: theme.transitions.easing.sharp,
//                duration: theme.transitions.duration.enteringScreen,
//            }),
//            boxSizing: 'border-box',
//            ...(!open && {
//                overflowX: 'hidden',
//                transition: theme.transitions.create('width', {
//                    easing: theme.transitions.easing.sharp,
//                    duration: theme.transitions.duration.leavingScreen,
//                }),
//                width: theme.spacing(7),
//                [theme.breakpoints.up('sm')]: {
//                    width: theme.spacing(9),
//                },
//            }),
//        },
//    }),
//);

const DrawerHeader = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
    justifyContent: 'flex-end',
}));
export default function NavBar() {
    const [open, setOpen] = React.useState(false);
    const toggleDrawer = () => {
        setOpen(!open);
    };
    const closeDrawer = () => {
        setOpen(false)
    }

    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static" color="dark" open={open} >
                <Toolbar
                    sx={{
                        pr: '24px', // keep right padding when drawer closed
                    }}
                >
                    {(window.location.pathname !== "/" && window.location.pathname !== "/create-account" && window.location.pathname !== "/athlete-setup" && window.location.pathname !== "/team-setup") && (
                        <IconButton
                            edge="start"
                            color="inherit"
                            aria-label="open drawer"
                            onClick={toggleDrawer}
                            sx={{
                                marginRight: '36px',
                                ...(open && { display: 'none' }),
                            }}
                        >
                            <MenuIcon />
                        </IconButton>
                    )}
                    <Typography
                        component="h1"
                        variant="h6"
                        color="inherit"
                        noWrap
                        sx={{ flexGrow: 1 }}
                    >
                        Collaborative Training Log
                    </Typography>
                    <IconButton color="inherit">
                        <Badge badgeContent={4} color="secondary">
                            <NotificationsIcon />
                        </Badge>
                    </IconButton>
                            {window.location.pathname !== "/" && (
                                <Button
                                    href="/"
                                >
                                    Logout
                                </Button>
                            )}
                </Toolbar>
            </AppBar>
            {/*<Drawer open={open}>*/}
            {/*    <Toolbar*/}
            {/*        sx={{*/}
            {/*            display: 'flex',*/}
            {/*            alignItems: 'center',*/}
            {/*            justifyContent: 'flex-end',*/}
            {/*            px: [1],*/}
            {/*        }}*/}
            {/*    >*/}
            {/*        <IconButton onClick={toggleDrawer}>*/}
            {/*            <ChevronLeftIcon />*/}
            {/*        </IconButton>*/}
            {/*    </Toolbar>*/}
            <Drawer
                sx={{
                    width: drawerWidth,
                    flexShrink: 0,
                    '& .MuiDrawer-paper': {
                        width: drawerWidth,
                        boxSizing: 'border-box',
                    },
                }}
                variant="persistent"
                anchor="left"
                open={open}
            >
                <DrawerHeader>
                    <IconButton onClick={toggleDrawer}>
                        <ChevronLeftIcon />
                    </IconButton>
                </DrawerHeader>
                <Divider />
                <List component="nav">
                    {mainListItems}
                    <Divider sx={{ my: 1 }} />
                    {secondaryListItems}
                </List>
            </Drawer>
            {/*<AppBar position="static" color="dark">*/}
            {/*    <Toolbar>*/}
                    {/*{(window.location.pathname !== "/" && window.location.pathname !== "/create-account" && window.location.pathname !== "/athlete-setup" && window.location.pathname !== "/team-setup") && (*/}
                    {/*    <iconbutton*/}
                    {/*        size="large"*/}
                    {/*        edge="start"*/}
                    {/*        aria-label="menu"*/}
                    {/*        color="light"*/}
                    {/*        sx={{ mr: 2 }}*/}
                    {/*    >*/}
                    {/*        <menuicon />*/}
                    {/*    </iconbutton>*/}
                    {/*)}*/}
            {/*        <Typography variant="h6" component="div" sx={{ flexGrow: 1}}>*/}
            {/*            Collaborative Training Log*/}
            {/*        </Typography>*/}
            {/*        {window.location.pathname !== "/" && (*/}
            {/*            <Button*/}
            {/*                href="/"*/}
            {/*            >*/}
            {/*                Logout*/}
            {/*            </Button>*/}
            {/*        )}*/}
            {/*    </Toolbar>*/}
            {/*</AppBar>*/}
            {(window.location.pathname === "/" || window.location.pathname === "/create-account" || window.location.pathname === "/athlete-setup" || window.location.pathname === "/team-setup") && (
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