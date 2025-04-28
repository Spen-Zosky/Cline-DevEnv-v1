"""
Scraper API Router

This module provides API endpoints for managing scrape jobs and results.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Path
from fastapi.responses import JSONResponse
from loguru import logger
from bson import ObjectId

from models.scrape_job import (
    ScrapeJob,
    ScrapeJobCreate,
    ScrapeJobUpdate,
    ScrapeJobStatus
)
from models.scrape_result import (
    ScrapeResult,
    ScrapeResultResponse,
    ScrapeResultsResponse
)
from services.database_service import DatabaseService
from services.scraper_service import ScraperService

# Create router
router = APIRouter(tags=["Scraper"])


# Jobs endpoints

@router.post(
    "/jobs",
    response_model=ScrapeJob,
    status_code=201,
    summary="Create a new scrape job"
)
async def create_job(
    job: ScrapeJobCreate,
    background_tasks: BackgroundTasks,
    db: DatabaseService = Depends(),
    scraper_service: ScraperService = Depends()
):
    """
    Create a new scrape job.
    
    The job will be created with PENDING status and then started asynchronously.
    
    Args:
        job: The job to create
        background_tasks: FastAPI background tasks
        db: Database service
        scraper_service: Scraper service
        
    Returns:
        The created job
    """
    try:
        # Create job in database
        created_job = await db.create_job(job)
        
        # Start job in background
        background_tasks.add_task(
            scraper_service.start_job,
            str(created_job.id)
        )
        
        return created_job
    except Exception as e:
        logger.error(f"Error creating job: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create job: {str(e)}"
        )


@router.get(
    "/jobs",
    response_model=Dict[str, Any],
    summary="List scrape jobs"
)
async def list_jobs(
    status: Optional[ScrapeJobStatus] = None,
    tags: Optional[List[str]] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: DatabaseService = Depends()
):
    """
    List scrape jobs with filtering and pagination.
    
    Args:
        status: Filter by job status
        tags: Filter by tags
        skip: Number of jobs to skip
        limit: Maximum number of jobs to return
        db: Database service
        
    Returns:
        Dictionary with jobs and pagination info
    """
    try:
        return await db.list_jobs(
            status=status,
            tags=tags,
            skip=skip,
            limit=limit
        )
    except Exception as e:
        logger.error(f"Error listing jobs: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list jobs: {str(e)}"
        )


@router.get(
    "/jobs/{job_id}",
    response_model=ScrapeJob,
    summary="Get a scrape job"
)
async def get_job(
    job_id: str = Path(..., title="The ID of the job to get"),
    db: DatabaseService = Depends()
):
    """
    Get a scrape job by ID.
    
    Args:
        job_id: The ID of the job to get
        db: Database service
        
    Returns:
        The job
    """
    try:
        job = await db.get_job(job_id)
        
        if not job:
            raise HTTPException(
                status_code=404,
                detail=f"Job with ID {job_id} not found"
            )
        
        return job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get job: {str(e)}"
        )


@router.put(
    "/jobs/{job_id}",
    response_model=ScrapeJob,
    summary="Update a scrape job"
)
async def update_job(
    job_update: ScrapeJobUpdate,
    job_id: str = Path(..., title="The ID of the job to update"),
    db: DatabaseService = Depends()
):
    """
    Update a scrape job.
    
    Args:
        job_update: The updates to apply
        job_id: The ID of the job to update
        db: Database service
        
    Returns:
        The updated job
    """
    try:
        # Check if job exists
        job = await db.get_job(job_id)
        
        if not job:
            raise HTTPException(
                status_code=404,
                detail=f"Job with ID {job_id} not found"
            )
        
        # Check if job can be updated
        if job.status not in [ScrapeJobStatus.PENDING, ScrapeJobStatus.FAILED]:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot update job with status {job.status}"
            )
        
        # Update job
        updated_job = await db.update_job(job_id, job_update)
        
        return updated_job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update job: {str(e)}"
        )


@router.delete(
    "/jobs/{job_id}",
    status_code=204,
    summary="Delete a scrape job"
)
async def delete_job(
    job_id: str = Path(..., title="The ID of the job to delete"),
    db: DatabaseService = Depends(),
    scraper_service: ScraperService = Depends()
):
    """
    Delete a scrape job and all its results.
    
    Args:
        job_id: The ID of the job to delete
        db: Database service
        scraper_service: Scraper service
    """
    try:
        # Check if job exists
        job = await db.get_job(job_id)
        
        if not job:
            raise HTTPException(
                status_code=404,
                detail=f"Job with ID {job_id} not found"
            )
        
        # Cancel job if running
        if job.status == ScrapeJobStatus.RUNNING:
            await scraper_service.cancel_job(job_id)
        
        # Delete job and its results
        deleted = await db.delete_job(job_id)
        
        if not deleted:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete job {job_id}"
            )
        
        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete job: {str(e)}"
        )


@router.post(
    "/jobs/{job_id}/start",
    response_model=ScrapeJob,
    summary="Start a scrape job"
)
async def start_job(
    job_id: str = Path(..., title="The ID of the job to start"),
    background_tasks: BackgroundTasks = None,
    db: DatabaseService = Depends(),
    scraper_service: ScraperService = Depends()
):
    """
    Start a scrape job.
    
    Args:
        job_id: The ID of the job to start
        background_tasks: FastAPI background tasks
        db: Database service
        scraper_service: Scraper service
        
    Returns:
        The updated job
    """
    try:
        # Check if job exists
        job = await db.get_job(job_id)
        
        if not job:
            raise HTTPException(
                status_code=404,
                detail=f"Job with ID {job_id} not found"
            )
        
        # Check if job can be started
        if job.status not in [ScrapeJobStatus.PENDING, ScrapeJobStatus.FAILED]:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot start job with status {job.status}"
            )
        
        # Update job status to PENDING
        job = await db.update_job_status(job_id, ScrapeJobStatus.PENDING)
        
        # Start job in background
        if background_tasks:
            background_tasks.add_task(
                scraper_service.start_job,
                job_id
            )
        else:
            # For testing or direct execution
            await scraper_service.start_job(job_id)
        
        return job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to start job: {str(e)}"
        )


@router.post(
    "/jobs/{job_id}/cancel",
    response_model=ScrapeJob,
    summary="Cancel a scrape job"
)
async def cancel_job(
    job_id: str = Path(..., title="The ID of the job to cancel"),
    db: DatabaseService = Depends(),
    scraper_service: ScraperService = Depends()
):
    """
    Cancel a running scrape job.
    
    Args:
        job_id: The ID of the job to cancel
        db: Database service
        scraper_service: Scraper service
        
    Returns:
        The updated job
    """
    try:
        # Check if job exists
        job = await db.get_job(job_id)
        
        if not job:
            raise HTTPException(
                status_code=404,
                detail=f"Job with ID {job_id} not found"
            )
        
        # Check if job can be cancelled
        if job.status != ScrapeJobStatus.RUNNING:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot cancel job with status {job.status}"
            )
        
        # Cancel job
        await scraper_service.cancel_job(job_id)
        
        # Get updated job
        job = await db.get_job(job_id)
        
        return job
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error cancelling job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to cancel job: {str(e)}"
        )


# Results endpoints

@router.get(
    "/jobs/{job_id}/results",
    response_model=ScrapeResultsResponse,
    summary="Get scrape results for a job"
)
async def get_results(
    job_id: str = Path(..., title="The ID of the job to get results for"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    include_html: bool = Query(False),
    db: DatabaseService = Depends()
):
    """
    Get scrape results for a job with pagination.
    
    Args:
        job_id: The ID of the job to get results for
        skip: Number of results to skip
        limit: Maximum number of results to return
        include_html: Whether to include HTML content in results
        db: Database service
        
    Returns:
        Dictionary with results and pagination info
    """
    try:
        # Check if job exists
        job = await db.get_job(job_id)
        
        if not job:
            raise HTTPException(
                status_code=404,
                detail=f"Job with ID {job_id} not found"
            )
        
        # Get results
        results_data = await db.list_results(
            job_id=job_id,
            skip=skip,
            limit=limit,
            include_html=include_html
        )
        
        # Convert to response model
        results = []
        for result in results_data["results"]:
            result_dict = result.dict(by_alias=True)
            results.append(ScrapeResultResponse(**result_dict))
        
        return ScrapeResultsResponse(
            results=results,
            pagination=results_data["pagination"]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting results for job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get results: {str(e)}"
        )


@router.get(
    "/results/{result_id}",
    response_model=ScrapeResultResponse,
    summary="Get a scrape result"
)
async def get_result(
    result_id: str = Path(..., title="The ID of the result to get"),
    db: DatabaseService = Depends()
):
    """
    Get a scrape result by ID.
    
    Args:
        result_id: The ID of the result to get
        db: Database service
        
    Returns:
        The result
    """
    try:
        result = await db.get_result(result_id)
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail=f"Result with ID {result_id} not found"
            )
        
        result_dict = result.dict(by_alias=True)
        
        return ScrapeResultResponse(**result_dict)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting result {result_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get result: {str(e)}"
        )
