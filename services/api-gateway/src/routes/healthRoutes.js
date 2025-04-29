/**
 * Health check routes for API Gateway
 * 
 * Provides endpoints for checking the health of the API Gateway
 * and its connected services.
 */

const express = require('express');
const axios = require('axios');
const router = express.Router();
const logger = require('../utils/logger');

/**
 * @swagger
 * /health:
 *   get:
 *     summary: Basic health check
 *     description: Returns a simple status to indicate the API Gateway is running
 *     responses:
 *       200:
 *         description: API Gateway is running
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 status:
 *                   type: string
 *                   example: UP
 *                 service:
 *                   type: string
 *                   example: api-gateway
 *                 timestamp:
 *                   type: number
 *                   example: 1619712000000
 */
router.get('/', (req, res) => {
  res.status(200).json({
    status: 'UP',
    service: 'api-gateway',
    timestamp: Date.now()
  });
});

/**
 * @swagger
 * /health/ready:
 *   get:
 *     summary: Readiness check
 *     description: Checks if the API Gateway is ready to handle requests
 *     responses:
 *       200:
 *         description: API Gateway is ready
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 status:
 *                   type: string
 *                   example: UP
 *                 service:
 *                   type: string
 *                   example: api-gateway
 *                 timestamp:
 *                   type: number
 *                   example: 1619712000000
 *       503:
 *         description: API Gateway is not ready
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 status:
 *                   type: string
 *                   example: DOWN
 *                 service:
 *                   type: string
 *                   example: api-gateway
 *                 timestamp:
 *                   type: number
 *                   example: 1619712000000
 */
router.get('/ready', async (req, res) => {
  try {
    // Check database connections if needed
    // For now, just return UP
    res.status(200).json({
      status: 'UP',
      service: 'api-gateway',
      timestamp: Date.now()
    });
  } catch (error) {
    logger.error(`Readiness check failed: ${error.message}`);
    res.status(503).json({
      status: 'DOWN',
      service: 'api-gateway',
      error: error.message,
      timestamp: Date.now()
    });
  }
});

/**
 * @swagger
 * /health/services:
 *   get:
 *     summary: Check all services
 *     description: Checks the health of all connected services
 *     responses:
 *       200:
 *         description: Status of all services
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 status:
 *                   type: string
 *                   example: UP
 *                 services:
 *                   type: object
 *                   additionalProperties:
 *                     type: object
 *                     properties:
 *                       status:
 *                         type: string
 *                         example: UP
 *                       url:
 *                         type: string
 *                         example: http://data-crawler:8080
 *                 timestamp:
 *                   type: number
 *                   example: 1619712000000
 */
router.get('/services', async (req, res) => {
  try {
    const services = {
      'data-crawler': {
        url: process.env.CRAWLER_SERVICE_URL || 'http://data-crawler:8080',
        endpoint: '/health'
      },
      'data-scraper': {
        url: process.env.SCRAPER_SERVICE_URL || 'http://data-scraper:8081',
        endpoint: '/health'
      },
      'data-preprocessor': {
        url: process.env.PREPROCESSOR_SERVICE_URL || 'http://data-preprocessor:8082',
        endpoint: '/health'
      },
      'data-transformer': {
        url: process.env.TRANSFORMER_SERVICE_URL || 'http://data-transformer:8083',
        endpoint: '/health'
      },
      'ml-trainer': {
        url: process.env.ML_TRAINER_URL || 'http://ml-trainer:8090',
        endpoint: '/health'
      },
      'ml-evaluator': {
        url: process.env.ML_EVALUATOR_URL || 'http://ml-evaluator:8091',
        endpoint: '/health'
      },
      'web-generator': {
        url: process.env.WEB_GENERATOR_URL || 'http://web-generator:8095',
        endpoint: '/health'
      }
    };

    const serviceStatuses = {};
    let overallStatus = 'UP';

    // Check each service in parallel
    const serviceChecks = Object.entries(services).map(async ([name, service]) => {
      try {
        const response = await axios.get(`${service.url}${service.endpoint}`, { timeout: 5000 });
        serviceStatuses[name] = {
          status: response.status === 200 ? 'UP' : 'DOWN',
          url: service.url,
          details: response.data
        };
      } catch (error) {
        logger.warn(`Service ${name} health check failed: ${error.message}`);
        serviceStatuses[name] = {
          status: 'DOWN',
          url: service.url,
          error: error.message
        };
        overallStatus = 'DEGRADED';
      }
    });

    await Promise.all(serviceChecks);

    res.status(200).json({
      status: overallStatus,
      services: serviceStatuses,
      timestamp: Date.now()
    });
  } catch (error) {
    logger.error(`Service health check failed: ${error.message}`);
    res.status(500).json({
      status: 'ERROR',
      error: error.message,
      timestamp: Date.now()
    });
  }
});

module.exports = router;
