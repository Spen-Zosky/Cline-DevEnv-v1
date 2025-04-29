import React from 'react';
import { Box, Typography, Paper } from '@mui/material';

const DataCollection: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Data Collection
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Typography variant="body1">
          This page is under development. Data Collection functionality will be implemented soon.
        </Typography>
      </Paper>
    </Box>
  );
};

export default DataCollection;
