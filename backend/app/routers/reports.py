"""
Reports API endpoints
Handles citizen reporting and environmental issue submissions
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List, Optional
from app.models.schemas import ReportSubmission, ReportResponse
from app.services.report_service import report_service
import logging
import uuid
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.post("/submit", response_model=ReportResponse)
async def submit_report(report: ReportSubmission):
    """
    Submit a citizen report for environmental issues or urban planning concerns
    
    This endpoint allows citizens to report:
    - Environmental issues (heat islands, air quality, flooding)
    - Urban planning suggestions
    - Infrastructure problems
    - Green space opportunities
    
    The report will be:
    - Stored in the database for analysis
    - Categorized and prioritized
    - Made available to urban planners
    - Used for trend analysis and AI recommendations
    """
    try:
        logger.info(f"New report submission: {report.title} by {report.reporter_name}")
        
        # Generate unique report ID
        report_id = str(uuid.uuid4())
        
        # Process the report through the service
        result = await report_service.process_report(report, report_id)
        
        # Determine estimated review time based on severity
        review_times = {
            "critical": "24 hours",
            "high": "3 days", 
            "medium": "1 week",
            "low": "2 weeks"
        }
        
        return ReportResponse(
            report_id=report_id,
            status="submitted",
            message=f"Report submitted successfully. Reference ID: {report_id}",
            estimated_review_time=review_times.get(report.severity, "1 week")
        )
        
    except Exception as e:
        logger.error(f"Error processing report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to process report. Please try again later."
        )


@router.get("/status/{report_id}")
async def get_report_status(report_id: str):
    """
    Get the status of a submitted report
    
    Returns:
    - Current status (submitted, under_review, resolved, closed)
    - Last updated timestamp
    - Any comments or updates from reviewers
    """
    try:
        status = await report_service.get_report_status(report_id)
        return status
    except Exception as e:
        logger.error(f"Error fetching report status: {str(e)}")
        raise HTTPException(
            status_code=404,
            detail="Report not found or error retrieving status"
        )


@router.post("/upload-images")
async def upload_images(files: List[UploadFile] = File(...)):
    """
    Upload images for reports
    
    Supports multiple image uploads with validation:
    - File types: JPEG, PNG, WebP
    - Max size: 10MB per file
    - Max files: 5 per report
    """
    try:
        # Validate files
        if len(files) > 5:
            raise HTTPException(
                status_code=400,
                detail="Maximum 5 images allowed per report"
            )
        
        uploaded_urls = []
        
        for file in files:
            # Validate file type
            if not file.content_type.startswith('image/'):
                raise HTTPException(
                    status_code=400,
                    detail=f"File {file.filename} is not a valid image"
                )
            
            # Validate file size (10MB max)
            content = await file.read()
            if len(content) > 10 * 1024 * 1024:  # 10MB
                raise HTTPException(
                    status_code=400,
                    detail=f"File {file.filename} is too large (max 10MB)"
                )
            
            # In a real implementation, you would upload to cloud storage
            # For now, we'll simulate by returning a mock URL
            mock_url = f"/uploads/reports/{uuid.uuid4()}_{file.filename}"
            uploaded_urls.append(mock_url)
            
            logger.info(f"Image uploaded: {file.filename} -> {mock_url}")
        
        return {
            "uploaded_files": uploaded_urls,
            "message": f"Successfully uploaded {len(uploaded_urls)} images"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading images: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to upload images"
        )


@router.get("/statistics")
async def get_report_statistics():
    """
    Get reporting statistics for dashboard
    
    Returns:
    - Total reports submitted
    - Reports by category
    - Reports by severity
    - Recent trends
    """
    try:
        stats = await report_service.get_report_statistics()
        return stats
    except Exception as e:
        logger.error(f"Error fetching report statistics: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch statistics"
        )


@router.get("/recent")
async def get_recent_reports(limit: int = 10):
    """
    Get recent reports for public viewing
    
    Returns recent reports with basic information:
    - Title and category
    - Location (general area)
    - Status
    - Submission date
    """
    try:
        recent_reports = await report_service.get_recent_reports(limit)
        return recent_reports
    except Exception as e:
        logger.error(f"Error fetching recent reports: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch recent reports"
        )

