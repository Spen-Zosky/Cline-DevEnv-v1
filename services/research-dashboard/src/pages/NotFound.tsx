import React from 'react';
import { Box, Typography, Button, Paper } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const NotFound: React.FC = () => {
  const navigate = useNavigate();

  return (
    <Box
      sx={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
      }}
    >
      <Paper
        elevation={3}
        sx={{
          p: 4,
          maxWidth: 500,
          textAlign: 'center',
        }}
      >
        <Typography variant="h1" color="primary" sx={{ fontSize: '6rem', fontWeight: 'bold' }}>
          404
        </Typography>
        <Typography variant="h5" gutterBottom>
          Page Not Found
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          The page you are looking for does not exist or has been moved.
        </Typography>
        <Button
          variant="contained"
          color="primary"
          onClick={() => navigate('/dashboard')}
          sx={{ mt: 2 }}
        >
          Go to Dashboard
        </Button>
      </Paper>
    </Box>
  );
};

export default NotFound;
