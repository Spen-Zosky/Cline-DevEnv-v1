import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Divider,
  LinearProgress,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Tabs,
  Tab,
} from '@mui/material';
import { Refresh as RefreshIcon } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { Line, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

// Mock API service - would be replaced with actual API calls
const fetchSystemMetrics = async () => {
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 1000));
  
  // Mock data
  return {
    cpu: {
      usage_percent: 45.2,
      temperature: 62.5,
      cores: 8,
      model: 'Intel Core i7-10700K',
      clock_speed: 3.8,
    },
    memory: {
      usage_percent: 68.7,
      available_mb: 1254.3,
      total_mb: 32768,
      swap_usage_percent: 12.3,
    },
    disk: {
      usage_percent: 72.1,
      available_gb: 58.4,
      total_gb: 512,
      read_speed_mbps: 120.5,
      write_speed_mbps: 85.2,
    },
    network: {
      incoming_mbps: 25.3,
      outgoing_mbps: 12.8,
      packets_per_second: 1250,
      active_connections: 42,
    },
    services: {
      total: 12,
      running: 10,
      stopped: 1,
      warning: 1,
    },
    uptime: 1209600, // 14 days in seconds
    timestamp: Date.now(),
  };
};

const fetchSystemLogs = async () => {
  // Simulate API call
  await new Promise((resolve) => setTimeout(resolve, 1000));
  
  // Mock data
  return {
    logs: Array.from({ length: 50 }, (_, i) => ({
      id: `log-${i}`,
      timestamp: new Date(Date.now() - i * 60000).toISOString(),
      level: ['info', 'warn', 'error'][Math.floor(Math.random() * 3)],
      service: ['api-gateway', 'data-crawler', 'data-preprocessor', 'ml-trainer'][Math.floor(Math.random() * 4)],
      message: [
        'Service started successfully',
        'Connection established',
        'Processing data batch',
        'Warning: High memory usage',
        'Error: Failed to connect to database',
        'Job completed successfully',
        'New request received',
      ][Math.floor(Math.random() * 7)],
    })),
  };
};

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`system-tabpanel-${index}`}
      aria-labelledby={`system-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const SystemMonitor: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [cpuChartData, setCpuChartData] = useState({
    labels: [],
    datasets: [],
  });
  const [memoryChartData, setMemoryChartData] = useState({
    labels: [],
    datasets: [],
  });
  const [networkChartData, setNetworkChartData] = useState({
    labels: [],
    datasets: [],
  });

  const { data: systemMetrics, isLoading: isLoadingMetrics, refetch: refetchMetrics } = useQuery({
    queryKey: ['systemMetrics'],
    queryFn: fetchSystemMetrics,
  });

  const { data: systemLogs, isLoading: isLoadingLogs, refetch: refetchLogs } = useQuery({
    queryKey: ['systemLogs'],
    queryFn: fetchSystemLogs,
  });

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleRefresh = () => {
    refetchMetrics();
    refetchLogs();
  };

  useEffect(() => {
    if (systemMetrics) {
      // Prepare chart data
      const timeLabels = Array.from({ length: 24 }, (_, i) => {
        const date = new Date();
        date.setHours(date.getHours() - 23 + i);
        return date.getHours() + ':00';
      });
      
      // Mock historical data
      const cpuData = Array.from({ length: 24 }, () => Math.random() * 100);
      const memoryData = Array.from({ length: 24 }, () => Math.random() * 100);
      const incomingData = Array.from({ length: 24 }, () => Math.random() * 50);
      const outgoingData = Array.from({ length: 24 }, () => Math.random() * 30);
      
      setCpuChartData({
        labels: timeLabels,
        datasets: [
          {
            label: 'CPU Usage (%)',
            data: cpuData,
            borderColor: 'rgb(255, 99, 132)',
            backgroundColor: 'rgba(255, 99, 132, 0.5)',
          },
        ],
      });
      
      setMemoryChartData({
        labels: timeLabels,
        datasets: [
          {
            label: 'Memory Usage (%)',
            data: memoryData,
            borderColor: 'rgb(53, 162, 235)',
            backgroundColor: 'rgba(53, 162, 235, 0.5)',
          },
        ],
      });
      
      setNetworkChartData({
        labels: timeLabels,
        datasets: [
          {
            label: 'Incoming (Mbps)',
            data: incomingData,
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.5)',
          },
          {
            label: 'Outgoing (Mbps)',
            data: outgoingData,
            borderColor: 'rgb(153, 102, 255)',
            backgroundColor: 'rgba(153, 102, 255, 0.5)',
          },
        ],
      });
    }
  }, [systemMetrics]);

  const formatUptime = (seconds: number) => {
    const days = Math.floor(seconds / 86400);
    const hours = Math.floor((seconds % 86400) / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    
    return `${days}d ${hours}h ${minutes}m`;
  };

  const getLogLevelColor = (level: string) => {
    switch (level) {
      case 'error':
        return 'error.main';
      case 'warn':
        return 'warning.main';
      case 'info':
        return 'info.main';
      default:
        return 'text.primary';
    }
  };

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          System Monitor
        </Typography>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={handleRefresh}
        >
          Refresh
        </Button>
      </Box>

      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          indicatorColor="primary"
          textColor="primary"
          variant="fullWidth"
        >
          <Tab label="Overview" />
          <Tab label="Resources" />
          <Tab label="Logs" />
        </Tabs>
      </Paper>

      {isLoadingMetrics ? (
        <LinearProgress />
      ) : systemMetrics ? (
        <>
          <TabPanel value={tabValue} index={0}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      System Overview
                    </Typography>
                    <Divider sx={{ mb: 2 }} />
                    <Grid container spacing={2}>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          CPU Model
                        </Typography>
                        <Typography variant="body1" gutterBottom>
                          {systemMetrics.cpu.model}
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          CPU Cores
                        </Typography>
                        <Typography variant="body1" gutterBottom>
                          {systemMetrics.cpu.cores}
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          Total Memory
                        </Typography>
                        <Typography variant="body1" gutterBottom>
                          {(systemMetrics.memory.total_mb / 1024).toFixed(2)} GB
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          Total Disk
                        </Typography>
                        <Typography variant="body1" gutterBottom>
                          {systemMetrics.disk.total_gb} GB
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          System Uptime
                        </Typography>
                        <Typography variant="body1" gutterBottom>
                          {formatUptime(systemMetrics.uptime)}
                        </Typography>
                      </Grid>
                      <Grid item xs={6}>
                        <Typography variant="body2" color="text.secondary">
                          Services Status
                        </Typography>
                        <Typography variant="body1" gutterBottom>
                          {systemMetrics.services.running} running, {systemMetrics.services.warning} warning, {systemMetrics.services.stopped} stopped
                        </Typography>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Current Resource Usage
                    </Typography>
                    <Divider sx={{ mb: 2 }} />
                    <Box sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="body2">CPU Usage</Typography>
                        <Typography variant="body2">{systemMetrics.cpu.usage_percent.toFixed(1)}%</Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={systemMetrics.cpu.usage_percent}
                        color={systemMetrics.cpu.usage_percent > 80 ? 'error' : 'primary'}
                      />
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="body2">Memory Usage</Typography>
                        <Typography variant="body2">{systemMetrics.memory.usage_percent.toFixed(1)}%</Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={systemMetrics.memory.usage_percent}
                        color={systemMetrics.memory.usage_percent > 80 ? 'error' : 'primary'}
                      />
                    </Box>
                    <Box sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="body2">Disk Usage</Typography>
                        <Typography variant="body2">{systemMetrics.disk.usage_percent.toFixed(1)}%</Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={systemMetrics.disk.usage_percent}
                        color={systemMetrics.disk.usage_percent > 80 ? 'error' : 'primary'}
                      />
                    </Box>
                    <Box>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                        <Typography variant="body2">Network</Typography>
                        <Typography variant="body2">
                          ↓ {systemMetrics.network.incoming_mbps.toFixed(1)} Mbps | 
                          ↑ {systemMetrics.network.outgoing_mbps.toFixed(1)} Mbps
                        </Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={(systemMetrics.network.incoming_mbps + systemMetrics.network.outgoing_mbps) / 2}
                        color="info"
                      />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      CPU Usage (24h)
                    </Typography>
                    <Box sx={{ height: 300 }}>
                      <Line
                        data={cpuChartData}
                        options={{
                          responsive: true,
                          maintainAspectRatio: false,
                          scales: {
                            y: {
                              beginAtZero: true,
                              max: 100,
                            },
                          },
                        }}
                      />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={1}>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      CPU Usage (24h)
                    </Typography>
                    <Box sx={{ height: 300 }}>
                      <Line
                        data={cpuChartData}
                        options={{
                          responsive: true,
                          maintainAspectRatio: false,
                          scales: {
                            y: {
                              beginAtZero: true,
                              max: 100,
                            },
                          },
                        }}
                      />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Memory Usage (24h)
                    </Typography>
                    <Box sx={{ height: 300 }}>
                      <Line
                        data={memoryChartData}
                        options={{
                          responsive: true,
                          maintainAspectRatio: false,
                          scales: {
                            y: {
                              beginAtZero: true,
                              max: 100,
                            },
                          },
                        }}
                      />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Network Traffic (24h)
                    </Typography>
                    <Box sx={{ height: 300 }}>
                      <Line
                        data={networkChartData}
                        options={{
                          responsive: true,
                          maintainAspectRatio: false,
                        }}
                      />
                    </Box>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12}>
                <Card>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Detailed Resource Information
                    </Typography>
                    <Divider sx={{ mb: 2 }} />
                    <Grid container spacing={3}>
                      <Grid item xs={12} md={6}>
                        <Typography variant="subtitle1" gutterBottom>
                          CPU
                        </Typography>
                        <Box sx={{ mb: 2 }}>
                          <Typography variant="body2">
                            <strong>Model:</strong> {systemMetrics.cpu.model}
                          </Typography>
                          <Typography variant="body2">
                            <strong>Cores:</strong> {systemMetrics.cpu.cores}
                          </Typography>
                          <Typography variant="body2">
                            <strong>Clock Speed:</strong> {systemMetrics.cpu.clock_speed} GHz
                          </Typography>
                          <Typography variant="body2">
                            <strong>Temperature:</strong> {systemMetrics.cpu.temperature}°C
                          </Typography>
                          <Typography variant="body2">
                            <strong>Usage:</strong> {systemMetrics.cpu.usage_percent.toFixed(1)}%
                          </Typography>
                        </Box>
                        
                        <Typography variant="subtitle1" gutterBottom>
                          Memory
                        </Typography>
                        <Box>
                          <Typography variant="body2">
                            <strong>Total:</strong> {(systemMetrics.memory.total_mb / 1024).toFixed(2)} GB
                          </Typography>
                          <Typography variant="body2">
                            <strong>Available:</strong> {(systemMetrics.memory.available_mb / 1024).toFixed(2)} GB
                          </Typography>
                          <Typography variant="body2">
                            <strong>Used:</strong> {((systemMetrics.memory.total_mb - systemMetrics.memory.available_mb) / 1024).toFixed(2)} GB
                          </Typography>
                          <Typography variant="body2">
                            <strong>Usage:</strong> {systemMetrics.memory.usage_percent.toFixed(1)}%
                          </Typography>
                          <Typography variant="body2">
                            <strong>Swap Usage:</strong> {systemMetrics.memory.swap_usage_percent.toFixed(1)}%
                          </Typography>
                        </Box>
                      </Grid>
                      <Grid item xs={12} md={6}>
                        <Typography variant="subtitle1" gutterBottom>
                          Disk
                        </Typography>
                        <Box sx={{ mb: 2 }}>
                          <Typography variant="body2">
                            <strong>Total:</strong> {systemMetrics.disk.total_gb} GB
                          </Typography>
                          <Typography variant="body2">
                            <strong>Available:</strong> {systemMetrics.disk.available_gb.toFixed(1)} GB
                          </Typography>
                          <Typography variant="body2">
                            <strong>Used:</strong> {(systemMetrics.disk.total_gb - systemMetrics.disk.available_gb).toFixed(1)} GB
                          </Typography>
                          <Typography variant="body2">
                            <strong>Usage:</strong> {systemMetrics.disk.usage_percent.toFixed(1)}%
                          </Typography>
                          <Typography variant="body2">
                            <strong>Read Speed:</strong> {systemMetrics.disk.read_speed_mbps.toFixed(1)} MB/s
                          </Typography>
                          <Typography variant="body2">
                            <strong>Write Speed:</strong> {systemMetrics.disk.write_speed_mbps.toFixed(1)} MB/s
                          </Typography>
                        </Box>
                        
                        <Typography variant="subtitle1" gutterBottom>
                          Network
                        </Typography>
                        <Box>
                          <Typography variant="body2">
                            <strong>Incoming:</strong> {systemMetrics.network.incoming_mbps.toFixed(1)} Mbps
                          </Typography>
                          <Typography variant="body2">
                            <strong>Outgoing:</strong> {systemMetrics.network.outgoing_mbps.toFixed(1)} Mbps
                          </Typography>
                          <Typography variant="body2">
                            <strong>Packets/sec:</strong> {systemMetrics.network.packets_per_second}
                          </Typography>
                          <Typography variant="body2">
                            <strong>Active Connections:</strong> {systemMetrics.network.active_connections}
                          </Typography>
                        </Box>
                      </Grid>
                    </Grid>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          </TabPanel>

          <TabPanel value={tabValue} index={2}>
            {isLoadingLogs ? (
              <LinearProgress />
            ) : systemLogs ? (
              <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Timestamp</TableCell>
                      <TableCell>Level</TableCell>
                      <TableCell>Service</TableCell>
                      <TableCell>Message</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {systemLogs.logs.map((log: { id: string; timestamp: string; level: string; service: string; message: string }) => (
                      <TableRow key={log.id}>
                        <TableCell>{new Date(log.timestamp).toLocaleString()}</TableCell>
                        <TableCell>
                          <Typography sx={{ color: getLogLevelColor(log.level) }}>
                            {log.level.toUpperCase()}
                          </Typography>
                        </TableCell>
                        <TableCell>{log.service}</TableCell>
                        <TableCell>{log.message}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            ) : (
              <Typography color="error">Failed to load system logs</Typography>
            )}
          </TabPanel>
        </>
      ) : (
        <Typography color="error">Failed to load system metrics</Typography>
      )}
    </Box>
  );
};

export default SystemMonitor;
