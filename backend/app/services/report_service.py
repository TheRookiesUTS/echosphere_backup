"""
Report service for processing citizen reports
Handles report validation, storage, and analysis
"""
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from app.models.schemas import ReportSubmission, ReportType, SeverityLevel, ReportCategory
from app.services.ai_service import ai_service

logger = logging.getLogger(__name__)


class ReportService:
    """Service for processing citizen reports"""
    
    def __init__(self):
        # In a real implementation, this would connect to the database
        self.reports_db = {}  # Mock database
        self.statistics_cache = {}
    
    async def process_report(self, report: ReportSubmission, report_id: str) -> Dict[str, Any]:
        """
        Process a submitted report
        
        Steps:
        1. Validate report data
        2. Enhance with AI analysis if applicable
        3. Store in database
        4. Categorize and prioritize
        5. Notify relevant stakeholders
        """
        try:
            # Enhanced report data
            enhanced_report = {
                "id": report_id,
                "submitted_at": datetime.utcnow(),
                "status": "submitted",
                "priority_score": self._calculate_priority_score(report),
                "ai_analysis": None,
                "original_data": report.dict()
            }
            
            # AI analysis for certain report types
            if report.report_type in [ReportType.ENVIRONMENTAL_ISSUE, ReportType.URBAN_PLANNING]:
                enhanced_report["ai_analysis"] = await self._analyze_report_with_ai(report)
            
            # Store in database (mock)
            self.reports_db[report_id] = enhanced_report
            
            # Update statistics
            self._update_statistics(report)
            
            logger.info(f"Report {report_id} processed successfully")
            
            return {
                "report_id": report_id,
                "priority_score": enhanced_report["priority_score"],
                "ai_analysis": enhanced_report["ai_analysis"]
            }
            
        except Exception as e:
            logger.error(f"Error processing report {report_id}: {str(e)}")
            raise
    
    def _calculate_priority_score(self, report: ReportSubmission) -> int:
        """
        Calculate priority score based on report characteristics
        
        Factors:
        - Severity level
        - Report type
        - Category
        - Location (if in high-risk areas)
        """
        score = 0
        
        # Severity scoring
        severity_scores = {
            SeverityLevel.LOW: 1,
            SeverityLevel.MEDIUM: 3,
            SeverityLevel.HIGH: 7,
            SeverityLevel.CRITICAL: 10
        }
        score += severity_scores.get(report.severity, 1)
        
        # Report type scoring
        type_scores = {
            ReportType.ENVIRONMENTAL_ISSUE: 5,
            ReportType.FLOOD_RISK: 8,
            ReportType.HEAT_STRESS: 6,
            ReportType.AIR_QUALITY: 7,
            ReportType.INFRASTRUCTURE: 6,
            ReportType.GREEN_SPACE: 3,
            ReportType.URBAN_PLANNING: 4
        }
        score += type_scores.get(report.report_type, 3)
        
        # Category scoring
        category_scores = {
            ReportCategory.HEAT_ISLAND: 6,
            ReportCategory.FLOODING: 8,
            ReportCategory.AIR_POLLUTION: 7,
            ReportCategory.GREEN_COVERAGE: 4,
            ReportCategory.TRANSPORTATION: 5,
            ReportCategory.WASTE_MANAGEMENT: 5,
            ReportCategory.ENERGY: 4,
            ReportCategory.OTHER: 2
        }
        score += category_scores.get(report.category, 3)
        
        return min(score, 20)  # Cap at 20
    
    async def _analyze_report_with_ai(self, report: ReportSubmission) -> Dict[str, Any]:
        """
        Use AI to analyze the report and provide insights
        """
        try:
            # Create a prompt for AI analysis
            prompt = f"""
            Analyze this citizen report for urban planning insights:
            
            Report Type: {report.report_type}
            Category: {report.category}
            Severity: {report.severity}
            Title: {report.title}
            Description: {report.description}
            Location: {report.location.address}
            
            Provide:
            1. Key insights about the reported issue
            2. Potential causes or contributing factors
            3. Suggested immediate actions
            4. Long-term planning recommendations
            5. Related environmental factors to consider
            
            Focus on actionable insights for urban planners and city leaders.
            """
            
            # Get AI analysis
            ai_response = await ai_service.chat(
                message=prompt,
                chat_history=[],
                area_data=None
            )
            
            return {
                "analysis": ai_response,
                "generated_at": datetime.utcnow(),
                "model": "deepseek-chat-v3.1"
            }
            
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            return {
                "analysis": "AI analysis temporarily unavailable",
                "error": str(e),
                "generated_at": datetime.utcnow()
            }
    
    def _update_statistics(self, report: ReportSubmission) -> None:
        """Update report statistics"""
        try:
            # Initialize statistics if needed
            if not self.statistics_cache:
                self.statistics_cache = {
                    "total_reports": 0,
                    "by_category": {},
                    "by_severity": {},
                    "by_type": {},
                    "recent_trends": []
                }
            
            # Update counts
            self.statistics_cache["total_reports"] += 1
            
            # Update category counts
            category = report.category
            self.statistics_cache["by_category"][category] = \
                self.statistics_cache["by_category"].get(category, 0) + 1
            
            # Update severity counts
            severity = report.severity
            self.statistics_cache["by_severity"][severity] = \
                self.statistics_cache["by_severity"].get(severity, 0) + 1
            
            # Update type counts
            report_type = report.report_type
            self.statistics_cache["by_type"][report_type] = \
                self.statistics_cache["by_type"].get(report_type, 0) + 1
            
            # Update trends (keep last 30 days)
            today = datetime.utcnow().date()
            self.statistics_cache["recent_trends"].append({
                "date": today,
                "category": category,
                "severity": severity,
                "count": 1
            })
            
            # Keep only last 30 days
            cutoff_date = today - timedelta(days=30)
            self.statistics_cache["recent_trends"] = [
                trend for trend in self.statistics_cache["recent_trends"]
                if trend["date"] >= cutoff_date
            ]
            
        except Exception as e:
            logger.error(f"Error updating statistics: {str(e)}")
    
    async def get_report_status(self, report_id: str) -> Dict[str, Any]:
        """Get status of a specific report"""
        try:
            if report_id not in self.reports_db:
                raise ValueError("Report not found")
            
            report = self.reports_db[report_id]
            
            return {
                "report_id": report_id,
                "status": report["status"],
                "submitted_at": report["submitted_at"],
                "last_updated": datetime.utcnow(),
                "priority_score": report["priority_score"],
                "title": report["original_data"]["title"],
                "category": report["original_data"]["category"],
                "severity": report["original_data"]["severity"]
            }
            
        except Exception as e:
            logger.error(f"Error getting report status: {str(e)}")
            raise
    
    async def get_report_statistics(self) -> Dict[str, Any]:
        """Get comprehensive report statistics"""
        try:
            # Ensure statistics are initialized
            if not self.statistics_cache:
                self.statistics_cache = {
                    "total_reports": 0,
                    "by_category": {},
                    "by_severity": {},
                    "by_type": {},
                    "recent_trends": []
                }
            
            # Calculate additional statistics
            stats = self.statistics_cache.copy()
            
            # Add computed fields
            stats["average_priority"] = self._calculate_average_priority()
            stats["most_common_category"] = max(
                stats["by_category"].items(), 
                key=lambda x: x[1], 
                default=("none", 0)
            )[0]
            stats["most_common_severity"] = max(
                stats["by_severity"].items(), 
                key=lambda x: x[1], 
                default=("none", 0)
            )[0]
            stats["reports_last_7_days"] = self._count_recent_reports(7)
            stats["reports_last_30_days"] = self._count_recent_reports(30)
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            raise
    
    def _calculate_average_priority(self) -> float:
        """Calculate average priority score"""
        if not self.reports_db:
            return 0.0
        
        total_score = sum(report["priority_score"] for report in self.reports_db.values())
        return total_score / len(self.reports_db)
    
    def _count_recent_reports(self, days: int) -> int:
        """Count reports from the last N days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        return sum(
            1 for report in self.reports_db.values()
            if report["submitted_at"] >= cutoff_date
        )
    
    async def get_recent_reports(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent reports for public viewing"""
        try:
            # Sort reports by submission date (newest first)
            sorted_reports = sorted(
                self.reports_db.items(),
                key=lambda x: x[1]["submitted_at"],
                reverse=True
            )
            
            # Return limited number with public-safe information
            recent_reports = []
            for report_id, report_data in sorted_reports[:limit]:
                original = report_data["original_data"]
                recent_reports.append({
                    "id": report_id,
                    "title": original["title"],
                    "category": original["category"],
                    "severity": original["severity"],
                    "location": original["location"]["address"],
                    "submitted_at": report_data["submitted_at"],
                    "status": report_data["status"]
                })
            
            return recent_reports
            
        except Exception as e:
            logger.error(f"Error getting recent reports: {str(e)}")
            raise


# Global service instance
report_service = ReportService()

