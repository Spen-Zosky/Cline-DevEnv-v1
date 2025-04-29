const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const { exec } = require('child_process');
const si = require('systeminformation');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());
app.use(morgan('dev'));

// Store service status
const services = {
  'data-crawler': {
    name: 'Data Crawler',
    status: 'UP',
    description: 'Crawls websites and collects data',
    version: '1.2.0',
    lastUpdated: '2025-04-15 10:30:00',
    command: {
      start: 'cd ../../data-collection/crawler && npm start',
      stop: 'taskkill /F /IM node.exe /T',
      restart: 'cd ../../data-collection/crawler && npm restart'
    }
  },
  'data-scraper': {
    name: 'Data Scraper',
    status: 'UP',
    description: 'Scrapes data from websites',
    version: '1.1.5',
    lastUpdated: '2025-04-10 09:15:00',
    command: {
      start: 'cd ../../data-collection/scraper && python src/main.py',
      stop: 'taskkill /F /IM python.exe /T',
      restart: 'taskkill /F /IM python.exe /T && cd ../../data-collection/scraper && python src/main.py'
    }
  },
  'data-preprocessor': {
    name: 'Data Preprocessor',
    status: 'UP',
    description: 'Preprocesses collected data',
    version: '1.0.8',
    lastUpdated: '2025-04-12 14:20:00',
    command: {
      start: 'cd ../../data-processing/preprocessor && python src/main.py',
      stop: 'taskkill /F /IM python.exe /T',
      restart: 'taskkill /F /IM python.exe /T && cd ../../data-processing/preprocessor && python src/main.py'
    }
  },
  'data-transformer': {
    name: 'Data Transformer',
    status: 'DOWN',
    description: 'Transforms data into different formats',
    version: '1.3.2',
    lastUpdated: '2025-04-05 11:20:00',
    command: {
      start: 'cd ../../data-processing/transformer && npm start',
      stop: 'taskkill /F /IM node.exe /T',
      restart: 'cd ../../data-processing/transformer && npm restart'
    }
  },
  'ml-trainer': {
    name: 'ML Trainer',
    status: 'UP',
    description: 'Trains machine learning models',
    version: '2.0.1',
    lastUpdated: '2025-04-20 16:45:00',
    command: {
      start: 'cd ../../ml-framework/trainer && python src/main.py',
      stop: 'taskkill /F /IM python.exe /T',
      restart: 'taskkill /F /IM python.exe /T && cd ../../ml-framework/trainer && python src/main.py'
    }
  },
  'ml-evaluator': {
    name: 'ML Evaluator',
    status: 'WARNING',
    description: 'Evaluates machine learning models',
    version: '2.2.1',
    lastUpdated: '2025-04-18 13:40:00',
    command: {
      start: 'cd ../../ml-framework/evaluator && python src/main.py',
      stop: 'taskkill /F /IM python.exe /T',
      restart: 'taskkill /F /IM python.exe /T && cd ../../ml-framework/evaluator && python src/main.py'
    }
  }
};

// Store recent jobs
const recentJobs = [
  {
    name: 'Web Crawl - News Sites',
    service: 'data-crawler',
    status: 'COMPLETED',
    timestamp: '2025-04-28 12:30:45'
  },
  {
    name: 'Data Preprocessing - Dataset A',
    service: 'data-preprocessor',
    status: 'RUNNING',
    timestamp: '2025-04-28 13:15:22'
  },
  {
    name: 'Model Training - NLP Classifier',
    service: 'ml-trainer',
    status: 'QUEUED',
    timestamp: '2025-04-28 13:45:10'
  },
  {
    name: 'Data Scraping - E-commerce',
    service: 'data-scraper',
    status: 'FAILED',
    timestamp: '2025-04-28 11:20:33'
  },
  {
    name: 'Model Evaluation - Image Classifier',
    service: 'ml-evaluator',
    status: 'COMPLETED',
    timestamp: '2025-04-28 10:05:18'
  }
];

// Routes

// Get all services
app.get('/api/services', (req, res) => {
  res.json(Object.values(services));
});

// Get a specific service
app.get('/api/services/:id', (req, res) => {
  const service = services[req.params.id];
  if (!service) {
    return res.status(404).json({ error: 'Service not found' });
  }
  res.json(service);
});

// Start a service
app.post('/api/services/:id/start', (req, res) => {
  const serviceId = req.params.id;
  const service = services[serviceId];
  
  if (!service) {
    return res.status(404).json({ error: 'Service not found' });
  }
  
  if (service.status === 'UP') {
    return res.status(400).json({ error: 'Service is already running' });
  }
  
  // Update status to STARTING
  service.status = 'STARTING';
  
  // Execute the start command
  exec(service.command.start, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error starting service: ${error.message}`);
      service.status = 'DOWN';
      return res.status(500).json({ error: 'Failed to start service', details: error.message });
    }
    
    // Update status to UP
    service.status = 'UP';
    res.json({ message: `Service ${serviceId} started successfully`, service });
  });
});

// Stop a service
app.post('/api/services/:id/stop', (req, res) => {
  const serviceId = req.params.id;
  const service = services[serviceId];
  
  if (!service) {
    return res.status(404).json({ error: 'Service not found' });
  }
  
  if (service.status === 'DOWN') {
    return res.status(400).json({ error: 'Service is already stopped' });
  }
  
  // Update status to STOPPING
  service.status = 'STOPPING';
  
  // Execute the stop command
  exec(service.command.stop, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error stopping service: ${error.message}`);
      service.status = 'UP';
      return res.status(500).json({ error: 'Failed to stop service', details: error.message });
    }
    
    // Update status to DOWN
    service.status = 'DOWN';
    res.json({ message: `Service ${serviceId} stopped successfully`, service });
  });
});

// Restart a service
app.post('/api/services/:id/restart', (req, res) => {
  const serviceId = req.params.id;
  const service = services[serviceId];
  
  if (!service) {
    return res.status(404).json({ error: 'Service not found' });
  }
  
  // Update status to RESTARTING
  service.status = 'RESTARTING';
  
  // Execute the restart command
  exec(service.command.restart, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error restarting service: ${error.message}`);
      service.status = 'DOWN';
      return res.status(500).json({ error: 'Failed to restart service', details: error.message });
    }
    
    // Update status to UP
    service.status = 'UP';
    res.json({ message: `Service ${serviceId} restarted successfully`, service });
  });
});

// Get system information
app.get('/api/system', async (req, res) => {
  try {
    const [cpu, mem, disk, os, time] = await Promise.all([
      si.cpu(),
      si.mem(),
      si.fsSize(),
      si.osInfo(),
      si.time()
    ]);
    
    const cpuUsage = await si.currentLoad();
    
    const systemInfo = {
      cpu: {
        model: cpu.manufacturer + ' ' + cpu.brand,
        cores: cpu.cores,
        usage: cpuUsage.currentLoad.toFixed(1)
      },
      memory: {
        total: (mem.total / (1024 * 1024 * 1024)).toFixed(2) + ' GB',
        used: (mem.used / (1024 * 1024 * 1024)).toFixed(2) + ' GB',
        usagePercentage: (mem.used / mem.total * 100).toFixed(1)
      },
      disk: {
        total: (disk[0].size / (1024 * 1024 * 1024)).toFixed(2) + ' GB',
        used: (disk[0].used / (1024 * 1024 * 1024)).toFixed(2) + ' GB',
        usagePercentage: (disk[0].use).toFixed(1)
      },
      os: {
        platform: os.platform,
        distro: os.distro,
        release: os.release,
        uptime: Math.floor(os.uptime / 86400) + 'd ' + 
                Math.floor((os.uptime % 86400) / 3600) + 'h ' + 
                Math.floor((os.uptime % 3600) / 60) + 'm'
      },
      time: {
        current: time.current,
        uptime: time.uptime,
        timezone: time.timezone
      }
    };
    
    res.json(systemInfo);
  } catch (error) {
    console.error('Error fetching system information:', error);
    res.status(500).json({ error: 'Failed to fetch system information' });
  }
});

// Get recent jobs
app.get('/api/jobs', (req, res) => {
  res.json(recentJobs);
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
