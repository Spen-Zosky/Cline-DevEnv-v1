import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Box } from '@mui/material';

// Layout components
import MainLayout from './components/layouts/MainLayout';

// Pages
import Dashboard from './pages/Dashboard';
import Services from './pages/Services'; // Import the Services component
import DataCollection from './pages/DataCollection';
import DataProcessing from './pages/DataProcessing';
import MLFramework from './pages/MLFramework';
import SystemMonitor from './pages/SystemMonitor';
import Settings from './pages/Settings';
import NotFound from './pages/NotFound'; // Ensure this file exists in the specified path

const App: React.FC = () => {
  return (
    <Box sx={{ display: 'flex', height: '100vh' }}>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="services" element={<Services />} />
          <Route path="data-collection" element={<DataCollection />} />
          <Route path="data-processing" element={<DataProcessing />} />
          <Route path="ml-framework" element={<MLFramework />} />
          <Route path="system" element={<SystemMonitor />} />
          <Route path="settings" element={<Settings />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </Box>
  );
};

export default App;
