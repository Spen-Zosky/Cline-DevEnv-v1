"""
Data Scraper Service

This service is responsible for scraping websites and extracting structured data
for the AI Research Platform.
"""

import os
import sys
import time
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from dotenv import load_dotenv

# Import local modules
from config import settings
from models.scrape_job import ScrapeJob, ScrapeJobCreate, ScrapeJobStatus
from models.scrape_result import ScrapeResult
from services.scraper_service import ScraperService
from services.database_service import DatabaseService
from api.health import router as health_router
from api.scraper import router as scraper_router

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
    "logs/scraper.log",
    rotation="10 MB",
    retention="7 days",
    level=settings.LOG_LEVEL,
)

# Create FastAPI app
app = FastAPI(
    title="Data Scraper Service",
    description="Service for scraping websites and extracting structured data",
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

# Scraper service dependency
def get_scraper_service(db: DatabaseService = Depends(get_db)):
    return ScraperService(db)

# Include routers
app.include_router(health_router)
app.include_router(scraper_router, prefix="/api/scraper", dependencies=[Depends(get_db)])

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting Data Scraper Service")
    
    # Initialize database connection
    db = DatabaseService()
    await db.connect()
    
    # Initialize scraper service
    scraper_service = ScraperService(db)
    await scraper_service.initialize()
    
    logger.info("Data Scraper Service started successfully")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up resources on shutdown"""
    logger.info("Shutting down Data Scraper Service")
    
    # Close database connection
    db = DatabaseService()
    await db.close()
    
    logger.info("Data Scraper Service shut down successfully")

if __name__ == "__main__":
    # Run the FastAPI app with Uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
