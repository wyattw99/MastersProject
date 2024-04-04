import * as React from 'react';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import MenuItem from '@mui/material/MenuItem';
import Checkbox from '@mui/material/Checkbox';
import FormControlLabel from '@mui/material/FormControlLabel';
import dayjs from 'dayjs';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

const date = dayjs();

const schoolYears = [
    {
        value: 'N/A',
        label: '-',
    },
    {
        value: '6th Grade',
        label: '6',
    },
    {
        value: '7th Grade',
        label: '7',
    },
    {
        value: '8th Grade',
        label: '8',
    },
    {
        value: '9th Grade',
        label: '9',
    },
    {
        value: '10th Grade',
        label: '10',
    },
    {
        value: '11th Grade',
        label: '11',
    },
    {
        value: '12th Grade',
        label: '12',
    },
    {
        value: 'College Freshman',
        label: 'Freshman',
    },
    {
        value: 'College Sophomore',
        label: 'Sophomore',
    },
    {
        value: 'College Junior',
        label: 'Junior',
    },
    {
        value: 'College Senior',
        label: 'Senior',
    },
    {
        value: 'College Super Senior',
        label: 'Super Senior',
    },
    {
        value: 'Grad Student',
        label: 'Grad Student',
    },
];
export default function AthleteSetup() {
    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        console.log({
            username: data.get('username'),
            password: data.get('password'),
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
                    Athlete Account Setup
                </Typography>
                <Box component="form" onSubmit={handleSubmit} noValidate autoComplete="off" sx={{ mt: 1, width: 300 }}>
                    <LocalizationProvider dateAdapter={AdapterDayjs}>
                        <DemoContainer components={['DatePicker']}>
                            <DatePicker label="Birthday" defaultValue={date} />
                        </DemoContainer>
                    </LocalizationProvider>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        select
                        name="schoolYear"
                        label="Year in School"
                        defaultValue="N/A"
                        id="schoolYear"
                    >
                        {schoolYears.map((option) => (
                            <MenuItem key={option.value} value={option.value}>
                                {option.label}
                            </MenuItem>
                        ))}
                    </TextField>
                    <FormControlLabel
                        value="stravaLink"
                        control={<Checkbox />}
                        label="Link Strava account now? (You can do this later!)"
                        labelPlacement="end"
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        color="light"
                        href="/athlete-setup"
                        sx={{ mt: 3, mb: 2, marginBottom: 5 }}
                    >
                        Finish
                    </Button>
                </Box>
            </Box>
        </Container>
    );
}