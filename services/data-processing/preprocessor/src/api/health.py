"""
Health API Router

This module provides health check endpoints for the Data Preprocessor Service.
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
from services.storage_service import StorageService

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
        "service": "data-preprocessor",
        "timestamp": time.time()
    }


@router.get("/ready", summary="Readiness check")
async def readiness_check(
    db: DatabaseService = Depends(),
    storage: StorageService = Depends()
):
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
        # Check MinIO connection
        storage_status = await storage.check_connection()
        dependencies["minio"] = "UP" if storage_status else "DOWN"
        if not storage_status:
            status = "DOWN"
    except Exception as e:
        logger.error(f"MinIO connection failed: {str(e)}")
        dependencies["minio"] = "DOWN"
        status = "DOWN"
    
    # Check data collection services
    try:
        # Check crawler service
        import httpx
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{settings.CRAWLER_SERVICE_URL}/health",
                    timeout=2.0
                )
                dependencies["crawler_service"] = "UP" if response.status_code == 200 else "DOWN"
            except Exception:
                dependencies["crawler_service"] = "DOWN"
            
            try:
                response = await client.get(
                    f"{settings.SCRAPER_SERVICE_URL}/health",
                    timeout=2.0
                )
                dependencies["scraper_service"] = "UP" if response.status_code == 200 else "DOWN"
            except Exception:
                dependencies["scraper_service"] = "DOWN"
    except Exception as e:
        logger.error(f"Error checking data collection services: {str(e)}")
        dependencies["crawler_service"] = "UNKNOWN"
        dependencies["scraper_service"] = "UNKNOWN"
    
    response = {
        "status": status,
        "service": "data-preprocessor",
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
            "average_processing_time": 0,
            "total_data_processed_bytes": 0
        },
        "timestamp": time.time()
    }
