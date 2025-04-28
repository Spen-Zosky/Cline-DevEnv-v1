"""
Data Preprocessor Service

This service is responsible for preprocessing data collected by the data collection services
before it is used for machine learning or other analytical purposes.
"""

# pyright: reportUnusedCallResult=false

import os
import sys
import time
import asyncio
from typing import Dict, List, Optional, Any
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from dotenv import load_dotenv

# Import local modules
from config import settings
from models.preprocessing_job import PreprocessingJob, PreprocessingJobCreate, PreprocessingJobStatus
from models.preprocessing_result import PreprocessingResult
from services.preprocessing_service import PreprocessingService
from services.database_service import DatabaseService
from services.storage_service import StorageService
from api.health import router as health_router
from api.preprocessor import router as preprocessor_router

# Load environment variables
load_dotenv()

# Configure logger
logger.remove()
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level=settings.LOG_LEVEL,
    colorize=True,
)
logger.add(
    "logs/preprocessor.log",
    rotation="10 MB",
    retention="7 days",
    level=settings.LOG_LEVEL,
)

# Create FastAPI app
app = FastAPI(
    title="Data Preprocessor Service",
    description="Service for preprocessing data collected by the data collection services",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database dependency
def get_db():
    db = DatabaseService()
    try:
        yield db
    finally:
        db.close()

# Storage dependency
def get_storage():
    storage = StorageService()
    try:
        yield storage
    finally:
        storage.close()

# Preprocessing service dependency
def get_preprocessing_service(
    db: DatabaseService = Depends(get_db),
    storage: StorageService = Depends(get_storage)
):
    return PreprocessingService(db, storage)

# Include routers
app.include_router(health_router)
app.include_router(
    preprocessor_router,
    prefix="/api/preprocessor",
    dependencies=[Depends(get_db), Depends(get_storage)]
)

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Data Preprocessor Service")
    
    # Initialize database connection
    db = DatabaseService()
    await db.connect()
    
    # Initialize storage service
    storage = StorageService()
    await storage.initialize()
    
    # Initialize preprocessing service
    preprocessing_service = PreprocessingService(db, storage)
    await preprocessing_service.initialize()
    
    # Start background task to process jobs
    # We intentionally don't await this task as it's meant to run in the background
    # The task will be kept alive by the event loop as long as the application is running
    # pylint: disable=unused-variable
    
    # Create a background task that will run continuously
    background_task: asyncio.Task = asyncio.create_task(preprocessing_service.process_jobs_queue())  # pyright: ignore[reportUnusedCallResult]
    
    # Store the task in app state to prevent it from being garbage collected
    app.state.background_tasks = getattr(app.state, "background_tasks", []) + [background_task]
    
    logger.info("Data Preprocessor Service started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    logger.info("Shutting down Data Preprocessor Service")
    
    # Close database connection
    db = DatabaseService()
    await db.close()
    
    # Close storage connection
    storage = StorageService()
    storage.close()  # This is not an async function, so no await needed
    
    logger.info("Data Preprocessor Service shut down successfully")

if __name__ == "__main__":
    # Run the FastAPI app with Uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
