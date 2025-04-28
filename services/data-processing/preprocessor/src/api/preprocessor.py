"""
Preprocessor API Router

This module provides API endpoints for managing preprocessing jobs and results.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query, Path
from fastapi.responses import JSONResponse
from loguru import logger
from bson import ObjectId

from models.preprocessing_job import (
    PreprocessingJob,
    PreprocessingJobCreate,
    PreprocessingJobUpdate,
    PreprocessingJobStatus,
    DataSourceType,
    DataType
)
from models.preprocessing_result import (
    PreprocessingResult,
    PreprocessingResultResponse,
    PreprocessingResultsResponse
)
from services.database_service import DatabaseService
from services.storage_service import StorageService
from services.preprocessing_service import PreprocessingService
from config import settings

# Create router
router = APIRouter(tags=["Preprocessor"])


# Jobs endpoints

@router.post(
    "/jobs",
    response_model=PreprocessingJob,
    status_code=201,
    summary="Create a new preprocessing job"
)
async def create_job(
    job: PreprocessingJobCreate,
    background_tasks: BackgroundTasks,
    db: DatabaseService = Depends(),
    preprocessing_service: PreprocessingService = Depends()
):
    """
    Create a new preprocessing job.
    
    The job will be created with PENDING status and then processed asynchronously.
    
    Args:
        job: The job to create
        background_tasks: FastAPI background tasks
        db: Database service
        preprocessing_service: Preprocessing service
        
    Returns:
        The created job
    """
    try:
        # Create job in database
        created_job = await db.create_job(job)
        
        # Process job in background
        # Note: The job will be picked up by the background job processor
        
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
    summary="List preprocessing jobs"
)
async def list_jobs(
    status: Optional[PreprocessingJobStatus] = None,
    source_type: Optional[DataSourceType] = None,
    source_id: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: DatabaseService = Depends()
):
    """
    List preprocessing jobs with filtering and pagination.
    
    Args:
        status: Filter by job status
        source_type: Filter by source type
        source_id: Filter by source ID
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
            source_type=source_type,
            source_id=source_id,
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
    response_model=PreprocessingJob,
    summary="Get a preprocessing job"
)
async def get_job(
    job_id: str = Path(..., title="The ID of the job to get"),
    db: DatabaseService = Depends()
):
    """
    Get a preprocessing job by ID.
    
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
    response_model=PreprocessingJob,
    summary="Update a preprocessing job"
)
async def update_job(
    job_update: PreprocessingJobUpdate,
    job_id: str = Path(..., title="The ID of the job to update"),
    db: DatabaseService = Depends()
):
    """
    Update a preprocessing job.
    
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
        if job.status not in [PreprocessingJobStatus.PENDING, PreprocessingJobStatus.FAILED]:
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
    summary="Delete a preprocessing job"
)
async def delete_job(
    job_id: str = Path(..., title="The ID of the job to delete"),
    db: DatabaseService = Depends(),
    preprocessing_service: PreprocessingService = Depends()
):
    """
    Delete a preprocessing job and all its results.
    
    Args:
        job_id: The ID of the job to delete
        db: Database service
        preprocessing_service: Preprocessing service
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
        if job.status == PreprocessingJobStatus.RUNNING:
            await preprocessing_service.cancel_job(job_id)
        
        # Delete job and its results
        deleted = await db.delete_job(job_id)
        
        if not deleted:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete job {job_id}"
            )
        
        # Delete output files if they exist
        if job.output_path:
            await preprocessing_service.delete_output_files(job)
        
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
    response_model=PreprocessingJob,
    summary="Start a preprocessing job"
)
async def start_job(
    job_id: str = Path(..., title="The ID of the job to start"),
    background_tasks: BackgroundTasks = None,
    db: DatabaseService = Depends(),
    preprocessing_service: PreprocessingService = Depends()
):
    """
    Start a preprocessing job.
    
    Args:
        job_id: The ID of the job to start
        background_tasks: FastAPI background tasks
        db: Database service
        preprocessing_service: Preprocessing service
        
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
        if job.status not in [PreprocessingJobStatus.PENDING, PreprocessingJobStatus.FAILED]:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot start job with status {job.status}"
            )
        
        # Update job status to PENDING
        job = await db.update_job_status(job_id, PreprocessingJobStatus.PENDING)
        
        # Start job in background
        if background_tasks:
            background_tasks.add_task(
                preprocessing_service.process_job,
                job_id
            )
        else:
            # For testing or direct execution
            await preprocessing_service.process_job(job_id)
        
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
    response_model=PreprocessingJob,
    summary="Cancel a preprocessing job"
)
async def cancel_job(
    job_id: str = Path(..., title="The ID of the job to cancel"),
    db: DatabaseService = Depends(),
    preprocessing_service: PreprocessingService = Depends()
):
    """
    Cancel a running preprocessing job.
    
    Args:
        job_id: The ID of the job to cancel
        db: Database service
        preprocessing_service: Preprocessing service
        
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
        if job.status != PreprocessingJobStatus.RUNNING:
            raise HTTPException(
                status_code=400,
                detail=f"Cannot cancel job with status {job.status}"
            )
        
        # Cancel job
        await preprocessing_service.cancel_job(job_id)
        
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
    response_model=PreprocessingResultsResponse,
    summary="Get preprocessing results for a job"
)
async def get_results(
    job_id: str = Path(..., title="The ID of the job to get results for"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: DatabaseService = Depends()
):
    """
    Get preprocessing results for a job with pagination.
    
    Args:
        job_id: The ID of the job to get results for
        skip: Number of results to skip
        limit: Maximum number of results to return
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
            limit=limit
        )
        
        # Convert to response model
        results = []
        for result in results_data["results"]:
            result_dict = result.dict(by_alias=True)
            results.append(PreprocessingResultResponse(**result_dict))
        
        return PreprocessingResultsResponse(
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
    response_model=PreprocessingResultResponse,
    summary="Get a preprocessing result"
)
async def get_result(
    result_id: str = Path(..., title="The ID of the result to get"),
    db: DatabaseService = Depends()
):
    """
    Get a preprocessing result by ID.
    
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
        
        return PreprocessingResultResponse(**result_dict)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting result {result_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get result: {str(e)}"
        )


@router.get(
    "/jobs/{job_id}/download",
    summary="Get a download URL for processed data"
)
async def get_download_url(
    job_id: str = Path(..., title="The ID of the job to get download URL for"),
    expires: int = Query(3600, ge=60, le=86400, description="Expiration time in seconds"),
    db: DatabaseService = Depends(),
    storage: StorageService = Depends()
):
    """
    Get a presigned URL to download the processed data.
    
    Args:
        job_id: The ID of the job to get download URL for
        expires: Expiration time in seconds
        db: Database service
        storage: Storage service
        
    Returns:
        Dictionary with download URL
    """
    try:
        # Check if job exists
        job = await db.get_job(job_id)
        
        if not job:
            raise HTTPException(
                status_code=404,
                detail=f"Job with ID {job_id} not found"
            )
        
        # Check if job is completed
        if job.status != PreprocessingJobStatus.COMPLETED:
            raise HTTPException(
                status_code=400,
                detail=f"Job is not completed (status: {job.status})"
            )
        
        # Check if output path exists
        if not job.output_path:
            raise HTTPException(
                status_code=400,
                detail="Job has no output path"
            )
        
        # Get presigned URL
        url = await storage.get_presigned_url(
            bucket=settings.MINIO_PROCESSED_BUCKET,
            object_name=job.output_path,
            expires=expires
        )
        
        return {
            "url": url,
            "expires_in": expires,
            "job_id": job_id,
            "output_path": job.output_path
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting download URL for job {job_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get download URL: {str(e)}"
        )
