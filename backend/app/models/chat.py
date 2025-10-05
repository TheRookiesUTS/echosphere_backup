"""
Chat history models for AI conversation tracking
Stores user-AI interactions for context and history
"""
from sqlalchemy import Column, String, Text, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from typing import Dict, List, Any, Optional
from app.models.base import Base, TimestampMixin, generate_uuid


class ChatHistory(Base, TimestampMixin):
    """
    AI chatbot conversation history
    
    Stores conversations between users and the AI assistant, grouped
    by session. Optionally linked to specific areas for context-aware
    responses. Optimized for quick session-based retrieval.
    
    Attributes:
        id: Unique identifier (UUID v4)
        session_id: Session identifier to group conversations
        area_id: Optional link to analyzed area
        user_message: User's message text
        ai_response: AI assistant's response text
        context_data: Additional context as JSON (metrics, analysis, etc.)
        model_used: AI model identifier
    """
    __tablename__ = "chat_history"
    
    id = Column(
        String(36), 
        primary_key=True, 
        default=generate_uuid,
        comment="Unique chat message identifier (UUID)"
    )
    session_id = Column(
        String(100), 
        nullable=False,
        comment="Session ID to group related conversations"
    )
    area_id = Column(
        String(36), 
        ForeignKey("areas.id", ondelete="CASCADE"), 
        nullable=True,
        comment="Optional reference to related area"
    )
    
    # Message content
    user_message = Column(
        Text, 
        nullable=False,
        comment="User's message text"
    )
    ai_response = Column(
        Text, 
        nullable=False,
        comment="AI assistant's response text"
    )
    
    # Context data for better AI responses
    context_data = Column(
        JSON, 
        nullable=True,
        comment="Additional context (metrics, analysis summary, etc.)"
    )
    
    # AI model information
    model_used = Column(
        String(50), 
        default="deepseek/deepseek-chat",
        comment="AI model identifier"
    )
    
    # Relationships
    area = relationship("Area", back_populates="chat_history")
    
    # Indexes for fast session queries
    __table_args__ = (
        # Primary index for retrieving chat history by session
        Index('idx_session_time', 'session_id', 'created_at'),
        # Index for area-specific chat queries
        Index('idx_chat_area', 'area_id', 'created_at'),
    )
    
    def __repr__(self) -> str:
        message_preview = self.user_message[:50] + "..." if len(self.user_message) > 50 else self.user_message
        return f"<ChatHistory(session={self.session_id}, msg='{message_preview}')>"
    
    def to_dict(self, include_context: bool = False) -> Dict[str, Any]:
        """
        Convert chat message to dictionary
        
        Args:
            include_context: Whether to include context_data
        
        Returns:
            dict: Chat message as dictionary
        """
        data = {
            "id": self.id,
            "session_id": self.session_id,
            "area_id": self.area_id,
            "user_message": self.user_message,
            "ai_response": self.ai_response,
            "model_used": self.model_used,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        
        if include_context and self.context_data:
            data["context_data"] = self.context_data
        
        return data
    
    @classmethod
    def format_for_ai(cls, messages: List['ChatHistory']) -> List[Dict[str, str]]:
        """
        Format chat history for AI model consumption
        
        Args:
            messages: List of ChatHistory objects
        
        Returns:
            list: Formatted messages for AI (OpenAI format)
        """
        formatted = []
        for msg in messages:
            formatted.append({
                "role": "user",
                "content": msg.user_message
            })
            formatted.append({
                "role": "assistant",
                "content": msg.ai_response
            })
        return formatted

