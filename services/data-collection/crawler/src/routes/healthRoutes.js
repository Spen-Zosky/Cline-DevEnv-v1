/**
 * Health Routes
 * 
 * Provides health check endpoints for the data crawler service.
 */

const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');
const logger = require('../utils/logger');

/**
 * @route   GET /health
 * @desc    Health check endpoint
 * @access  Public
 */
router.get('/health', (req, res) => {
  res.status(200).json({
    status: 'UP',
    service: 'data-crawler',
    timestamp: new Date().toISOString()
  });
});

/**
 * @route   GET /ready
 * @desc    Readiness check endpoint
 * @access  Public
 */
router.get('/ready', async (req, res) => {
  try {
    // Check MongoDB connection
    const mongoStatus = mongoose.connection.readyState === 1 ? 'UP' : 'DOWN';
    
    if (mongoStatus === 'DOWN') {
      logger.warn('MongoDB connection is down during readiness check');
      return res.status(503).json({
        status: 'DOWN',
        service: 'data-crawler',
        dependencies: {
          mongodb: mongoStatus
        },
        timestamp: new Date().toISOString()
      });
    }
    
    res.status(200).json({
      status: 'UP',
      service: 'data-crawler',
      dependencies: {
        mongodb: mongoStatus
      },
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    logger.error(`Readiness check failed: ${error.message}`);
    res.status(503).json({
      status: 'DOWN',
      service: 'data-crawler',
      error: error.message,
      timestamp: new Date().toISOString()
    });
  }
});

/**
 * @route   GET /metrics
 * @desc    Metrics endpoint
 * @access  Public
 */
router.get('/metrics', (req, res) => {
  // In a real implementation, this would return Prometheus metrics
  res.status(200).json({
    metrics: {
      activeJobs: 0,
      completedJobs: 0,
      failedJobs: 0,
      queuedJobs: 0
    },
    timestamp: new Date().toISOString()
  });
});

module.exports = router;
