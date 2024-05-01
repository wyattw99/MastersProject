import React from 'react';
import './index.css';
import reportWebVitals from './reportWebVitals';
import ReactDOM from "react-dom";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Layout from "./Layout";
import Login from "./pages/Login";
import CreateAccount from "./pages/CreateAccount";
import AthleteSetup from "./pages/AthleteSetup";
import TeamSetup from "./pages/TeamSetup";
import Dashboard from "./pages/Dashboard";
import CreateWorkout from "./pages/CreateWorkout";
import CreateActivity from "./pages/CreateActivity";
import LinkStrava from "./pages/LinkStrava";

const { palette } = createTheme();
const { augmentColor } = palette;
const createColor = (mainColor) => augmentColor({ color: { main: mainColor } });
const theme = createTheme({
    palette: {
        mode: 'light',
        primary: createColor('#D7837A'),
        secondary: createColor('#CEB4D5'),
        dark: createColor('#322B34'),
        light: createColor('#F5F5F5'),
    }
});
export default function App() {
    return (
        <ThemeProvider theme={theme}>
            <BrowserRouter>
                <Routes>
                    <Route path="/" element={<Layout />}>
                        <Route index element={<Login />} />
                        <Route path="create-account" element={<CreateAccount />} />
                        <Route path="athlete-setup" element={<AthleteSetup />} />
                        <Route path="team-setup" element={<TeamSetup />} />
                        <Route path="dashboard" element={<Dashboard />} />
                        <Route path="create-workout" element={<CreateWorkout />} />
                        <Route path="create-activity" element={<CreateActivity />} />
                        <Route path="link-strava" element={<LinkStrava />} />
                    </Route>
                </Routes>
            </BrowserRouter>
        </ThemeProvider>
    );
}

ReactDOM.render(<App />, document.getElementById("root"));

//// If you want to start measuring performance in your app, pass a function
//// to log results (for example: reportWebVitals(console.log))
//// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
