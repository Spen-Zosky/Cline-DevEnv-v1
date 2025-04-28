/**
 * Crawler Routes
 * 
 * Provides endpoints for managing web crawling operations.
 */

const express = require('express');
const router = express.Router();
const logger = require('../utils/logger');
const CrawlJob = require('../models/CrawlJob');
const crawlerService = require('../services/crawlerService');

/**
 * @route   POST /api/crawler/jobs
 * @desc    Create a new crawl job
 * @access  Public
 */
router.post('/jobs', async (req, res) => {
  try {
    const { url, depth, maxPages, selectors, filters } = req.body;
    
    // Validate required fields
    if (!url) {
      return res.status(400).json({ error: 'URL is required' });
    }
    
    // Create a new crawl job
    const newJob = new CrawlJob({
      url,
      depth: depth || 2,
      maxPages: maxPages || 100,
      selectors: selectors || {},
      filters: filters || [],
      status: 'pending'
    });
    
    // Save the job to the database
    await newJob.save();
    
    // Start the crawl job asynchronously
    crawlerService.startCrawlJob(newJob._id);
    
    res.status(201).json({
      message: 'Crawl job created successfully',
      jobId: newJob._id
    });
  } catch (error) {
    logger.error(`Error creating crawl job: ${error.message}`);
    res.status(500).json({ error: 'Failed to create crawl job', message: error.message });
  }
});

/**
 * @route   GET /api/crawler/jobs
 * @desc    Get all crawl jobs
 * @access  Public
 */
router.get('/jobs', async (req, res) => {
  try {
    const { status, limit = 10, page = 1 } = req.query;
    
    // Build query
    const query = {};
    if (status) {
      query.status = status;
    }
    
    // Calculate pagination
    const skip = (parseInt(page) - 1) * parseInt(limit);
    
    // Get jobs from database
    const jobs = await CrawlJob.find(query)
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(parseInt(limit));
    
    // Get total count
    const total = await CrawlJob.countDocuments(query);
    
    res.status(200).json({
      jobs,
      pagination: {
        total,
        page: parseInt(page),
        limit: parseInt(limit),
        pages: Math.ceil(total / parseInt(limit))
      }
    });
  } catch (error) {
    logger.error(`Error fetching crawl jobs: ${error.message}`);
    res.status(500).json({ error: 'Failed to fetch crawl jobs', message: error.message });
  }
});

/**
 * @route   GET /api/crawler/jobs/:id
 * @desc    Get a specific crawl job
 * @access  Public
 */
router.get('/jobs/:id', async (req, res) => {
  try {
    const job = await CrawlJob.findById(req.params.id);
    
    if (!job) {
      return res.status(404).json({ error: 'Crawl job not found' });
    }
    
    res.status(200).json(job);
  } catch (error) {
    logger.error(`Error fetching crawl job: ${error.message}`);
    res.status(500).json({ error: 'Failed to fetch crawl job', message: error.message });
  }
});

/**
 * @route   PUT /api/crawler/jobs/:id/cancel
 * @desc    Cancel a crawl job
 * @access  Public
 */
router.put('/jobs/:id/cancel', async (req, res) => {
  try {
    const job = await CrawlJob.findById(req.params.id);
    
    if (!job) {
      return res.status(404).json({ error: 'Crawl job not found' });
    }
    
    if (job.status === 'completed' || job.status === 'failed' || job.status === 'cancelled') {
      return res.status(400).json({ error: `Cannot cancel job with status: ${job.status}` });
    }
    
    // Cancel the job
    job.status = 'cancelled';
    await job.save();
    
    // Stop the crawler if it's running
    crawlerService.stopCrawlJob(job._id);
    
    res.status(200).json({
      message: 'Crawl job cancelled successfully',
      job
    });
  } catch (error) {
    logger.error(`Error cancelling crawl job: ${error.message}`);
    res.status(500).json({ error: 'Failed to cancel crawl job', message: error.message });
  }
});

/**
 * @route   GET /api/crawler/jobs/:id/results
 * @desc    Get results of a crawl job
 * @access  Public
 */
router.get('/jobs/:id/results', async (req, res) => {
  try {
    const { page = 1, limit = 100 } = req.query;
    
    const job = await CrawlJob.findById(req.params.id);
    
    if (!job) {
      return res.status(404).json({ error: 'Crawl job not found' });
    }
    
    // Get results from the crawler service
    const results = await crawlerService.getJobResults(job._id, parseInt(page), parseInt(limit));
    
    res.status(200).json(results);
  } catch (error) {
    logger.error(`Error fetching crawl job results: ${error.message}`);
    res.status(500).json({ error: 'Failed to fetch crawl job results', message: error.message });
  }
});

module.exports = router;
