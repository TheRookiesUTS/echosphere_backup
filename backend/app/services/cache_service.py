"""
Simple in-memory cache service
Will be replaced with Redis/PostgreSQL by teammate later
"""
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import json


class CacheItem:
    """Cache item with expiration"""
    def __init__(self, value: Any, ttl: int):
        self.value = value
        self.expires_at = datetime.utcnow() + timedelta(seconds=ttl)
    
    def is_expired(self) -> bool:
        return datetime.utcnow() > self.expires_at


class InMemoryCache:
    """Simple in-memory cache for demo purposes"""
    
    def __init__(self):
        self._cache: Dict[str, CacheItem] = {}
        self._chat_history: Dict[str, List[Dict[str, str]]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self._cache:
            item = self._cache[key]
            if not item.is_expired():
                return item.value
            else:
                # Clean up expired item
                del self._cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl: int = 3600):
        """Set value in cache with TTL"""
        self._cache[key] = CacheItem(value, ttl)
    
    def delete(self, key: str):
        """Delete key from cache"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self):
        """Clear entire cache"""
        self._cache.clear()
        self._chat_history.clear()
    
    # Chat history management
    def get_chat_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get chat history for session"""
        return self._chat_history.get(session_id, [])
    
    def save_chat_message(self, session_id: str, role: str, content: str):
        """Save chat message to history"""
        if session_id not in self._chat_history:
            self._chat_history[session_id] = []
        
        self._chat_history[session_id].append({
            "role": role,
            "content": content
        })
        
        # Keep only last 20 messages per session (memory management)
        if len(self._chat_history[session_id]) > 20:
            self._chat_history[session_id] = self._chat_history[session_id][-20:]
    
    def clear_chat_history(self, session_id: str):
        """Clear chat history for session"""
        if session_id in self._chat_history:
            del self._chat_history[session_id]


# Global cache instance
cache = InMemoryCache()

