"""
Preprocessing Service

This module provides the core functionality for data preprocessing operations.
"""

import asyncio
import time
import os
import io
from typing import Dict, List, Optional, Any, Union, BinaryIO, Set
from datetime import datetime
import traceback
import json
import uuid
import numpy as np
import pandas as pd
from loguru import logger
from bson import ObjectId

from config import settings
from models.preprocessing_job import (
    PreprocessingJob, 
    PreprocessingJobStatus, 
    DataSourceType,
    DataType,
    TextPreprocessingConfig,
    ImagePreprocessingConfig,
    TabularPreprocessingConfig
)
from models.preprocessing_result import (
    PreprocessingResultCreate,
    DataStats,
    ColumnTransformation
)
from services.database_service import DatabaseService
from services.storage_service import StorageService


class PreprocessingService:
    """Service for data preprocessing operations."""
    
    def __init__(self, db: DatabaseService, storage: StorageService):
        """
        Initialize the preprocessing service.
        
        Args:
            db: Database service
            storage: Storage service
        """
        self.db = db
        self.storage = storage
        self.active_jobs: Dict[str, asyncio.Task] = {}
        self.cancel_flags: Set[str] = set()
        self._job_queue_processor: Optional[asyncio.Task] = None
    
    async def initialize(self):
        """Initialize the preprocessing service."""
        try:
            logger.info("Initializing preprocessing service")
            
            # Ensure database connection
            if not self.db.client:
                await self.db.connect()
            
            # Ensure storage connection
            await self.storage.initialize()
            
            # Reset any stuck jobs
            await self._reset_stuck_jobs()
            
            logger.info("Preprocessing service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize preprocessing service: {str(e)}")
            raise
    
    async def _reset_stuck_jobs(self):
        """Reset any jobs that were left in RUNNING state."""
        try:
            # Get all running jobs
            jobs_data = await self.db.list_jobs(status=PreprocessingJobStatus.RUNNING)
            
            # Reset jobs to PENDING
            for job in jobs_data["jobs"]:
                job_id = str(job.id)
                logger.warning(f"Resetting stuck job {job_id} from RUNNING to PENDING")
                await self.db.update_job_status(
                    job_id,
                    PreprocessingJobStatus.PENDING,
                    error="Job was reset due to service restart"
                )
        except Exception as e:
            logger.error(f"Error resetting stuck jobs: {str(e)}")
    
    async def process_jobs_queue(self):
        """
        Process the jobs queue continuously.
        
        This method runs in the background and processes jobs from the queue.
        """
        try:
            logger.info("Starting job queue processor")
            
            while True:
                try:
                    # Check if we can process more jobs
                    if len(self.active_jobs) >= settings.MAX_CONCURRENT_JOBS:
                        # Wait before checking again
                        await asyncio.sleep(settings.JOB_POLL_INTERVAL)
                        continue
                    
                    # Get next pending job
                    job = await self.db.get_next_pending_job()
                    
                    if not job:
                        # No pending jobs, wait before checking again
                        await asyncio.sleep(settings.JOB_POLL_INTERVAL)
                        continue
                    
                    # Process job
                    job_id = str(job.id)
                    logger.info(f"Starting job {job_id} from queue")
                    
                    # Create task for job
                    task = asyncio.create_task(self.process_job(job_id))
                    self.active_jobs[job_id] = task
                    
                    # Wait a short time before checking for more jobs
                    await asyncio.sleep(0.1)
                except asyncio.CancelledError:
                    logger.info("Job queue processor was cancelled")
                    break
                except Exception as e:
                    logger.error(f"Error in job queue processor: {str(e)}")
                    traceback.print_exc()
                    # Wait before trying again
                    await asyncio.sleep(settings.JOB_POLL_INTERVAL)
        except Exception as e:
            logger.error(f"Fatal error in job queue processor: {str(e)}")
            traceback.print_exc()
    
    async def process_job(self, job_id: str):
        """
        Process a preprocessing job.
        
        Args:
            job_id: The ID of the job to process
        """
        try:
            # Get job from database
            job = await self.db.get_job(job_id)
            
            if not job:
                logger.error(f"Job {job_id} not found")
                return
            
            # Update job status to running
            job = await self.db.update_job_status(
                job_id,
                PreprocessingJobStatus.RUNNING,
                progress=0.0
            )
            
            # Process job based on data type
            if job.config.data_type == DataType.TEXT:
                await self._process_text_job(job)
            elif job.config.data_type == DataType.IMAGE:
                await self._process_image_job(job)
            elif job.config.data_type == DataType.TABULAR:
                await self._process_tabular_job(job)
            elif job.config.data_type == DataType.MIXED:
                await self._process_mixed_job(job)
            else:
                raise ValueError(f"Unsupported data type: {job.config.data_type}")
            
            # Remove job from active jobs
            if job_id in self.active_jobs:
                del self.active_jobs[job_id]
            
            # Remove from cancel flags if present
            if job_id in self.cancel_flags:
                self.cancel_flags.remove(job_id)
            
        except asyncio.CancelledError:
            logger.info(f"Job {job_id} was cancelled")
            
            # Update job status to cancelled
            await self.db.update_job_status(
                job_id,
                PreprocessingJobStatus.CANCELLED
            )
            
            # Remove job from active jobs
            if job_id in self.active_jobs:
                del self.active_jobs[job_id]
            
            # Remove from cancel flags if present
            if job_id in self.cancel_flags:
                self.cancel_flags.remove(job_id)
            
            raise
        except Exception as e:
            logger.error(f"Error processing job {job_id}: {str(e)}")
            traceback.print_exc()
            
            # Update job status to failed
            await self.db.update_job_status(
                job_id,
                PreprocessingJobStatus.FAILED,
                error=str(e)
            )
            
            # Remove job from active jobs
            if job_id in self.active_jobs:
                del self.active_jobs[job_id]
            
            # Remove from cancel flags if present
            if job_id in self.cancel_flags:
                self.cancel_flags.remove(job_id)
    
    async def cancel_job(self, job_id: str):
        """
        Cancel a running preprocessing job.
        
        Args:
            job_id: The ID of the job to cancel
        """
        try:
            # Check if job is running
            if job_id not in self.active_jobs:
                logger.warning(f"Job {job_id} is not running")
                return
            
            # Add to cancel flags
            self.cancel_flags.add(job_id)
            
            # Cancel task
            task = self.active_jobs[job_id]
            task.cancel()
            
            # Wait for task to be cancelled
            try:
                await task
            except asyncio.CancelledError:
                pass
            
            logger.info(f"Cancelled job {job_id}")
        except Exception as e:
            logger.error(f"Error cancelling job {job_id}: {str(e)}")
    
    async def delete_output_files(self, job: PreprocessingJob):
        """
        Delete output files for a job.
        
        Args:
            job: The job to delete output files for
        """
        try:
            if not job.output_path:
                return
            
            # Delete output file
            await self.storage.remove_object(
                settings.MINIO_PROCESSED_BUCKET,
                job.output_path
            )
            
            logger.info(f"Deleted output files for job {job.id}")
        except Exception as e:
            logger.error(f"Error deleting output files for job {job.id}: {str(e)}")
    
    async def _check_cancellation(self, job_id: str):
        """
        Check if a job has been cancelled.
        
        Args:
            job_id: The ID of the job to check
            
        Raises:
            asyncio.CancelledError: If the job has been cancelled
        """
        if job_id in self.cancel_flags:
            raise asyncio.CancelledError()
    
    async def _get_source_data(self, job: PreprocessingJob) -> Any:
        """
        Get source data for a job.
        
        Args:
            job: The job to get source data for
            
        Returns:
            The source data
        """
        job_id = str(job.id)
        source_type = job.source_type
        source_id = job.source_id
        
        # Check cancellation
        await self._check_cancellation(job_id)
        
        # Update progress
        await self.db.update_job_status(
            job_id,
            PreprocessingJobStatus.RUNNING,
            progress=5.0
        )
        
        # Get source data based on source type
        if source_type == DataSourceType.CRAWLER:
            # Get crawler data from MinIO
            # In a real implementation, this would get the data from the crawler service
            # For now, we'll just return a dummy dataframe
            return pd.DataFrame({
                "url": ["https://example.com/1", "https://example.com/2"],
                "title": ["Example 1", "Example 2"],
                "content": ["This is example content 1", "This is example content 2"],
                "timestamp": [datetime.now(), datetime.now()]
            })
        elif source_type == DataSourceType.SCRAPER:
            # Get scraper data from MongoDB
            # In a real implementation, this would get the data from the scraper service
            # For now, we'll just return a dummy dataframe
            return pd.DataFrame({
                "url": ["https://example.com/1", "https://example.com/2"],
                "title": ["Example 1", "Example 2"],
                "content": ["This is example content 1", "This is example content 2"],
                "timestamp": [datetime.now(), datetime.now()]
            })
        elif source_type == DataSourceType.FILE:
            # Get file data from MinIO
            try:
                # Get file from MinIO
                file_data = await self.storage.get_object(
                    settings.MINIO_RAW_BUCKET,
                    source_id
                )
                
                # Determine file type from extension
                if source_id.endswith(".csv"):
                    return pd.read_csv(io.BytesIO(file_data.read()))
                elif source_id.endswith(".parquet"):
                    return pd.read_parquet(io.BytesIO(file_data.read()))
                elif source_id.endswith(".json"):
                    return pd.read_json(io.BytesIO(file_data.read()))
                else:
                    raise ValueError(f"Unsupported file type: {source_id}")
            except Exception as e:
                logger.error(f"Error getting file data: {str(e)}")
                raise
        elif source_type == DataSourceType.DATABASE:
            # Get database data
            # In a real implementation, this would query the database
            # For now, we'll just return a dummy dataframe
            return pd.DataFrame({
                "id": [1, 2],
                "name": ["Example 1", "Example 2"],
                "value": [10, 20],
                "timestamp": [datetime.now(), datetime.now()]
            })
        elif source_type == DataSourceType.API:
            # Get API data
            # In a real implementation, this would call the API
            # For now, we'll just return a dummy dataframe
            return pd.DataFrame({
                "id": [1, 2],
                "name": ["Example 1", "Example 2"],
                "value": [10, 20],
                "timestamp": [datetime.now(), datetime.now()]
            })
        elif source_type == DataSourceType.CUSTOM:
            # Get custom data
            # In a real implementation, this would be customized
            # For now, we'll just return a dummy dataframe
            return pd.DataFrame({
                "id": [1, 2],
                "name": ["Example 1", "Example 2"],
                "value": [10, 20],
                "timestamp": [datetime.now(), datetime.now()]
            })
        else:
            raise ValueError(f"Unsupported source type: {source_type}")
    
    async def _process_text_job(self, job: PreprocessingJob):
        """
        Process a text preprocessing job.
        
        Args:
            job: The job to process
        """
        job_id = str(job.id)
        config = job.config.text_config
        
        if not config:
            raise ValueError("Text preprocessing config is required for text jobs")
        
        # Get source data
        logger.info(f"Getting source data for job {job_id}")
        df = await self._get_source_data(job)
        
        # Check cancellation
        await self._check_cancellation(job_id)
        
        # Update progress
        await self.db.update_job_status(
            job_id,
            PreprocessingJobStatus.RUNNING,
            progress=20.0
        )
        
        # Preprocess text data
        logger.info(f"Preprocessing text data for job {job_id}")
        
        # Track transformations
        transformations = []
        
        # Process each text column
        text_columns = df.select_dtypes(include=['object']).columns
        
        for column in text_columns:
            # Check if column contains text
            if df[column].str.len().mean() > 10:  # Simple heuristic for text columns
                logger.info(f"Processing text column: {column}")
                
                # Apply text preprocessing
                processed_column = df[column].copy()
                
                # Convert to lowercase
                if config.lowercase:
                    processed_column = processed_column.str.lower()
                
                # Remove HTML tags
                if config.remove_html:
                    import re
                    processed_column = processed_column.str.replace(r'<.*?>', ' ', regex=True)
                
                # Remove punctuation
                if config.remove_punctuation:
                    import string
                    translator = str.maketrans('', '', string.punctuation)
                    processed_column = processed_column.apply(
                        lambda x: x.translate(translator) if isinstance(x, str) else x
                    )
                
                # Remove stopwords
                if config.remove_stopwords:
                    try:
                        import nltk
                        from nltk.corpus import stopwords
                        
                        # Download stopwords if needed
                        try:
                            nltk.data.find(f'corpora/stopwords')
                        except LookupError:
                            nltk.download('stopwords')
                        
                        # Get stopwords for the specified language
                        stop_words = set(stopwords.words(config.language))
                        
                        # Add custom stopwords
                        if config.custom_stopwords:
                            stop_words.update(config.custom_stopwords)
                        
                        # Remove stopwords
                        processed_column = processed_column.apply(
                            lambda x: ' '.join([word for word in x.split() if word not in stop_words]) if isinstance(x, str) else x
                        )
                    except Exception as e:
                        logger.warning(f"Error removing stopwords: {str(e)}")
                
                # Lemmatize
                if config.lemmatize:
                    try:
                        import nltk
                        from nltk.stem import WordNetLemmatizer
                        
                        # Download WordNet if needed
                        try:
                            nltk.data.find('corpora/wordnet')
                        except LookupError:
                            nltk.download('wordnet')
                        
                        # Initialize lemmatizer
                        lemmatizer = WordNetLemmatizer()
                        
                        # Lemmatize
                        processed_column = processed_column.apply(
                            lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]) if isinstance(x, str) else x
                        )
                    except Exception as e:
                        logger.warning(f"Error lemmatizing: {str(e)}")
                
                # Stem
                if config.stem:
                    try:
                        from nltk.stem import PorterStemmer
                        
                        # Initialize stemmer
                        stemmer = PorterStemmer()
                        
                        # Stem
                        processed_column = processed_column.apply(
                            lambda x: ' '.join([stemmer.stem(word) for word in x.split()]) if isinstance(x, str) else x
                        )
                    except Exception as e:
                        logger.warning(f"Error stemming: {str(e)}")
                
                # Filter by word length
                if config.min_word_length > 0 or config.max_word_length:
                    processed_column = processed_column.apply(
                        lambda x: ' '.join([
                            word for word in x.split() 
                            if len(word) >= config.min_word_length and 
                            (not config.max_word_length or len(word) <= config.max_word_length)
                        ]) if isinstance(x, str) else x
                    )
                
                # Extract entities
                if config.extract_entities:
                    try:
                        import spacy
                        
                        # Load spaCy model
                        nlp = spacy.load(f"{config.language}_core_web_sm")
                        
                        # Extract entities
                        entity_column = f"{column}_entities"
                        df[entity_column] = df[column].apply(
                            lambda x: [
                                {"text": ent.text, "label": ent.label_} 
                                for ent in nlp(x).ents
                            ] if isinstance(x, str) else []
                        )
                        
                        # Add transformation
                        transformations.append(
                            ColumnTransformation(
                                column_name=entity_column,
                                original_type="text",
                                transformed_type="entity_list",
                                transformation="entity_extraction",
                                parameters={"model": f"{config.language}_core_web_sm"},
                                stats={"entity_count": df[entity_column].apply(len).sum()}
                            )
                        )
                    except Exception as e:
                        logger.warning(f"Error extracting entities: {str(e)}")
                
                # Extract keywords
                if config.extract_keywords:
                    try:
                        from sklearn.feature_extraction.text import TfidfVectorizer
                        
                        # Initialize vectorizer
                        vectorizer = TfidfVectorizer(
                            max_features=10,
                            stop_words=config.language
                        )
                        
                        # Fit vectorizer
                        vectorizer.fit(df[column].fillna(''))
                        
                        # Get feature names
                        feature_names = vectorizer.get_feature_names_out()
                        
                        # Extract keywords
                        keyword_column = f"{column}_keywords"
                        df[keyword_column] = df[column].apply(
                            lambda x: self._extract_keywords(x, vectorizer, feature_names) if isinstance(x, str) else []
                        )
                        
                        # Add transformation
                        transformations.append(
                            ColumnTransformation(
                                column_name=keyword_column,
                                original_type="text",
                                transformed_type="keyword_list",
                                transformation="keyword_extraction",
                                parameters={"max_features": 10},
                                stats={"keyword_count": df[keyword_column].apply(len).sum()}
                            )
                        )
                    except Exception as e:
                        logger.warning(f"Error extracting keywords: {str(e)}")
                
                # Extract sentiment
                if config.extract_sentiment:
                    try:
                        from textblob import TextBlob
                        
                        # Extract sentiment
                        sentiment_column = f"{column}_sentiment"
                        df[sentiment_column] = df[column].apply(
                            lambda x: TextBlob(x).sentiment.polarity if isinstance(x, str) else None
                        )
                        
                        # Add transformation
                        transformations.append(
                            ColumnTransformation(
                                column_name=sentiment_column,
                                original_type="text",
                                transformed_type="float",
                                transformation="sentiment_analysis",
                                parameters={},
                                stats={
                                    "mean": df[sentiment_column].mean(),
                                    "std": df[sentiment_column].std(),
                                    "min": df[sentiment_column].min(),
                                    "max": df[sentiment_column].max()
                                }
                            )
                        )
                    except Exception as e:
                        logger.warning(f"Error extracting sentiment: {str(e)}")
                
                # Replace original column with processed column
                df[column] = processed_column
                
                # Add transformation
                transformations.append(
                    ColumnTransformation(
                        column_name=column,
                        original_type="text",
                        transformed_type="text",
                        transformation="text_preprocessing",
                        parameters={
                            "lowercase": config.lowercase,
                            "remove_html": config.remove_html,
                            "remove_punctuation": config.remove_punctuation,
                            "remove_stopwords": config.remove_stopwords,
                            "lemmatize": config.lemmatize,
                            "stem": config.stem,
                            "min_word_length": config.min_word_length,
                            "max_word_length": config.max_word_length
                        },
                        stats={
                            "mean_length": df[column].str.len().mean(),
                            "mean_word_count": df[column].str.split().str.len().mean()
                        }
                    )
                )
        
        # Check cancellation
        await self._check_cancellation(job_id)
        
        # Update progress
        await self.db.update_job_status(
            job_id,
            PreprocessingJobStatus.RUNNING,
            progress=80.0
        )
        
        # Save processed data
        logger.info(f"Saving processed data for job {job_id}")
        output_path = f"{job_id}/{datetime.now().strftime('%Y%m%d%H%M%S')}.{job.output_format}"
        
        # Save to MinIO
        result = await self.storage.save_dataframe(
            df,
            settings.MINIO_PROCESSED_BUCKET,
            output_path,
            format=job.output_format
        )
        
        # Calculate statistics
        stats = DataStats(
            row_count=len(df),
            column_count=len(df.columns),
            total_size_bytes=result.get("size", 0),
            processed_size_bytes=result.get("size", 0),
            processing_time_seconds=time.time() - job.started_at.timestamp() if job.started_at else 0,
            token_count=df.select_dtypes(include=['object']).apply(lambda x: x.str.split().str.len().sum()).sum(),
            word_count=df.select_dtypes(include=['object']).apply(lambda x: x.str.split().str.len().sum()).sum(),
            sentence_count=df.select_dtypes(include=['object']).apply(lambda x: x.str.count(r'[.!?]')).sum(),
            document_count=len(df),
            vocabulary_size=len(set(' '.join(df.select_dtypes(include=['object']).fillna('').values.flatten()).split())),
            avg_tokens_per_document=df.select_dtypes(include=['object']).apply(lambda x: x.str.split().str.len().mean()).mean()
        )
        
        # Create result
        result = PreprocessingResultCreate(
            job_id=job_id,
            data_type=DataType.TEXT,
            output_path=output_path,
            output_format=job.output_format,
            stats=stats,
            transformations=transformations,
            metadata={
                "source_type": job.source_type,
                "source_id": job.source_id,
                "config": job.config.dict()
            },
            sample_data=df.head(5).to_dict(orient="records")
        )
        
        # Save result
        await self.db.create_result(result)
        
        # Update job status to completed
        await self.db.update_job_status(
            job_id,
            PreprocessingJobStatus.COMPLETED,
            progress=100.0,
            output_path=output_path,
            stats={
                "row_count": stats.row_count,
                "column_count": stats.column_count,
                "processing_time_seconds": stats.processing_time_seconds
            }
        )
        
        logger.info(f"Completed text preprocessing job {job_id}")
    
    def _extract_keywords(self, text, vectorizer, feature_names):
        """
        Extract keywords from text using TF-IDF.
        
        Args:
            text: The text to extract keywords from
            vectorizer: The TF-IDF vectorizer
            feature_names: The feature names
            
        Returns:
            List of keywords
        """
        # Transform text
        tfidf = vectorizer.transform([text])
        
        # Get scores
        scores = zip(feature_names, tfidf.toarray()[0])
        
        # Sort by score
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        # Get top keywords
        return [{"keyword": keyword, "score": float(score)} for keyword, score in sorted_scores if score > 0]
    
    async def _process_image_job(self, job: PreprocessingJob):
        """
        Process an image preprocessing job.
        
        Args:
            job: The job to process
        """
        job_id = str(job.id)
        config = job.config.image_config
        
        if not config:
            raise ValueError("Image preprocessing config is required for image jobs")
        
        # Get source data
        logger.info(f"Getting source data for job {job_id}")
        
        # In a real implementation, this would get image data
        # For now, we'll just simulate image processing
        
        # Check cancellation
        await self._check_cancellation(job_id)
        
        # Update progress
        await self.db.update_job_status(
            job_id,
            PreprocessingJobStatus.RUNNING,
            progress=20.0
        )
        
        # Simulate image processing
        logger.info(f"Preprocessing image data for job {job_id}")
        await asyncio.sleep(2)  # Simulate processing time
        
        # Check cancellation
        await self._check_cancellation(job_id)
        
        # Update progress
        await self.db.update_job_status(
            job_id,
            PreprocessingJobStatus.RUNNING,
            progress=80.0
        )
        
        # Simulate saving processed data
        logger.info(f"Saving processed image data for job {job_id}")
        output_path = f"{job_id}/{datetime.now().strftime('%Y%m%d%H%M%S')}.{job.output_format}"
        
        # Simulate statistics
        stats = DataStats(
            row_count=10,  # Simulated number of images
            file_count=10,
            total_size_bytes=1000000,
            processed_size_bytes=800000,
            compression_ratio=0.8,
            processing_time_seconds=time.time() - job.started_at.timestamp() if job.started_at else 0,
            image_count=10,
            avg_width=224,
            avg_height=224,
            avg_channels=3
        )
        
        # Create result
        result = PreprocessingResultCreate(
            job_id=job_id,
            data_type=DataType.IMAGE,
            output_path=output_path,
            output_format=job.output_format,
            stats=stats,
            transformations=[
                ColumnTransformation(
                    column_name="images",
                    original_type="image",
                    transformed_type="image",
                    transformation="image_preprocessing",
                    parameters={
                        "resize": config.resize,
                        "crop": config.crop,
                        "normalize": config.normalize,
                        "grayscale": config.grayscale,
                        "format": config.format,
                        "quality": config.quality
                    },
                    stats={
                        "image_count": 10,
                        "avg_width": 224,
                        "avg_height": 224,
                        "avg_channels": 3
                    }
                )
            ],
            metadata={
                "source_type": job.source_type,
                "source_id": job.source_id,
                "config": job.config.dict()
            }
        )
        
        # Save result
        await self.db.create_result(result)
        
        # Update job status to completed
        await self.db.update_job_status(
            job_id,
            PreprocessingJobStatus.COMPLETED,
            progress=100.0,
            output_path=output_path,
            stats={
                "image_count": stats.image_count,
                "processing_time_seconds": stats.processing_time_seconds
            }
        )
        
        logger.info(f"Completed image preprocessing job {job_id}")
    
    async def _process_tabular_job(self, job: PreprocessingJob):
        """
        Process a tabular preprocessing job.
        
        Args:
            job: The job to process
        """
        job_id = str(job.id)
        config = job.config.tabular_config
        
        if not config:
            raise ValueError("Tabular preprocessing config is required for tabular jobs")
        
        # Get source data
        logger.info(f"Getting source data for job {job_id}")
        df = await self._get_source_data(job)
        
        # Check cancellation
        await self._check_cancellation(job_id)
        
        # Update progress
        await self.db.update_job_status(
            job_id,
            PreprocessingJobStatus.RUNNING,
            progress=20.0
        )
        
        # Preprocess tabular data
        logger.info(f"Preprocessing tabular data for job {job_id}")
        
        # Track transformations
        transformations = []
        
        # Handle missing values
        if config.handle_missing:
            logger.info(f"Handling missing values with strategy: {config.missing_strategy}")
            
            # Get numerical columns
            numerical_columns = df.select_dtypes(include=['number']).columns
            
            for column in numerical_columns:
                if df[column].isna().any():
                    # Apply missing value strategy
                    if config.missing_strategy == "mean":
                        df[column] = df[column].fillna(df[column].mean())
                    elif config.missing_strategy == "median":
                        df[column] = df[column].fillna(df[column].median())
                    elif config.missing_strategy == "mode":
                        df[column] = df[column].fillna(df[column].mode()[0])
                    elif config.missing_strategy == "zero":
                        df[column] = df[column].fillna(0)
                    else:
                        # Default to mean
                        df[column] = df[column].fillna(df[column].mean())
                    
                    # Add transformation
                    transformations.append(
                        ColumnTransformation(
                            column_name=column,
                            original_type="numerical",
                            transformed_type="numerical",
                            transformation="missing_value_imputation",
                            parameters={"strategy": config.missing_strategy},
                            stats={
                                "missing_count_before": df[column].isna().sum(),
                                "missing_count_after": 0
                            }
                        )
                    )
            
            # Get categorical columns
            categorical_columns = df.select_dtypes(include=['object']).columns
            
            for column in categorical_columns:
                if df[column].isna().any():
                    # Apply missing value strategy
                    if config.missing_strategy == "mode":
                        df[column] = df[column].fillna(df[column].mode()[0] if not df[column].mode().empty else "MISSING")
                    else:
                        # Default to most frequent
                        df[column] = df[column].fillna(df[column].mode()[0] if not df[column].mode().empty else "MISSING")
                    
                    # Add transformation
                    transformations.append(
                        ColumnTransformation(
                            column_name=column,
                            original_type="categorical",
                            transformed_type="categorical",
                            transformation="missing_value_imputation",
                            parameters={"strategy": "mode"},
                            stats={
                                "missing_count_before": df[column].isna().sum(),
                                "missing_count_after": 0
                            }
                        )
                    )
        
        # Encode categorical features
        if config.categorical_encoding != "none":
            logger.info(f"Encoding categorical features with strategy: {config.categorical_encoding}")
            
            # Get categorical columns
            categorical_columns = df.select_dtypes(include=['object']).columns
            
            for column in categorical_columns:
                # Skip columns with too many unique values
                if df[column].nunique() > 100:
                    logger.warning(f"Skipping encoding for column {column} with {df[column].nunique()} unique values")
                    continue
                
                # Apply encoding strategy
                if config.categorical_encoding == "onehot":
                    # One-hot encoding
                    try:
                        from sklearn.preprocessing import OneHotEncoder
                        
                        # Initialize encoder
                        encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
                        
                        # Fit and transform
                        encoded = encoder.fit_transform(df[[column]])
                        
                        # Create new columns
                        categories = encoder.categories_[0]
                        for i, category in enumerate(categories):
                            new_column = f"{column}_{category}"
                            df[new_column] = encoded[:, i]
                            
                            # Add transformation
                            transformations.append(
                                ColumnTransformation(
                                    column_name=new_column,
                                    original_type="categorical",
                                    transformed_type="binary",
                                    transformation="onehot_encoding",
                                    parameters={"source_column": column, "category": category},
                                    stats={
                                        "count": df[new_column].sum(),
                                        "percentage": df[new_column].mean() * 100
                                    }
                                )
                            )
                        
                        # Drop original column
                        df = df.drop(column, axis=1)
                    except Exception as e:
                        logger.warning(f"Error one-hot encoding column {column}: {str(e)}")
                
                elif config.categorical_encoding == "label":
                    # Label encoding
                    try:
                        from sklearn.preprocessing import LabelEncoder
                        
                        # Initialize encoder
                        encoder = LabelEncoder()
                        
                        # Fit and transform
                        df[column] = encoder.fit_transform(df[column].fillna("MISSING"))
                        
                        # Add transformation
                        transformations.append(
                            ColumnTransformation(
                                column_name=column,
                                original_type="categorical",
                                transformed_type="numerical",
                                transformation="label_encoding",
                                parameters={},
                                stats={
                                    "unique_values": df[column].nunique(),
                                    "min": df[column].min(),
                                    "max": df[column].max()
                                }
                            )
                        )
                    except Exception as e:
                        logger.warning(f"Error label encoding column {column}: {str(e)}")
                
                elif config.categorical_encoding == "target":
                    # Target encoding (simplified version)
                    # In a real implementation, this would use proper target encoding with cross-validation
                    logger.warning("Target encoding not fully implemented, using label encoding instead")
                    
                    try:
                        from sklearn.preprocessing import LabelEncoder
                        
                        # Initialize encoder
                        encoder = LabelEncoder()
                        
                        # Fit and transform
                        df[column] = encoder.fit_transform(df[column].fillna("MISSING"))
                        
                        # Add transformation
                        transformations.append(
                            ColumnTransformation(
                                column_name=column,
                                original_type="categorical",
                                transformed_type="numerical",
                                transformation="label_encoding",
                                parameters={},
                                stats={
                                    "unique_values": df[column].nunique(),
                                    "min": df[column].min(),
                                    "max": df[column].max()
                                }
                            )
                        )
                    except Exception as e:
                        logger.warning(f"Error encoding column {column}: {str(e)}")
        
        # Scale numerical features
        if config.numerical_scaling != "none":
            logger.info(f"Scaling numerical features with strategy: {config.numerical_scaling}")
            
            # Get numerical columns
            numerical_columns = df.select_dtypes(include=['number']).columns
            
            for column in numerical_columns:
                # Apply scaling strategy
                if config.numerical_scaling == "standard":
                    # Standard scaling
                    try:
                        from sklearn.preprocessing import StandardScaler
                        
                        # Initialize scaler
                        scaler = StandardScaler()
                        
                        # Fit and transform
                        df[column] = scaler.fit_transform(df[[column]])
                        
                        # Add transformation
                        # Safely extract parameters
                        params = {}
                        try:
                            # Calculate mean and std manually to avoid potential None issues
                            mean_value = df[column].mean()
                            std_value = df[column].std()
                            
                            params["mean"] = float(mean_value)
                            params["std"] = float(std_value if std_value != 0 else 1.0)
                        except Exception as param_error:
                            logger.warning(f"Error extracting standard scaling parameters: {str(param_error)}")
                            params["mean"] = 0.0
                            params["std"] = 1.0
                            
                        transformations.append(
                            ColumnTransformation(
                                column_name=column,
                                original_type="numerical",
                                transformed_type="numerical",
                                transformation="standard_scaling",
                                parameters=params,
                                stats={
                                    "min": float(df[column].min()),
                                    "max": float(df[column].max()),
                                    "mean": float(df[column].mean()),
                                    "std": float(df[column].std())
                                }
                            )
                        )
                    except Exception as e:
                        logger.warning(f"Error standard scaling column {column}: {str(e)}")
                
                elif config.numerical_scaling == "minmax":
                    # Min-max scaling
                    try:
                        from sklearn.preprocessing import MinMaxScaler
                        
                        # Initialize scaler
                        scaler = MinMaxScaler()
                        
                        # Fit and transform
                        df[column] = scaler.fit_transform(df[[column]])
                        
                        # Add transformation
                        # Safely extract parameters
                        params = {}
                        try:
                            # Calculate min and max manually to avoid potential None issues
                            min_value = df[column].min()
                            max_value = df[column].max()
                            
                            params["min"] = float(min_value)
                            params["max"] = float(max_value)
                        except Exception as param_error:
                            logger.warning(f"Error extracting minmax scaling parameters: {str(param_error)}")
                            params["min"] = 0.0
                            params["max"] = 1.0
                            
                        transformations.append(
                            ColumnTransformation(
                                column_name=column,
                                original_type="numerical",
                                transformed_type="numerical",
                                transformation="minmax_scaling",
                                parameters=params,
                                stats={
                                    "min": float(df[column].min()),
                                    "max": float(df[column].max()),
                                    "mean": float(df[column].mean()),
                                    "std": float(df[column].std())
                                }
                            )
                        )
                    except Exception as e:
                        logger.warning(f"Error min-max scaling column {column}: {str(e)}")
                
                elif config.numerical_scaling == "robust":
                    # Robust scaling
                    try:
                        # Calculate median and IQR manually
                        median = df[column].median()
                        q1 = df[column].quantile(0.25)
                        q3 = df[column].quantile(0.75)
                        iqr = q3 - q1
                        
                        # Apply robust scaling manually
                        if iqr != 0:  # Avoid division by zero
                            df[column] = (df[column] - median) / iqr
                        else:
                            # If IQR is 0, just center the data
                            df[column] = df[column] - median
                        
                        # Add transformation
                        transformations.append(
                            ColumnTransformation(
                                column_name=column,
                                original_type="numerical",
                                transformed_type="numerical",
                                transformation="robust_scaling",
                                parameters={
                                    "median": float(median),
                                    "iqr": float(iqr if iqr != 0 else 1.0)
                                },
                                stats={
                                    "min": float(df[column].min()),
                                    "max": float(df[column].max()),
                                    "median": float(df[column].median()),
                                    "q1": float(q1),
                                    "q3": float(q3)
                                }
                            )
                        )
                    except Exception as e:
                        logger.warning(f"Error robust scaling column {column}: {str(e)}")
        
        # Drop specified columns
        if config.drop_columns:
            logger.info(f"Dropping columns: {config.drop_columns}")
            
            # Drop columns
            columns_to_drop = [col for col in config.drop_columns if col in df.columns]
            df = df.drop(columns_to_drop, axis=1)
        
        # Keep only specified columns
        if config.keep_columns:
            logger.info(f"Keeping only columns: {config.keep_columns}")
            
            # Keep only specified columns
            columns_to_keep = [col for col in config.keep_columns if col in df.columns]
            df = df[columns_to_keep]
        
        # Check cancellation
        await self._check_cancellation(job_id)
        
        # Update progress
        await self.db.update_job_status(
            job_id,
            PreprocessingJobStatus.RUNNING,
            progress=80.0
        )
        
        # Save processed data
        logger.info(f"Saving processed data for job {job_id}")
        output_path = f"{job_id}/{datetime.now().strftime('%Y%m%d%H%M%S')}.{job.output_format}"
        
        # Save to MinIO
        result = await self.storage.save_dataframe(
            df,
            settings.MINIO_PROCESSED_BUCKET,
            output_path,
            format=job.output_format
        )
        
        # Calculate statistics
        stats = DataStats(
            row_count=len(df),
            column_count=len(df.columns),
            total_size_bytes=result.get("size", 0),
            processed_size_bytes=result.get("size", 0),
            processing_time_seconds=time.time() - job.started_at.timestamp() if job.started_at else 0,
            missing_values={col: int(df[col].isna().sum()) for col in df.columns},
            column_types={col: str(df[col].dtype) for col in df.columns},
            numerical_stats={
                col: {
                    "min": float(df[col].min()),
                    "max": float(df[col].max()),
                    "mean": float(df[col].mean()),
                    "median": float(df[col].median()),
                    "std": float(df[col].std())
                } for col in df.select_dtypes(include=['number']).columns
            },
            categorical_stats={
                col: {
                    str(val): int(count) for val, count in df[col].value_counts().items()
                } for col in df.select_dtypes(include=['object']).columns
            }
        )
        
        # Create result
        result = PreprocessingResultCreate(
            job_id=job_id,
            data_type=DataType.TABULAR,
            output_path=output_path,
            output_format=job.output_format,
            stats=stats,
            transformations=transformations,
            metadata={
                "source_type": job.source_type,
                "source_id": job.source_id,
                "config": job.config.dict()
            },
            sample_data=df.head(5).to_dict(orient="records")
        )
        
        # Save result
        await self.db.create_result(result)
        
        # Update job status to completed
        await self.db.update_job_status(
            job_id,
            PreprocessingJobStatus.COMPLETED,
            progress=100.0,
            output_path=output_path,
            stats={
                "row_count": stats.row_count,
                "column_count": stats.column_count,
                "processing_time_seconds": stats.processing_time_seconds
            }
        )
        
        logger.info(f"Completed tabular preprocessing job {job_id}")
    
    async def _process_mixed_job(self, job: PreprocessingJob):
        """
        Process a mixed data preprocessing job.
        
        Args:
            job: The job to process
        """
        job_id = str(job.id)
        
        # Get source data
        logger.info(f"Getting source data for job {job_id}")
        df = await self._get_source_data(job)
        
        # Check cancellation
        await self._check_cancellation(job_id)
        
        # Update progress
        await self.db.update_job_status(
            job_id,
            PreprocessingJobStatus.RUNNING,
            progress=20.0
        )
        
        # Process text columns
        if job.config.text_config:
            logger.info("Processing text columns")
            # Create a text job with the same data
            text_job = PreprocessingJob(
                **job.dict(),
                config=job.config.dict()
            )
            text_job.config.data_type = DataType.TEXT
            
            # Process text columns
            await self._process_text_job(text_job)
        
        # Process tabular columns
        if job.config.tabular_config:
            logger.info("Processing tabular columns")
            # Create a tabular job with the same data
            tabular_job = PreprocessingJob(
                **job.dict(),
                config=job.config.dict()
            )
            tabular_job.config.data_type = DataType.TABULAR
            
            # Process tabular columns
            await self._process_tabular_job(tabular_job)
        
        # Process image columns
        if job.config.image_config:
            logger.info("Processing image columns")
            # Create an image job with the same data
            image_job = PreprocessingJob(
                **job.dict(),
                config=job.config.dict()
            )
            image_job.config.data_type = DataType.IMAGE
            
            # Process image columns
            await self._process_image_job(image_job)
        
        # Update job status to completed
        await self.db.update_job_status(
            job_id,
            PreprocessingJobStatus.COMPLETED,
            progress=100.0
        )
        
        logger.info(f"Completed mixed preprocessing job {job_id}")
