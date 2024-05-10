import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListSubheader from '@mui/material/ListSubheader';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import PeopleIcon from '@mui/icons-material/People';
import BarChartIcon from '@mui/icons-material/BarChart';
import LayersIcon from '@mui/icons-material/Layers';
import AssignmentIcon from '@mui/icons-material/Assignment';
import DirectionsRunIcon from '@mui/icons-material/DirectionsRun';

export const mainListItems = (
    <React.Fragment>
        <ListItemButton href="/dashboard">
            <ListItemIcon>
                <DashboardIcon />
            </ListItemIcon>
            <ListItemText primary="Dashboard" />
        </ListItemButton>
        {localStorage.getItem("teamID") && localStorage.getItem("teamID") !== 'null' ?
            <ListItemButton href="/team-page">
                <ListItemIcon>
                    <PeopleIcon />
                </ListItemIcon>
                <ListItemText primary={localStorage.getItem("teamName")} />
            </ListItemButton>
            :
            <ListItemButton href="/join-team">
                <ListItemIcon>
                    <PeopleIcon />
                </ListItemIcon>
                <ListItemText primary="Join a Team" />
            </ListItemButton>
        }
    </React.Fragment>
);

export const secondaryListItems = (
    <React.Fragment>
        <ListItemButton href="/workout-view">
            <ListItemIcon>
                <AssignmentIcon />
            </ListItemIcon>
            <ListItemText primary="Workouts" />
        </ListItemButton>
        {(localStorage.getItem("isAthlete") === 'true') && (
            <ListItemButton href="/activity-view">
                <ListItemIcon>
                    <DirectionsRunIcon />
                </ListItemIcon>
                <ListItemText primary="Activities" />
            </ListItemButton>
        )}
        <ListItemButton href="/stats">
            <ListItemIcon>
                <BarChartIcon />
            </ListItemIcon>
            <ListItemText primary="Stats" />
        </ListItemButton>
    </React.Fragment>
);
