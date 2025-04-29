/**
 * Service management routes for API Gateway
 * 
 * Provides endpoints for managing and interacting with the platform services.
 */

const express = require('express');
const axios = require('axios');
const router = express.Router();
const logger = require('../utils/logger');

/**
 * @swagger
 * /api/services:
 *   get:
 *     summary: List all services
 *     description: Returns a list of all available services in the platform
 *     responses:
 *       200:
 *         description: List of services
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 services:
 *                   type: array
 *                   items:
 *                     type: object
 *                     properties:
 *                       id:
 *                         type: string
 *                         example: data-crawler
 *                       name:
 *                         type: string
 *                         example: Data Crawler
 *                       description:
 *                         type: string
 *                         example: Crawls websites and collects data
 *                       url:
 *                         type: string
 *                         example: http://data-crawler:8080
 *                       status:
 *                         type: string
 *                         example: UP
 */
router.get('/', async (req, res) => {
  try {
    // Define the services
    const services = [
      {
        id: 'data-crawler',
        name: 'Data Crawler',
        description: 'Crawls websites and collects data',
        url: process.env.CRAWLER_SERVICE_URL || 'http://data-crawler:8080',
        category: 'data-collection'
      },
      {
        id: 'data-scraper',
        name: 'Data Scraper',
        description: 'Scrapes structured data from websites',
        url: process.env.SCRAPER_SERVICE_URL || 'http://data-scraper:8081',
        category: 'data-collection'
      },
      {
        id: 'data-preprocessor',
        name: 'Data Preprocessor',
        description: 'Preprocesses data for machine learning',
        url: process.env.PREPROCESSOR_SERVICE_URL || 'http://data-preprocessor:8082',
        category: 'data-processing'
      },
      {
        id: 'data-transformer',
        name: 'Data Transformer',
        description: 'Transforms data into different formats',
        url: process.env.TRANSFORMER_SERVICE_URL || 'http://data-transformer:8083',
        category: 'data-processing'
      },
      {
        id: 'ml-trainer',
        name: 'ML Trainer',
        description: 'Trains machine learning models',
        url: process.env.ML_TRAINER_URL || 'http://ml-trainer:8090',
        category: 'ml-framework'
      },
      {
        id: 'ml-evaluator',
        name: 'ML Evaluator',
        description: 'Evaluates machine learning models',
        url: process.env.ML_EVALUATOR_URL || 'http://ml-evaluator:8091',
        category: 'ml-framework'
      },
      {
        id: 'web-generator',
        name: 'Web Generator',
        description: 'Generates websites and web applications',
        url: process.env.WEB_GENERATOR_URL || 'http://web-generator:8095',
        category: 'web-generator'
      }
    ];

    // Check service status in parallel
    const servicePromises = services.map(async (service) => {
      try {
        const response = await axios.get(`${service.url}/health`, { timeout: 3000 });
        return {
          ...service,
          status: response.status === 200 ? 'UP' : 'DOWN'
        };
      } catch (error) {
        logger.warn(`Service ${service.id} health check failed: ${error.message}`);
        return {
          ...service,
          status: 'DOWN'
        };
      }
    });

    const servicesWithStatus = await Promise.all(servicePromises);

    res.status(200).json({
      services: servicesWithStatus
    });
  } catch (error) {
    logger.error(`Error listing services: ${error.message}`);
    res.status(500).json({
      status: 'error',
      message: 'Failed to list services',
      error: error.message
    });
  }
});

/**
 * @swagger
 * /api/services/{serviceId}/status:
 *   get:
 *     summary: Get service status
 *     description: Returns the status of a specific service
 *     parameters:
 *       - in: path
 *         name: serviceId
 *         required: true
 *         schema:
 *           type: string
 *         description: ID of the service to get status for
 *     responses:
 *       200:
 *         description: Service status
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 id:
 *                   type: string
 *                   example: data-crawler
 *                 status:
 *                   type: string
 *                   example: UP
 *                 details:
 *                   type: object
 *       404:
 *         description: Service not found
 *       500:
 *         description: Error getting service status
 */
router.get('/:serviceId/status', async (req, res) => {
  try {
    const { serviceId } = req.params;
    
    // Map service ID to URL
    const serviceUrls = {
      'data-crawler': process.env.CRAWLER_SERVICE_URL || 'http://data-crawler:8080',
      'data-scraper': process.env.SCRAPER_SERVICE_URL || 'http://data-scraper:8081',
      'data-preprocessor': process.env.PREPROCESSOR_SERVICE_URL || 'http://data-preprocessor:8082',
      'data-transformer': process.env.TRANSFORMER_SERVICE_URL || 'http://data-transformer:8083',
      'ml-trainer': process.env.ML_TRAINER_URL || 'http://ml-trainer:8090',
      'ml-evaluator': process.env.ML_EVALUATOR_URL || 'http://ml-evaluator:8091',
      'web-generator': process.env.WEB_GENERATOR_URL || 'http://web-generator:8095'
    };
    
    const serviceUrl = serviceUrls[serviceId];
    
    if (!serviceUrl) {
      return res.status(404).json({
        status: 'error',
        message: `Service ${serviceId} not found`
      });
    }
    
    try {
      const response = await axios.get(`${serviceUrl}/health`, { timeout: 5000 });
      
      res.status(200).json({
        id: serviceId,
        status: response.status === 200 ? 'UP' : 'DOWN',
        details: response.data
      });
    } catch (error) {
      logger.warn(`Service ${serviceId} health check failed: ${error.message}`);
      
      res.status(200).json({
        id: serviceId,
        status: 'DOWN',
        error: error.message
      });
    }
  } catch (error) {
    logger.error(`Error getting service status: ${error.message}`);
    res.status(500).json({
      status: 'error',
      message: 'Failed to get service status',
      error: error.message
    });
  }
});

/**
 * @swagger
 * /api/services/{serviceId}/restart:
 *   post:
 *     summary: Restart a service
 *     description: Restarts a specific service
 *     parameters:
 *       - in: path
 *         name: serviceId
 *         required: true
 *         schema:
 *           type: string
 *         description: ID of the service to restart
 *     responses:
 *       200:
 *         description: Service restarted successfully
 *       404:
 *         description: Service not found
 *       500:
 *         description: Error restarting service
 */
router.post('/:serviceId/restart', async (req, res) => {
  try {
    const { serviceId } = req.params;
    
    // In a real implementation, this would use Kubernetes API or Docker API
    // to restart the service. For now, we'll just simulate it.
    
    logger.info(`Simulating restart of service ${serviceId}`);
    
    // Simulate a delay for the restart
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    res.status(200).json({
      id: serviceId,
      status: 'restarted',
      message: `Service ${serviceId} restarted successfully`
    });
  } catch (error) {
    logger.error(`Error restarting service ${req.params.serviceId}: ${error.message}`);
    res.status(500).json({
      status: 'error',
      message: 'Failed to restart service',
      error: error.message
    });
  }
});

/**
 * @swagger
 * /api/services/categories:
 *   get:
 *     summary: Get service categories
 *     description: Returns a list of service categories with their services
 *     responses:
 *       200:
 *         description: List of service categories
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 categories:
 *                   type: array
 *                   items:
 *                     type: object
 *                     properties:
 *                       id:
 *                         type: string
 *                         example: data-collection
 *                       name:
 *                         type: string
 *                         example: Data Collection
 *                       services:
 *                         type: array
 *                         items:
 *                           type: object
 */
router.get('/categories', async (req, res) => {
  try {
    const categories = [
      {
        id: 'data-collection',
        name: 'Data Collection',
        description: 'Services for collecting data from various sources',
        services: ['data-crawler', 'data-scraper']
      },
      {
        id: 'data-processing',
        name: 'Data Processing',
        description: 'Services for processing and transforming data',
        services: ['data-preprocessor', 'data-transformer']
      },
      {
        id: 'ml-framework',
        name: 'Machine Learning Framework',
        description: 'Services for training and evaluating machine learning models',
        services: ['ml-trainer', 'ml-evaluator']
      },
      {
        id: 'web-generator',
        name: 'Web Generator',
        description: 'Services for generating websites and web applications',
        services: ['web-generator']
      }
    ];
    
    res.status(200).json({
      categories
    });
  } catch (error) {
    logger.error(`Error getting service categories: ${error.message}`);
    res.status(500).json({
      status: 'error',
      message: 'Failed to get service categories',
      error: error.message
    });
  }
});

module.exports = router;
