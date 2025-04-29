/**
 * API Gateway for AI Research Platform
 * 
 * This service acts as a central entry point for all API requests,
 * routing them to the appropriate microservices.
 */

const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const { createProxyMiddleware } = require('http-proxy-middleware');
const rateLimit = require('express-rate-limit');
const swaggerJsDoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');
const logger = require('./utils/logger');

// Load environment variables
require('dotenv').config();

// Import routes
const healthRoutes = require('./routes/healthRoutes');
const serviceRoutes = require('./routes/serviceRoutes');
const systemRoutes = require('./routes/systemRoutes');

// Create Express app
const app = express();
const PORT = process.env.PORT || 8000;

// Middleware
app.use(helmet()); // Security headers
app.use(cors()); // Enable CORS for all routes
app.use(express.json()); // Parse JSON request bodies
app.use(express.urlencoded({ extended: true })); // Parse URL-encoded request bodies
app.use(morgan('combined', { stream: { write: message => logger.info(message.trim()) } })); // HTTP request logging

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // Limit each IP to 100 requests per windowMs
  standardHeaders: true,
  legacyHeaders: false,
  message: 'Too many requests from this IP, please try again after 15 minutes'
});
app.use(limiter);

// Swagger documentation
const swaggerOptions = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'AI Research Platform API',
      version: '1.0.0',
      description: 'API documentation for the AI Research Platform',
    },
    servers: [
      {
        url: `http://localhost:${PORT}`,
        description: 'Development server',
      },
    ],
  },
  apis: ['./src/routes/*.js'], // Path to the API docs
};
const swaggerDocs = swaggerJsDoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));

// Routes
app.use('/health', healthRoutes);
app.use('/api/services', serviceRoutes);
app.use('/api/system', systemRoutes);

// Service proxies
// Data Collection Services
app.use('/api/crawler', createProxyMiddleware({
  target: process.env.CRAWLER_SERVICE_URL || 'http://data-crawler:8080',
  changeOrigin: true,
  pathRewrite: { '^/api/crawler': '' },
  logLevel: 'debug'
}));

app.use('/api/scraper', createProxyMiddleware({
  target: process.env.SCRAPER_SERVICE_URL || 'http://data-scraper:8081',
  changeOrigin: true,
  pathRewrite: { '^/api/scraper': '' },
  logLevel: 'debug'
}));

// Data Processing Services
app.use('/api/preprocessor', createProxyMiddleware({
  target: process.env.PREPROCESSOR_SERVICE_URL || 'http://data-preprocessor:8082',
  changeOrigin: true,
  pathRewrite: { '^/api/preprocessor': '' },
  logLevel: 'debug'
}));

app.use('/api/transformer', createProxyMiddleware({
  target: process.env.TRANSFORMER_SERVICE_URL || 'http://data-transformer:8083',
  changeOrigin: true,
  pathRewrite: { '^/api/transformer': '' },
  logLevel: 'debug'
}));

// ML Framework Services
app.use('/api/ml-trainer', createProxyMiddleware({
  target: process.env.ML_TRAINER_URL || 'http://ml-trainer:8090',
  changeOrigin: true,
  pathRewrite: { '^/api/ml-trainer': '' },
  logLevel: 'debug'
}));

app.use('/api/ml-evaluator', createProxyMiddleware({
  target: process.env.ML_EVALUATOR_URL || 'http://ml-evaluator:8091',
  changeOrigin: true,
  pathRewrite: { '^/api/ml-evaluator': '' },
  logLevel: 'debug'
}));

// Web Generator Service
app.use('/api/web-generator', createProxyMiddleware({
  target: process.env.WEB_GENERATOR_URL || 'http://web-generator:8095',
  changeOrigin: true,
  pathRewrite: { '^/api/web-generator': '' },
  logLevel: 'debug'
}));

// Error handling middleware
app.use((err, req, res, next) => {
  logger.error(err.stack);
  res.status(500).json({
    status: 'error',
    message: 'Internal Server Error',
    error: process.env.NODE_ENV === 'development' ? err.message : undefined
  });
});

// Start the server
app.listen(PORT, () => {
  logger.info(`API Gateway running on port ${PORT}`);
});

module.exports = app; // Export for testing
