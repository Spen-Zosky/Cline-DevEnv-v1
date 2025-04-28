"""
Health API Router

This module provides health check endpoints for the Data Scraper Service.
"""

import time
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from minio import Minio
from minio.error import MinioException

from config import settings
from services.database_service import DatabaseService

# Create router
router = APIRouter(tags=["Health"])


@router.get("/health", summary="Health check")
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Health status information
    """
    return {
        "status": "UP",
        "service": "data-scraper",
        "timestamp": time.time()
    }


@router.get("/ready", summary="Readiness check")
async def readiness_check(db: DatabaseService = Depends()):
    """
    Readiness check endpoint.
    
    Checks if the service is ready to handle requests by verifying
    connections to dependencies like MongoDB and MinIO.
    
    Returns:
        dict: Readiness status information
    """
    status = "UP"
    dependencies = {}
    
    # Check MongoDB connection
    try:
        # Ping MongoDB
        await db.ping()
        dependencies["mongodb"] = "UP"
    except Exception as e:
        logger.error(f"MongoDB connection failed: {str(e)}")
        dependencies["mongodb"] = "DOWN"
        status = "DOWN"
    
    # Check MinIO connection
    try:
        # Create MinIO client
        minio_client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE
        )
        
        # Check if bucket exists
        if not minio_client.bucket_exists(settings.MINIO_BUCKET):
            # Create bucket if it doesn't exist
            minio_client.make_bucket(settings.MINIO_BUCKET)
            logger.info(f"Created MinIO bucket: {settings.MINIO_BUCKET}")
        
        dependencies["minio"] = "UP"
    except MinioException as e:
        logger.error(f"MinIO connection failed: {str(e)}")
        dependencies["minio"] = "DOWN"
        status = "DOWN"
    except Exception as e:
        logger.error(f"MinIO error: {str(e)}")
        dependencies["minio"] = "DOWN"
        status = "DOWN"
    
    response = {
        "status": status,
        "service": "data-scraper",
        "dependencies": dependencies,
        "timestamp": time.time()
    }
    
    if status == "DOWN":
        return JSONResponse(content=response, status_code=503)
    
    return response


@router.get("/metrics", summary="Metrics endpoint")
async def metrics():
    """
    Metrics endpoint.
    
    Returns:
        dict: Service metrics
    """
    # In a real implementation, this would return Prometheus metrics
    return {
        "metrics": {
            "active_jobs": 0,
            "completed_jobs": 0,
            "failed_jobs": 0,
            "total_jobs": 0,
            "scrape_results": 0,
            "average_scrape_time": 0
        },
        "timestamp": time.time()
    }
