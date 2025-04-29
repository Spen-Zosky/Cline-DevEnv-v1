import React, { useState, useEffect } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CardHeader,
  Divider,
  LinearProgress,
  Chip,
  Stack,
  Button,
  IconButton,
  Tooltip,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip as ChartTooltip,
  Legend,
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  ChartTooltip,
  Legend
);

// Mock API service - would be replaced with actual API calls
const fetchServiceStatus = async () => {
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 1000));
  
  // Mock data
  return {
    services: [
      { id: 'data-crawler', name: 'Data Crawler', status: 'UP', category: 'data-collection' },
      { id: 'data-scraper', name: 'Data Scraper', status: 'UP', category: 'data-collection' },
      { id: 'data-preprocessor', name: 'Data Preprocessor', status: 'UP', category: 'data-processing' },
      { id: 'data-transformer', name: 'Data Transformer', status: 'DOWN', category: 'data-processing' },
      { id: 'ml-trainer', name: 'ML Trainer', status: 'UP', category: 'ml-framework' },
      { id: 'ml-evaluator', name: 'ML Evaluator', status: 'WARNING', category: 'ml-framework' },
      { id: 'web-generator', name: 'Web Generator', status: 'UP', category: 'web-generator' },
    ],
  };
};

const fetchSystemMetrics = async () => {
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 1000));
  
  // Mock data
  return {
    cpu: {
      usage_percent: 45.2,
      temperature: 62.5,
    },
    memory: {
      usage_percent: 68.7,
      available_mb: 1254.3,
    },
    disk: {
      usage_percent: 72.1,
      available_gb: 58.4,
    },
    services: {
      'data-crawler': {
        requests_per_second: 5.2,
        average_response_time_ms: 120,
        error_rate: 0.02,
      },
      'data-scraper': {
        requests_per_second: 3.8,
        average_response_time_ms: 180,
        error_rate: 0.01,
      },
      'data-preprocessor': {
        jobs_processed: 42,
        average_processing_time_ms: 850,
        error_rate: 0.05,
      },
    },
    timestamp: Date.now(),
  };
};

const fetchRecentJobs = async () => {
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 1000));
  
  // Mock data
  return {
    jobs: [
      { id: 'job-1', name: 'Web Crawl - News Sites', status: 'COMPLETED', service: 'data-crawler', timestamp: '2025-04-28T12:30:45Z' },
      { id: 'job-2', name: 'Data Preprocessing - Dataset A', status: 'RUNNING', service: 'data-preprocessor', timestamp: '2025-04-28T13:15:22Z' },
      { id: 'job-3', name: 'Model Training - NLP Classifier', status: 'QUEUED', service: 'ml-trainer', timestamp: '2025-04-28T13:45:10Z' },
      { id: 'job-4', name: 'Data Scraping - E-commerce', status: 'FAILED', service: 'data-scraper', timestamp: '2025-04-28T11:20:33Z' },
      { id: 'job-5', name: 'Model Evaluation - Image Classifier', status: 'COMPLETED', service: 'ml-evaluator', timestamp: '2025-04-28T10:05:18Z' },
    ],
  };
};

const Dashboard: React.FC = () => {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [],
  });

  const { data: serviceStatus, isLoading: isLoadingServices, refetch: refetchServices } = useQuery({
    queryKey: ['serviceStatus'],
    queryFn: fetchServiceStatus,
  });

  const { data: systemMetrics, isLoading: isLoadingMetrics, refetch: refetchMetrics } = useQuery({
    queryKey: ['systemMetrics'],
    queryFn: fetchSystemMetrics,
  });

  const { data: recentJobs, isLoading: isLoadingJobs, refetch: refetchJobs } = useQuery({
    queryKey: ['recentJobs'],
    queryFn: fetchRecentJobs,
  });

  useEffect(() => {
    if (systemMetrics) {
      // Prepare chart data
      const labels = Array.from({ length: 24 }, (_, i) => `${i}:00`);
      
      // Mock historical data
      const cpuData = Array.from({ length: 24 }, () => Math.random() * 100);
      const memoryData = Array.from({ length: 24 }, () => Math.random() * 100);
      
      setChartData({
        labels,
        datasets: [
          {
            label: 'CPU Usage (%)',
            data: cpuData,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
          },
          {
            label: 'Memory Usage (%)',
            data: memoryData,
            borderColor: 'rgb(53, 162, 235)',
            backgroundColor: 'rgba(53, 162, 235, 0.5)',
          },
        ],
      });
    }
  }, [systemMetrics]);

  const handleRefresh = () => {
    refetchServices();
    refetchMetrics();
    refetchJobs();
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

  const getJobStatusColor = (status: string) => {
    switch (status) {
      case 'COMPLETED':
        return 'success';
      case 'RUNNING':
        return 'info';
      case 'QUEUED':
        return 'secondary';
      case 'FAILED':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Dashboard
        </Typography>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={handleRefresh}
        >
          Refresh
        </Button>
      </Box>

      <Grid container spacing={3}>
        {/* System Overview */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              System Overview
            </Typography>
            {isLoadingMetrics ? (
              <LinearProgress />
            ) : systemMetrics ? (
              <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                  <Card>
                    <CardContent>
                      <Typography color="text.secondary" gutterBottom>
                        CPU Usage
                      </Typography>
                      <Typography variant="h5" component="div">
                        {systemMetrics.cpu.usage_percent.toFixed(1)}%
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={systemMetrics.cpu.usage_percent}
                        color={systemMetrics.cpu.usage_percent > 80 ? 'error' : 'primary'}
                        sx={{ mt: 1 }}
                      />
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Card>
                    <CardContent>
                      <Typography color="text.secondary" gutterBottom>
                        Memory Usage
                      </Typography>
                      <Typography variant="h5" component="div">
                        {systemMetrics.memory.usage_percent.toFixed(1)}%
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={systemMetrics.memory.usage_percent}
                        color={systemMetrics.memory.usage_percent > 80 ? 'error' : 'primary'}
                        sx={{ mt: 1 }}
                      />
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Card>
                    <CardContent>
                      <Typography color="text.secondary" gutterBottom>
                        Disk Usage
                      </Typography>
                      <Typography variant="h5" component="div">
                        {systemMetrics.disk.usage_percent.toFixed(1)}%
                      </Typography>
                      <LinearProgress
                        variant="determinate"
                        value={systemMetrics.disk.usage_percent}
                        color={systemMetrics.disk.usage_percent > 80 ? 'error' : 'primary'}
                        sx={{ mt: 1 }}
                      />
                    </CardContent>
                  </Card>
                </Grid>
                <Grid item xs={12}>
                  <Box sx={{ height: 300 }}>
                    <Line
                      data={chartData}
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                          legend: {
                            position: 'top' as const,
                          },
                          title: {
                            display: true,
                            text: 'System Resource Usage (24h)',
                          },
                        },
                      }}
                    />
                  </Box>
                </Grid>
              </Grid>
            ) : (
              <Typography color="error">Failed to load system metrics</Typography>
            )}
          </Paper>
        </Grid>

        {/* Service Status */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Service Status
            </Typography>
            {isLoadingServices ? (
              <LinearProgress />
            ) : serviceStatus ? (
              <Stack spacing={1}>
                {serviceStatus.services.map((service: any) => (
                  <Box
                    key={service.id}
                    sx={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      p: 1,
                      borderRadius: 1,
                      bgcolor: 'background.default',
                    }}
                  >
                    <Box sx={{ display: 'flex', alignItems: 'center' }}>
                      {getStatusIcon(service.status)}
                      <Typography sx={{ ml: 1 }}>{service.name}</Typography>
                    </Box>
                    <Chip
                      label={service.status}
                      color={getStatusColor(service.status)}
                      size="small"
                    />
                  </Box>
                ))}
              </Stack>
            ) : (
              <Typography color="error">Failed to load service status</Typography>
            )}
          </Paper>
        </Grid>

        {/* Recent Jobs */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recent Jobs
            </Typography>
            {isLoadingJobs ? (
              <LinearProgress />
            ) : recentJobs ? (
              <Box sx={{ overflowX: 'auto' }}>
                <Box
                  sx={{
                    display: 'grid',
                    gridTemplateColumns: 'minmax(200px, 1fr) minmax(150px, 1fr) minmax(150px, 1fr) minmax(200px, 1fr)',
                    gap: 2,
                    p: 1,
                    fontWeight: 'bold',
                  }}
                >
                  <Typography>Job Name</Typography>
                  <Typography>Service</Typography>
                  <Typography>Status</Typography>
                  <Typography>Timestamp</Typography>
                </Box>
                <Divider />
                {recentJobs.jobs.map((job: any) => (
                  <Box
                    key={job.id}
                    sx={{
                      display: 'grid',
                      gridTemplateColumns: 'minmax(200px, 1fr) minmax(150px, 1fr) minmax(150px, 1fr) minmax(200px, 1fr)',
                      gap: 2,
                      p: 1,
                      '&:nth-of-type(odd)': {
                        bgcolor: 'background.default',
                      },
                    }}
                  >
                    <Typography>{job.name}</Typography>
                    <Typography>{job.service}</Typography>
                    <Box>
                      <Chip
                        label={job.status}
                        color={getJobStatusColor(job.status)}
                        size="small"
                      />
                    </Box>
                    <Typography>{new Date(job.timestamp).toLocaleString()}</Typography>
                  </Box>
                ))}
              </Box>
            ) : (
              <Typography color="error">Failed to load recent jobs</Typography>
            )}
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;
