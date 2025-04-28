"""
Scraper Service

This module provides the core functionality for web scraping operations.
"""

import asyncio
import time
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
import traceback
from urllib.parse import urlparse, urljoin
import aiohttp
from bs4 import BeautifulSoup
from loguru import logger
from playwright.async_api import async_playwright
from minio import Minio
from minio.error import MinioException

from config import settings
from models.scrape_job import ScrapeJob, ScrapeJobStatus, ScraperType
from models.scrape_result import ScrapeResultCreate
from services.database_service import DatabaseService


class ScraperService:
    """Service for web scraping operations."""
    
    def __init__(self, db: DatabaseService):
        """
        Initialize the scraper service.
        
        Args:
            db: Database service
        """
        self.db = db
        self.active_jobs = {}  # job_id -> task
        self.minio_client = None
    
    async def initialize(self):
        """Initialize the scraper service."""
        try:
            # Initialize MinIO client
            self.minio_client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_SECURE
            )
            
            # Create bucket if it doesn't exist
            if not self.minio_client.bucket_exists(settings.MINIO_BUCKET):
                self.minio_client.make_bucket(settings.MINIO_BUCKET)
                logger.info(f"Created MinIO bucket: {settings.MINIO_BUCKET}")
            
            logger.info("Scraper service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize scraper service: {str(e)}")
            raise
    
    async def start_job(self, job_id: str):
        """
        Start a scrape job.
        
        Args:
            job_id: The ID of the job to start
        """
        try:
            # Get job from database
            job = await self.db.get_job(job_id)
            
            if not job:
                logger.error(f"Job {job_id} not found")
                return
            
            # Check if job is already running
            if job_id in self.active_jobs:
                logger.warning(f"Job {job_id} is already running")
                return
            
            # Update job status to running
            await self.db.update_job_status(job_id, ScrapeJobStatus.RUNNING)
            
            # Create task for job
            task = asyncio.create_task(self._run_job(job))
            self.active_jobs[job_id] = task
            
            # Wait for task to complete
            await task
            
            # Remove task from active jobs
            if job_id in self.active_jobs:
                del self.active_jobs[job_id]
            
        except Exception as e:
            logger.error(f"Error starting job {job_id}: {str(e)}")
            traceback.print_exc()
            
            # Update job status to failed
            await self.db.update_job_status(
                job_id,
                ScrapeJobStatus.FAILED,
                error=str(e)
            )
            
            # Remove task from active jobs
            if job_id in self.active_jobs:
                del self.active_jobs[job_id]
    
    async def cancel_job(self, job_id: str):
        """
        Cancel a running scrape job.
        
        Args:
            job_id: The ID of the job to cancel
        """
        try:
            # Check if job is running
            if job_id not in self.active_jobs:
                logger.warning(f"Job {job_id} is not running")
                return
            
            # Cancel task
            task = self.active_jobs[job_id]
            task.cancel()
            
            # Update job status to cancelled
            await self.db.update_job_status(job_id, ScrapeJobStatus.CANCELLED)
            
            # Remove task from active jobs
            del self.active_jobs[job_id]
            
            logger.info(f"Cancelled job {job_id}")
        except Exception as e:
            logger.error(f"Error cancelling job {job_id}: {str(e)}")
    
    async def _run_job(self, job: ScrapeJob):
        """
        Run a scrape job.
        
        Args:
            job: The job to run
        """
        try:
            job_id = str(job.id)
            logger.info(f"Running job {job_id}: {job.name}")
            
            # Choose scraper based on job type
            if job.scraper_type == ScraperType.BASIC:
                await self._run_basic_scraper(job)
            elif job.scraper_type == ScraperType.BROWSER:
                await self._run_browser_scraper(job)
            elif job.scraper_type == ScraperType.API:
                await self._run_api_scraper(job)
            elif job.scraper_type == ScraperType.CUSTOM:
                await self._run_custom_scraper(job)
            else:
                raise ValueError(f"Unknown scraper type: {job.scraper_type}")
            
            # Update job status to completed
            await self.db.update_job_status(
                job_id,
                ScrapeJobStatus.COMPLETED,
                progress=100.0
            )
            
            logger.info(f"Completed job {job_id}")
        except asyncio.CancelledError:
            logger.info(f"Job {job.id} was cancelled")
            raise
        except Exception as e:
            logger.error(f"Error running job {job.id}: {str(e)}")
            traceback.print_exc()
            
            # Update job status to failed
            await self.db.update_job_status(
                str(job.id),
                ScrapeJobStatus.FAILED,
                error=str(e)
            )
    
    async def _run_basic_scraper(self, job: ScrapeJob):
        """
        Run a basic scraper using aiohttp and BeautifulSoup.
        
        Args:
            job: The job to run
        """
        job_id = str(job.id)
        url = str(job.url)
        
        # Create session
        async with aiohttp.ClientSession() as session:
            # Create request headers
            headers = {
                "User-Agent": settings.USER_AGENT
            }
            
            # Add custom headers from job
            if job.headers:
                headers.update(job.headers)
            
            # Send request
            start_time = time.time()
            async with session.get(url, headers=headers) as response:
                # Check response
                if response.status != 200:
                    raise ValueError(f"HTTP error: {response.status}")
                
                # Get content type
                content_type = response.headers.get("Content-Type", "")
                
                # Check if HTML
                if "text/html" not in content_type:
                    raise ValueError(f"Unsupported content type: {content_type}")
                
                # Get HTML content
                html = await response.text()
                
                # Parse HTML
                soup = BeautifulSoup(html, "html.parser")
                
                # Extract data based on selectors
                data = {}
                for field_name, selector_config in job.selectors.items():
                    selector_type = selector_config.type
                    selector_value = selector_config.value
                    attribute = selector_config.attribute
                    multiple = selector_config.multiple
                    
                    if selector_type == "css":
                        elements = soup.select(selector_value)
                    elif selector_type == "xpath":
                        # BeautifulSoup doesn't support XPath, so we use a workaround
                        from lxml import etree
                        dom = etree.HTML(str(soup))
                        elements = dom.xpath(selector_value)
                    else:
                        raise ValueError(f"Unknown selector type: {selector_type}")
                    
                    if multiple:
                        if attribute:
                            data[field_name] = [
                                element.get(attribute) if hasattr(element, "get") else element.get_attribute(attribute)
                                for element in elements
                            ]
                        else:
                            data[field_name] = [
                                element.text.strip() if hasattr(element, "text") else element.text_content().strip()
                                for element in elements
                            ]
                    else:
                        if elements:
                            element = elements[0]
                            if attribute:
                                data[field_name] = element.get(attribute) if hasattr(element, "get") else element.get_attribute(attribute)
                            else:
                                data[field_name] = element.text.strip() if hasattr(element, "text") else element.text_content().strip()
                        else:
                            data[field_name] = None
                
                # Extract metadata
                metadata = {
                    "title": soup.title.text.strip() if soup.title else "",
                    "meta_description": soup.find("meta", attrs={"name": "description"}).get("content", "") if soup.find("meta", attrs={"name": "description"}) else "",
                    "meta_keywords": soup.find("meta", attrs={"name": "keywords"}).get("content", "") if soup.find("meta", attrs={"name": "keywords"}) else "",
                    "canonical_url": soup.find("link", attrs={"rel": "canonical"}).get("href", "") if soup.find("link", attrs={"rel": "canonical"}) else "",
                    "content_type": content_type,
                    "headers": dict(response.headers),
                    "status_code": response.status
                }
                
                # Calculate scrape time
                scrape_time = time.time() - start_time
                
                # Create result
                result = ScrapeResultCreate(
                    job_id=job_id,
                    url=url,
                    data=data,
                    html=html,
                    metadata=metadata,
                    status_code=response.status,
                    headers=dict(response.headers),
                    scrape_time=scrape_time
                )
                
                # Save result
                await self.db.create_result(result)
                
                # Update job progress
                await self.db.update_job_status(
                    job_id,
                    ScrapeJobStatus.RUNNING,
                    progress=100.0
                )
    
    async def _run_browser_scraper(self, job: ScrapeJob):
        """
        Run a browser scraper using Playwright.
        
        Args:
            job: The job to run
        """
        job_id = str(job.id)
        url = str(job.url)
        
        # Launch browser
        async with async_playwright() as p:
            # Launch browser
            browser = await p.chromium.launch(headless=True)
            
            try:
                # Create context
                context = await browser.new_context(
                    user_agent=settings.USER_AGENT
                )
                
                # Create page
                page = await context.new_page()
                
                # Set cookies if provided
                if job.cookies:
                    for name, value in job.cookies.items():
                        await page.add_cookie({
                            "name": name,
                            "value": value,
                            "url": url
                        })
                
                # Navigate to URL
                start_time = time.time()
                response = await page.goto(url)
                
                # Check response
                if not response:
                    raise ValueError("No response received")
                
                if response.status != 200:
                    raise ValueError(f"HTTP error: {response.status}")
                
                # Wait for selector if provided
                if job.wait_for_selector:
                    await page.wait_for_selector(job.wait_for_selector)
                
                # Wait for specified time if provided
                if job.wait_time:
                    await asyncio.sleep(job.wait_time)
                
                # Get HTML content
                html = await page.content()
                
                # Extract data based on selectors
                data = {}
                for field_name, selector_config in job.selectors.items():
                    selector_type = selector_config.type
                    selector_value = selector_config.value
                    attribute = selector_config.attribute
                    multiple = selector_config.multiple
                    
                    if selector_type == "css":
                        if multiple:
                            if attribute:
                                data[field_name] = await page.eval_on_selector_all(
                                    selector_value,
                                    f"elements => elements.map(e => e.getAttribute('{attribute}'))"
                                )
                            else:
                                data[field_name] = await page.eval_on_selector_all(
                                    selector_value,
                                    "elements => elements.map(e => e.textContent.trim())"
                                )
                        else:
                            try:
                                if attribute:
                                    data[field_name] = await page.get_attribute(selector_value, attribute)
                                else:
                                    data[field_name] = await page.text_content(selector_value)
                            except:
                                data[field_name] = None
                    elif selector_type == "xpath":
                        if multiple:
                            if attribute:
                                data[field_name] = await page.eval_on_xpath_all(
                                    selector_value,
                                    f"elements => elements.map(e => e.getAttribute('{attribute}'))"
                                )
                            else:
                                data[field_name] = await page.eval_on_xpath_all(
                                    selector_value,
                                    "elements => elements.map(e => e.textContent.trim())"
                                )
                        else:
                            try:
                                elements = await page.xpath(selector_value)
                                if elements:
                                    if attribute:
                                        data[field_name] = await elements[0].get_attribute(attribute)
                                    else:
                                        data[field_name] = await elements[0].text_content()
                                else:
                                    data[field_name] = None
                            except:
                                data[field_name] = None
                    else:
                        raise ValueError(f"Unknown selector type: {selector_type}")
                
                # Extract metadata
                metadata = {
                    "title": await page.title(),
                    "url": page.url,
                    "content_type": response.headers.get("content-type", ""),
                    "headers": dict(response.headers),
                    "status_code": response.status
                }
                
                # Take screenshot
                screenshot = await page.screenshot()
                
                # Save screenshot to MinIO
                if self.minio_client:
                    try:
                        screenshot_path = f"{job_id}/{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
                        self.minio_client.put_object(
                            settings.MINIO_BUCKET,
                            screenshot_path,
                            screenshot,
                            len(screenshot),
                            "image/png"
                        )
                        metadata["screenshot_path"] = screenshot_path
                    except MinioException as e:
                        logger.error(f"Failed to save screenshot: {str(e)}")
                
                # Calculate scrape time
                scrape_time = time.time() - start_time
                
                # Create result
                result = ScrapeResultCreate(
                    job_id=job_id,
                    url=url,
                    data=data,
                    html=html,
                    metadata=metadata,
                    status_code=response.status,
                    headers=dict(response.headers),
                    scrape_time=scrape_time
                )
                
                # Save result
                await self.db.create_result(result)
                
                # Update job progress
                await self.db.update_job_status(
                    job_id,
                    ScrapeJobStatus.RUNNING,
                    progress=100.0
                )
            finally:
                # Close browser
                await browser.close()
    
    async def _run_api_scraper(self, job: ScrapeJob):
        """
        Run an API scraper using aiohttp.
        
        Args:
            job: The job to run
        """
        job_id = str(job.id)
        url = str(job.url)
        
        # Create session
        async with aiohttp.ClientSession() as session:
            # Create request headers
            headers = {
                "User-Agent": settings.USER_AGENT,
                "Accept": "application/json"
            }
            
            # Add custom headers from job
            if job.headers:
                headers.update(job.headers)
            
            # Send request
            start_time = time.time()
            async with session.get(url, headers=headers) as response:
                # Check response
                if response.status != 200:
                    raise ValueError(f"HTTP error: {response.status}")
                
                # Get content type
                content_type = response.headers.get("Content-Type", "")
                
                # Check if JSON
                if "application/json" not in content_type:
                    raise ValueError(f"Unsupported content type: {content_type}")
                
                # Get JSON content
                data = await response.json()
                
                # Calculate scrape time
                scrape_time = time.time() - start_time
                
                # Create result
                result = ScrapeResultCreate(
                    job_id=job_id,
                    url=url,
                    data=data,
                    metadata={
                        "content_type": content_type,
                        "headers": dict(response.headers),
                        "status_code": response.status
                    },
                    status_code=response.status,
                    headers=dict(response.headers),
                    scrape_time=scrape_time
                )
                
                # Save result
                await self.db.create_result(result)
                
                # Update job progress
                await self.db.update_job_status(
                    job_id,
                    ScrapeJobStatus.RUNNING,
                    progress=100.0
                )
    
    async def _run_custom_scraper(self, job: ScrapeJob):
        """
        Run a custom scraper.
        
        Args:
            job: The job to run
        """
        # This is a placeholder for custom scraper implementation
        # In a real implementation, this would be customized based on job parameters
        raise NotImplementedError("Custom scraper not implemented")
