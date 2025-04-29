import React from 'react';
import { Box, Typography, Paper, Divider, Button, Grid } from '@mui/material';

const Settings: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Settings
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h6" gutterBottom>
          Application Settings
        </Typography>
        <Divider sx={{ my: 2 }} />
        
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <Typography variant="body1">
              Dark Mode: Enabled
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body1">
              Notifications: Enabled
            </Typography>
          </Grid>
          <Grid item xs={12}>
            <Typography variant="body1">
              Analytics: Disabled
            </Typography>
          </Grid>
          
          <Grid item xs={12}>
            <Divider sx={{ my: 2 }} />
            <Typography variant="h6" gutterBottom>
              API Configuration
            </Typography>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Typography variant="body1">
              API Endpoint: https://api.example.com
            </Typography>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Typography variant="body1">
              API Key: ********
            </Typography>
          </Grid>
          
          <Grid item xs={12}>
            <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
              <Button variant="contained" color="primary">
                Save Settings
              </Button>
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default Settings;
