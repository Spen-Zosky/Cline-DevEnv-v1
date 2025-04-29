import React, { useState } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Chip,
  Divider,
  LinearProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Tabs,
  Tab,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  PlayArrow as StartIcon,
  Stop as StopIcon,
  Replay as RestartIcon,
  Info as InfoIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';

interface Service {
  id: string;
  name: string;
  description: string;
  status: string;
  category: string;
  version?: string;
  lastUpdated?: string;
  metrics?: {
    cpu?: number;
    memory?: number;
    requests?: number;
    errors?: number;
  };
}

interface ServiceCategory {
  id: string;
  name: string;
  description: string;
  services: string[];
}

// Mock API service - would be replaced with actual API calls
const fetchServices = async () => {
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 1000));
  
  // Mock data
  return {
    services: [
      {
        id: 'data-crawler',
        name: 'Data Crawler',
        description: 'Crawls websites and collects data',
        status: 'UP',
        category: 'data-collection',
        version: '1.2.0',
        lastUpdated: '2025-04-15T10:30:00Z',
        metrics: {
          cpu: 35,
          memory: 42,
          requests: 120,
          errors: 2,
        },
      },
      {
        id: 'data-scraper',
        name: 'Data Scraper',
        description: 'Scrapes structured data from websites',
        status: 'UP',
        category: 'data-collection',
        version: '1.1.5',
        lastUpdated: '2025-04-10T14:45:00Z',
        metrics: {
          cpu: 28,
          memory: 35,
          requests: 85,
          errors: 0,
        },
      },
      {
        id: 'data-preprocessor',
        name: 'Data Preprocessor',
        description: 'Preprocesses data for machine learning',
        status: 'UP',
        category: 'data-processing',
        version: '2.0.1',
        lastUpdated: '2025-04-20T09:15:00Z',
        metrics: {
          cpu: 45,
          memory: 60,
          requests: 50,
          errors: 1,
        },
      },
      {
        id: 'data-transformer',
        name: 'Data Transformer',
        description: 'Transforms data into different formats',
        status: 'DOWN',
        category: 'data-processing',
        version: '1.3.2',
        lastUpdated: '2025-04-05T11:20:00Z',
        metrics: {
          cpu: 0,
          memory: 0,
          requests: 0,
          errors: 0,
        },
      },
      {
        id: 'ml-trainer',
        name: 'ML Trainer',
        description: 'Trains machine learning models',
        status: 'UP',
        category: 'ml-framework',
        version: '3.1.0',
        lastUpdated: '2025-04-25T16:10:00Z',
        metrics: {
          cpu: 85,
          memory: 75,
          requests: 10,
          errors: 0,
        },
      },
      {
        id: 'ml-evaluator',
        name: 'ML Evaluator',
        description: 'Evaluates machine learning models',
        status: 'WARNING',
        category: 'ml-framework',
        version: '2.2.1',
        lastUpdated: '2025-04-18T13:40:00Z',
        metrics: {
          cpu: 65,
          memory: 70,
          requests: 15,
          errors: 3,
        },
      },
      {
        id: 'web-generator',
        name: 'Web Generator',
        description: 'Generates websites and web applications',
        status: 'UP',
        category: 'web-generator',
        version: '1.0.0',
        lastUpdated: '2025-04-22T10:00:00Z',
        metrics: {
          cpu: 25,
          memory: 40,
          requests: 5,
          errors: 0,
        },
      },
    ],
    categories: [
      {
        id: 'data-collection',
        name: 'Data Collection',
        description: 'Services for collecting data from various sources',
        services: ['data-crawler', 'data-scraper'],
      },
      {
        id: 'data-processing',
        name: 'Data Processing',
        description: 'Services for processing and transforming data',
        services: ['data-preprocessor', 'data-transformer'],
      },
      {
        id: 'ml-framework',
        name: 'Machine Learning Framework',
        description: 'Services for training and evaluating machine learning models',
        services: ['ml-trainer', 'ml-evaluator'],
      },
      {
        id: 'web-generator',
        name: 'Web Generator',
        description: 'Services for generating websites and web applications',
        services: ['web-generator'],
      },
    ],
  };
};

const Services: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [selectedService, setSelectedService] = useState<Service | null>(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [actionDialogOpen, setActionDialogOpen] = useState(false);
  const [actionType, setActionType] = useState<'start' | 'stop' | 'restart' | null>(null);

  const { data, isLoading, refetch } = useQuery({
    queryKey: ['services'],
    queryFn: fetchServices,
  });

  const handleCategoryChange = (_event: React.SyntheticEvent, newValue: string | null) => {
    setSelectedCategory(newValue);
  };

  const handleServiceClick = (service: Service) => {
    setSelectedService(service);
    setDialogOpen(true);
  };

  const handleCloseDialog = () => {
    setDialogOpen(false);
  };

  const handleServiceAction = (service: Service, action: 'start' | 'stop' | 'restart') => {
    setSelectedService(service);
    setActionType(action);
    setActionDialogOpen(true);
  };

  const handleConfirmAction = () => {
    // In a real implementation, this would call an API to perform the action
    console.log(`Performing ${actionType} on service ${selectedService?.id}`);
    setActionDialogOpen(false);
    
    // Simulate a delay and then refetch the services
    setTimeout(() => {
      refetch();
    }, 1000);
  };

  const handleCancelAction = () => {
    setActionDialogOpen(false);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'UP':
        return 'success';
      case 'DOWN':
        return 'error';
      case 'WARNING':
        return 'warning';
      default:
        return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'UP':
        return <CheckCircleIcon color="success" />;
      case 'DOWN':
        return <ErrorIcon color="error" />;
      case 'WARNING':
        return <WarningIcon color="warning" />;
      default:
        return null;
    }
  };

  const filteredServices = data?.services.filter(
    (service) => !selectedCategory || service.category === selectedCategory
  );

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Services
        </Typography>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={() => refetch()}
        >
          Refresh
        </Button>
      </Box>

      {isLoading ? (
        <LinearProgress />
      ) : data ? (
        <>
          <Paper sx={{ mb: 3 }}>
            <Tabs
              value={selectedCategory}
              onChange={handleCategoryChange}
              indicatorColor="primary"
              textColor="primary"
              variant="scrollable"
              scrollButtons="auto"
              sx={{ px: 2 }}
            >
              <Tab label="All Services" value={null} />
              {data.categories.map((category: any) => (
                <Tab key={category.id} label={category.name} value={category.id} />
              ))}
            </Tabs>
          </Paper>

          <Grid container spacing={3}>
            {filteredServices?.map((service: Service) => (
              <Grid item xs={12} sm={6} md={4} key={service.id}>
                <Card>
                  <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                      <Typography variant="h6" component="div">
                        {service.name}
                      </Typography>
                      <Chip
                        icon={getStatusIcon(service.status)}
                        label={service.status}
                        color={getStatusColor(service.status)}
                        size="small"
                      />
                    </Box>
                    <Typography color="text.secondary" sx={{ mb: 1.5 }}>
                      {service.description}
                    </Typography>
                    <Typography variant="body2" sx={{ mb: 1 }}>
                      Version: {service.version}
                    </Typography>
                    <Typography variant="body2" sx={{ mb: 2 }}>
                      Last Updated: {new Date(service.lastUpdated || '').toLocaleString()}
                    </Typography>
                    
                    {service.metrics && (
                      <Box sx={{ mt: 2 }}>
                        <Typography variant="subtitle2" gutterBottom>
                          Resource Usage
                        </Typography>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          <Typography variant="body2" sx={{ minWidth: 100 }}>
                            CPU:
                          </Typography>
                          <LinearProgress
                            variant="determinate"
                            value={service.metrics.cpu || 0}
                            color={service.metrics.cpu && service.metrics.cpu > 80 ? 'error' : 'primary'}
                            sx={{ flexGrow: 1, mr: 1 }}
                          />
                          <Typography variant="body2">
                            {service.metrics.cpu}%
                          </Typography>
                        </Box>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <Typography variant="body2" sx={{ minWidth: 100 }}>
                            Memory:
                          </Typography>
                          <LinearProgress
                            variant="determinate"
                            value={service.metrics.memory || 0}
                            color={service.metrics.memory && service.metrics.memory > 80 ? 'error' : 'primary'}
                            sx={{ flexGrow: 1, mr: 1 }}
                          />
                          <Typography variant="body2">
                            {service.metrics.memory}%
                          </Typography>
                        </Box>
                      </Box>
                    )}
                  </CardContent>
                  <Divider />
                  <CardActions>
                    <Button
                      size="small"
                      startIcon={<InfoIcon />}
                      onClick={() => handleServiceClick(service)}
                    >
                      Details
                    </Button>
                    {service.status === 'DOWN' && (
                      <Button
                        size="small"
                        startIcon={<StartIcon />}
                        color="success"
                        onClick={() => handleServiceAction(service, 'start')}
                      >
                        Start
                      </Button>
                    )}
                    {service.status === 'UP' && (
                      <Button
                        size="small"
                        startIcon={<StopIcon />}
                        color="error"
                        onClick={() => handleServiceAction(service, 'stop')}
                      >
                        Stop
                      </Button>
                    )}
                    <Button
                      size="small"
                      startIcon={<RestartIcon />}
                      color="warning"
                      onClick={() => handleServiceAction(service, 'restart')}
                    >
                      Restart
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>

          {/* Service Details Dialog */}
          <Dialog open={dialogOpen} onClose={handleCloseDialog} maxWidth="md" fullWidth>
            {selectedService && (
              <>
                <DialogTitle>
                  <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                    <Typography variant="h6">{selectedService.name} Details</Typography>
                    <Chip
                      icon={getStatusIcon(selectedService.status)}
                      label={selectedService.status}
                      color={getStatusColor(selectedService.status)}
                    />
                  </Box>
                </DialogTitle>
                <DialogContent dividers>
                  <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle1" gutterBottom>
                        General Information
                      </Typography>
                      <Box sx={{ mb: 2 }}>
                        <Typography variant="body2" gutterBottom>
                          <strong>ID:</strong> {selectedService.id}
                        </Typography>
                        <Typography variant="body2" gutterBottom>
                          <strong>Description:</strong> {selectedService.description}
                        </Typography>
                        <Typography variant="body2" gutterBottom>
                          <strong>Category:</strong> {
                            data.categories.find((c: any) => c.id === selectedService.category)?.name
                          }
                        </Typography>
                        <Typography variant="body2" gutterBottom>
                          <strong>Version:</strong> {selectedService.version}
                        </Typography>
                        <Typography variant="body2" gutterBottom>
                          <strong>Last Updated:</strong> {new Date(selectedService.lastUpdated || '').toLocaleString()}
                        </Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Typography variant="subtitle1" gutterBottom>
                        Metrics
                      </Typography>
                      {selectedService.metrics && (
                        <Box>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <Typography variant="body2" sx={{ minWidth: 150 }}>
                              CPU Usage:
                            </Typography>
                            <LinearProgress
                              variant="determinate"
                              value={selectedService.metrics.cpu || 0}
                              color={selectedService.metrics.cpu && selectedService.metrics.cpu > 80 ? 'error' : 'primary'}
                              sx={{ flexGrow: 1, mr: 1 }}
                            />
                            <Typography variant="body2">
                              {selectedService.metrics.cpu}%
                            </Typography>
                          </Box>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <Typography variant="body2" sx={{ minWidth: 150 }}>
                              Memory Usage:
                            </Typography>
                            <LinearProgress
                              variant="determinate"
                              value={selectedService.metrics.memory || 0}
                              color={selectedService.metrics.memory && selectedService.metrics.memory > 80 ? 'error' : 'primary'}
                              sx={{ flexGrow: 1, mr: 1 }}
                            />
                            <Typography variant="body2">
                              {selectedService.metrics.memory}%
                            </Typography>
                          </Box>
                          <Typography variant="body2" gutterBottom>
                            <strong>Requests:</strong> {selectedService.metrics.requests} per minute
                          </Typography>
                          <Typography variant="body2" gutterBottom>
                            <strong>Errors:</strong> {selectedService.metrics.errors} in the last hour
                          </Typography>
                        </Box>
                      )}
                    </Grid>
                  </Grid>
                </DialogContent>
                <DialogActions>
                  <Button onClick={handleCloseDialog}>Close</Button>
                  {selectedService.status === 'DOWN' && (
                    <Button
                      startIcon={<StartIcon />}
                      color="success"
                      onClick={() => {
                        handleCloseDialog();
                        handleServiceAction(selectedService, 'start');
                      }}
                    >
                      Start
                    </Button>
                  )}
                  {selectedService.status === 'UP' && (
                    <Button
                      startIcon={<StopIcon />}
                      color="error"
                      onClick={() => {
                        handleCloseDialog();
                        handleServiceAction(selectedService, 'stop');
                      }}
                    >
                      Stop
                    </Button>
                  )}
                  <Button
                    startIcon={<RestartIcon />}
                    color="warning"
                    onClick={() => {
                      handleCloseDialog();
                      handleServiceAction(selectedService, 'restart');
                    }}
                  >
                    Restart
                  </Button>
                </DialogActions>
              </>
            )}
          </Dialog>

          {/* Action Confirmation Dialog */}
          <Dialog open={actionDialogOpen} onClose={handleCancelAction}>
            <DialogTitle>Confirm Action</DialogTitle>
            <DialogContent>
              <DialogContentText>
                {actionType === 'start' && `Are you sure you want to start ${selectedService?.name}?`}
                {actionType === 'stop' && `Are you sure you want to stop ${selectedService?.name}?`}
                {actionType === 'restart' && `Are you sure you want to restart ${selectedService?.name}?`}
              </DialogContentText>
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCancelAction}>Cancel</Button>
              <Button onClick={handleConfirmAction} color="primary" autoFocus>
                Confirm
              </Button>
            </DialogActions>
          </Dialog>
        </>
      ) : (
        <Typography color="error">Failed to load services</Typography>
      )}
    </Box>
  );
};

export default Services;
