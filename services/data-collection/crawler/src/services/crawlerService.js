/**
 * Crawler Service
 * 
 * Provides functionality for web crawling operations.
 */

const puppeteer = require('puppeteer');
const cheerio = require('cheerio');
const axios = require('axios');
const { URL } = require('url');
const logger = require('../utils/logger');
const CrawlJob = require('../models/CrawlJob');
const CrawlResult = require('../models/CrawlResult');

// Map to track active crawlers
const activeCrawlers = new Map();

/**
 * Start a crawl job
 * @param {string} jobId - The ID of the job to start
 */
const startCrawlJob = async (jobId) => {
  try {
    // Get the job from the database
    const job = await CrawlJob.findById(jobId);
    
    if (!job) {
      logger.error(`Job not found: ${jobId}`);
      return;
    }
    
    if (job.status !== 'pending') {
      logger.warn(`Cannot start job with status: ${job.status}`);
      return;
    }
    
    // Update job status to running
    job.status = 'running';
    await job.save();
    
    logger.info(`Starting crawl job: ${jobId} for URL: ${job.url}`);
    
    // Start the crawler
    const crawler = new Crawler(job);
    activeCrawlers.set(jobId.toString(), crawler);
    
    // Start crawling
    await crawler.start();
    
  } catch (error) {
    logger.error(`Error starting crawl job: ${error.message}`);
    
    // Update job status to failed
    try {
      const job = await CrawlJob.findById(jobId);
      if (job) {
        job.status = 'failed';
        job.error = error.message;
        await job.save();
      }
    } catch (updateError) {
      logger.error(`Error updating job status: ${updateError.message}`);
    }
  }
};

/**
 * Stop a crawl job
 * @param {string} jobId - The ID of the job to stop
 */
const stopCrawlJob = async (jobId) => {
  try {
    const crawler = activeCrawlers.get(jobId.toString());
    
    if (crawler) {
      await crawler.stop();
      activeCrawlers.delete(jobId.toString());
      logger.info(`Stopped crawl job: ${jobId}`);
    } else {
      logger.warn(`No active crawler found for job: ${jobId}`);
    }
  } catch (error) {
    logger.error(`Error stopping crawl job: ${error.message}`);
  }
};

/**
 * Get job results
 * @param {string} jobId - The ID of the job
 * @param {number} page - Page number for pagination
 * @param {number} limit - Number of results per page
 * @returns {Object} - Results and pagination info
 */
const getJobResults = async (jobId, page = 1, limit = 100) => {
  try {
    // Calculate pagination
    const skip = (page - 1) * limit;
    
    // Get results from database
    const results = await CrawlResult.find({ jobId })
      .sort({ createdAt: -1 })
      .skip(skip)
      .limit(limit)
      .select('-html'); // Exclude HTML content to reduce response size
    
    // Get total count
    const total = await CrawlResult.countDocuments({ jobId });
    
    return {
      results,
      pagination: {
        total,
        page,
        limit,
        pages: Math.ceil(total / limit)
      }
    };
  } catch (error) {
    logger.error(`Error fetching job results: ${error.message}`);
    throw error;
  }
};

/**
 * Crawler class for handling the crawling process
 */
class Crawler {
  /**
   * Create a new crawler
   * @param {Object} job - The crawl job
   */
  constructor(job) {
    this.job = job;
    this.browser = null;
    this.visitedUrls = new Set();
    this.queue = [];
    this.running = false;
    this.pagesProcessed = 0;
    this.pagesSuccessful = 0;
    this.pagesFailed = 0;
  }
  
  /**
   * Start the crawler
   */
  async start() {
    try {
      this.running = true;
      
      // Launch browser
      this.browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
      });
      
      // Add initial URL to queue
      this.queue.push({
        url: this.job.url,
        depth: 0,
        parentUrl: null
      });
      
      // Process queue
      await this.processQueue();
      
      // Close browser
      if (this.browser) {
        await this.browser.close();
      }
      
      // Update job status
      if (this.running) {
        this.job.status = 'completed';
      } else {
        this.job.status = 'cancelled';
      }
      
      this.job.resultCount = await CrawlResult.countDocuments({ jobId: this.job._id });
      await this.job.save();
      
      logger.info(`Crawl job completed: ${this.job._id}, processed: ${this.pagesProcessed}, successful: ${this.pagesSuccessful}, failed: ${this.pagesFailed}`);
      
    } catch (error) {
      logger.error(`Crawler error: ${error.message}`);
      
      // Update job status
      this.job.status = 'failed';
      this.job.error = error.message;
      await this.job.save();
      
      // Close browser if open
      if (this.browser) {
        await this.browser.close();
      }
    }
  }
  
  /**
   * Stop the crawler
   */
  async stop() {
    this.running = false;
    
    if (this.browser) {
      await this.browser.close();
    }
  }
  
  /**
   * Process the queue of URLs
   */
  async processQueue() {
    while (this.queue.length > 0 && this.running && this.pagesProcessed < this.job.maxPages) {
      const { url, depth, parentUrl } = this.queue.shift();
      
      // Skip if already visited
      if (this.visitedUrls.has(url)) {
        continue;
      }
      
      this.visitedUrls.add(url);
      this.pagesProcessed++;
      
      try {
        // Process the URL
        const result = await this.processUrl(url, depth, parentUrl);
        
        if (result) {
          this.pagesSuccessful++;
          
          // Extract links if depth allows
          if (depth < this.job.depth) {
            for (const link of result.links || []) {
              if (link.isInternal && !this.visitedUrls.has(link.url)) {
                this.queue.push({
                  url: link.url,
                  depth: depth + 1,
                  parentUrl: url
                });
              }
            }
          }
        } else {
          this.pagesFailed++;
        }
      } catch (error) {
        logger.error(`Error processing URL ${url}: ${error.message}`);
        this.pagesFailed++;
      }
      
      // Update job progress
      await this.job.updateProgress(this.pagesProcessed, this.pagesSuccessful, this.pagesFailed);
    }
  }
  
  /**
   * Process a single URL
   * @param {string} url - The URL to process
   * @param {number} depth - The depth level
   * @param {string} parentUrl - The parent URL
   * @returns {Object} - The crawl result
   */
  async processUrl(url, depth, parentUrl) {
    logger.info(`Processing URL: ${url} (depth: ${depth})`);
    
    const startTime = Date.now();
    let page = null;
    
    try {
      // Create a new page
      page = await this.browser.newPage();
      
      // Set timeout
      await page.setDefaultNavigationTimeout(30000);
      
      // Navigate to URL
      const response = await page.goto(url, { waitUntil: 'domcontentloaded' });
      
      if (!response) {
        throw new Error('No response received');
      }
      
      const statusCode = response.status();
      
      // Skip non-successful responses
      if (statusCode !== 200) {
        throw new Error(`HTTP status code: ${statusCode}`);
      }
      
      // Get content type
      const headers = response.headers();
      const contentType = headers['content-type'] || '';
      
      // Skip non-HTML content
      if (!contentType.includes('text/html')) {
        throw new Error(`Unsupported content type: ${contentType}`);
      }
      
      // Get page content
      const html = await page.content();
      const title = await page.title();
      
      // Extract text content
      const textContent = await page.evaluate(() => document.body.innerText);
      
      // Extract metadata
      const metadata = await page.evaluate(() => {
        const metaTags = {};
        const metas = document.querySelectorAll('meta');
        
        metas.forEach(meta => {
          const name = meta.getAttribute('name') || meta.getAttribute('property');
          const content = meta.getAttribute('content');
          
          if (name && content) {
            metaTags[name] = content;
          }
        });
        
        return metaTags;
      });
      
      // Extract links
      const links = await page.evaluate(() => {
        const baseUrl = window.location.origin;
        const currentUrl = window.location.href;
        const urlObj = new URL(currentUrl);
        
        return Array.from(document.querySelectorAll('a[href]')).map(a => {
          let href = a.href;
          
          // Skip anchors, javascript, mailto, etc.
          if (href.startsWith('#') || 
              href.startsWith('javascript:') || 
              href.startsWith('mailto:') || 
              href.startsWith('tel:')) {
            return null;
          }
          
          // Determine if internal link
          const isInternal = href.startsWith(baseUrl) || 
                            (href.startsWith('/') && !href.startsWith('//'));
          
          return {
            url: href,
            text: a.innerText.trim(),
            isInternal
          };
        }).filter(link => link !== null);
      });
      
      // Create result
      const result = new CrawlResult({
        jobId: this.job._id,
        url,
        title,
        content: {
          text: textContent
        },
        html,
        metadata,
        links,
        depth,
        parentUrl,
        statusCode,
        mimeType: contentType,
        headers,
        fetchTime: new Date(),
        processingTime: Date.now() - startTime
      });
      
      // Save result
      await result.save();
      
      return result;
    } catch (error) {
      logger.error(`Error processing URL ${url}: ${error.message}`);
      
      // Create error result
      const errorResult = new CrawlResult({
        jobId: this.job._id,
        url,
        depth,
        parentUrl,
        error: error.message,
        fetchTime: new Date(),
        processingTime: Date.now() - startTime
      });
      
      // Save error result
      await errorResult.save();
      
      return null;
    } finally {
      if (page) {
        await page.close();
      }
    }
  }
}

module.exports = {
  startCrawlJob,
  stopCrawlJob,
  getJobResults
};
