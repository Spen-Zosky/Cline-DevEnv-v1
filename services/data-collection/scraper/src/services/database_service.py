"""
Database Service

This module provides database connectivity and operations for the Data Scraper Service.
"""

import asyncio
from typing import Dict, List, Optional, Any, Union
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure, DuplicateKeyError
from loguru import logger

from config import settings
from models.scrape_job import ScrapeJob, ScrapeJobCreate, ScrapeJobUpdate, ScrapeJobStatus
from models.scrape_result import ScrapeResult, ScrapeResultCreate


class DatabaseService:
    """Service for database operations."""
    
    def __init__(self):
        """Initialize the database service."""
        self.client = None
        self.db = None
        self.jobs_collection = None
        self.results_collection = None
    
    async def connect(self):
        """Connect to the MongoDB database."""
        try:
            # Create MongoDB client
            self.client = AsyncIOMotorClient(settings.MONGODB_URI)
            
            # Get database
            self.db = self.client[settings.MONGODB_DB]
            
            # Get collections
            self.jobs_collection = self.db.scrape_jobs
            self.results_collection = self.db.scrape_results
            
            # Create indexes
            await self.jobs_collection.create_index("status")
            await self.jobs_collection.create_index("created_at")
            await self.jobs_collection.create_index("tags")
            
            await self.results_collection.create_index("job_id")
            await self.results_collection.create_index([("job_id", 1), ("url", 1)], unique=True)
            await self.results_collection.create_index("created_at")
            
            logger.info("Connected to MongoDB")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise
    
    async def close(self):
        """Close the MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("Closed MongoDB connection")
    
    async def ping(self):
        """Ping the MongoDB server to check connection."""
        if not self.client:
            await self.connect()
        
        try:
            await self.client.admin.command("ping")
            return True
        except ConnectionFailure:
            logger.error("MongoDB ping failed")
            raise
    
    # Scrape Job operations
    
    async def create_job(self, job: ScrapeJobCreate) -> ScrapeJob:
        """
        Create a new scrape job.
        
        Args:
            job: The job to create
            
        Returns:
            The created job
        """
        if not self.jobs_collection:
            await self.connect()
        
        job_dict = job.dict()
        job_dict["status"] = ScrapeJobStatus.PENDING
        
        result = await self.jobs_collection.insert_one(job_dict)
        
        created_job = await self.jobs_collection.find_one({"_id": result.inserted_id})
        
        return ScrapeJob(**created_job)
    
    async def get_job(self, job_id: str) -> Optional[ScrapeJob]:
        """
        Get a scrape job by ID.
        
        Args:
            job_id: The ID of the job to get
            
        Returns:
            The job, or None if not found
        """
        if not self.jobs_collection:
            await self.connect()
        
        job = await self.jobs_collection.find_one({"_id": ObjectId(job_id)})
        
        if job:
            return ScrapeJob(**job)
        
        return None
    
    async def update_job(self, job_id: str, job_update: Union[ScrapeJobUpdate, Dict[str, Any]]) -> Optional[ScrapeJob]:
        """
        Update a scrape job.
        
        Args:
            job_id: The ID of the job to update
            job_update: The updates to apply
            
        Returns:
            The updated job, or None if not found
        """
        if not self.jobs_collection:
            await self.connect()
        
        if isinstance(job_update, ScrapeJobUpdate):
            update_data = job_update.dict(exclude_unset=True)
        else:
            update_data = job_update
        
        # Add updated_at timestamp
        update_data["updated_at"] = asyncio.get_event_loop().time()
        
        result = await self.jobs_collection.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
        
        return await self.get_job(job_id)
    
    async def delete_job(self, job_id: str) -> bool:
        """
        Delete a scrape job.
        
        Args:
            job_id: The ID of the job to delete
            
        Returns:
            True if the job was deleted, False otherwise
        """
        if not self.jobs_collection:
            await self.connect()
        
        result = await self.jobs_collection.delete_one({"_id": ObjectId(job_id)})
        
        # Also delete all results for this job
        await self.results_collection.delete_many({"job_id": ObjectId(job_id)})
        
        return result.deleted_count > 0
    
    async def list_jobs(
        self,
        status: Optional[ScrapeJobStatus] = None,
        tags: Optional[List[str]] = None,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "created_at",
        sort_order: int = -1
    ) -> Dict[str, Any]:
        """
        List scrape jobs with filtering and pagination.
        
        Args:
            status: Filter by job status
            tags: Filter by tags
            skip: Number of jobs to skip
            limit: Maximum number of jobs to return
            sort_by: Field to sort by
            sort_order: Sort order (1 for ascending, -1 for descending)
            
        Returns:
            Dictionary with jobs and pagination info
        """
        if not self.jobs_collection:
            await self.connect()
        
        # Build query
        query = {}
        if status:
            query["status"] = status
        if tags:
            query["tags"] = {"$all": tags}
        
        # Get total count
        total = await self.jobs_collection.count_documents(query)
        
        # Get jobs
        cursor = self.jobs_collection.find(query)
        cursor.sort(sort_by, sort_order)
        cursor.skip(skip)
        cursor.limit(limit)
        
        jobs = []
        async for job in cursor:
            jobs.append(ScrapeJob(**job))
        
        return {
            "jobs": jobs,
            "pagination": {
                "total": total,
                "skip": skip,
                "limit": limit,
                "pages": (total + limit - 1) // limit
            }
        }
    
    async def update_job_status(
        self,
        job_id: str,
        status: ScrapeJobStatus,
        error: Optional[str] = None,
        progress: Optional[float] = None
    ) -> Optional[ScrapeJob]:
        """
        Update a job's status.
        
        Args:
            job_id: The ID of the job to update
            status: The new status
            error: Error message if status is FAILED
            progress: Current progress percentage
            
        Returns:
            The updated job, or None if not found
        """
        if not self.jobs_collection:
            await self.connect()
        
        update_data = {"status": status, "updated_at": asyncio.get_event_loop().time()}
        
        if status == ScrapeJobStatus.RUNNING and progress is None:
            update_data["started_at"] = asyncio.get_event_loop().time()
            update_data["progress"] = 0.0
        
        if status in [ScrapeJobStatus.COMPLETED, ScrapeJobStatus.FAILED, ScrapeJobStatus.CANCELLED]:
            update_data["completed_at"] = asyncio.get_event_loop().time()
        
        if error:
            update_data["error"] = error
        
        if progress is not None:
            update_data["progress"] = progress
        
        result = await self.jobs_collection.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
        
        return await self.get_job(job_id)
    
    # Scrape Result operations
    
    async def create_result(self, result: ScrapeResultCreate) -> ScrapeResult:
        """
        Create a new scrape result.
        
        Args:
            result: The result to create
            
        Returns:
            The created result
        """
        if not self.results_collection:
            await self.connect()
        
        result_dict = result.dict()
        result_dict["job_id"] = ObjectId(result_dict["job_id"])
        
        try:
            insert_result = await self.results_collection.insert_one(result_dict)
            
            # Update job result count
            await self.jobs_collection.update_one(
                {"_id": result_dict["job_id"]},
                {"$inc": {"result_count": 1}}
            )
            
            created_result = await self.results_collection.find_one({"_id": insert_result.inserted_id})
            
            return ScrapeResult(**created_result)
        except DuplicateKeyError:
            # Result already exists for this job and URL
            logger.warning(f"Duplicate result for job {result_dict['job_id']} and URL {result_dict['url']}")
            
            # Get the existing result
            existing_result = await self.results_collection.find_one({
                "job_id": result_dict["job_id"],
                "url": result_dict["url"]
            })
            
            return ScrapeResult(**existing_result)
    
    async def get_result(self, result_id: str) -> Optional[ScrapeResult]:
        """
        Get a scrape result by ID.
        
        Args:
            result_id: The ID of the result to get
            
        Returns:
            The result, or None if not found
        """
        if not self.results_collection:
            await self.connect()
        
        result = await self.results_collection.find_one({"_id": ObjectId(result_id)})
        
        if result:
            return ScrapeResult(**result)
        
        return None
    
    async def list_results(
        self,
        job_id: str,
        skip: int = 0,
        limit: int = 100,
        include_html: bool = False
    ) -> Dict[str, Any]:
        """
        List scrape results for a job with pagination.
        
        Args:
            job_id: The ID of the job to get results for
            skip: Number of results to skip
            limit: Maximum number of results to return
            include_html: Whether to include HTML content in results
            
        Returns:
            Dictionary with results and pagination info
        """
        if not self.results_collection:
            await self.connect()
        
        # Build query
        query = {"job_id": ObjectId(job_id)}
        
        # Get total count
        total = await self.results_collection.count_documents(query)
        
        # Get results
        projection = None if include_html else {"html": 0}
        cursor = self.results_collection.find(query, projection)
        cursor.sort("created_at", -1)
        cursor.skip(skip)
        cursor.limit(limit)
        
        results = []
        async for result in cursor:
            results.append(ScrapeResult(**result))
        
        return {
            "results": results,
            "pagination": {
                "total": total,
                "skip": skip,
                "limit": limit,
                "pages": (total + limit - 1) // limit
            }
        }
