"""Base provider interface for LLM implementations."""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import asyncio


@dataclass
class LLMResponse:
    """Response from LLM provider."""
    
    content: str
    model: str
    provider: str
    tokens_used: Optional[int] = None
    cost: Optional[float] = None
    latency: Optional[float] = None
    timestamp: datetime = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass 
class LLMRequest:
    """Request to LLM provider."""
    
    prompt: str
    model: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    system_prompt: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class BaseProvider(ABC):
    """Abstract base class for LLM providers."""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.api_key = config.get("api_key")
        self.base_url = config.get("base_url")
        self.timeout = config.get("timeout", 30)
        self.max_retries = config.get("max_retries", 3)
        self.rate_limit = config.get("rate_limit", 10)
        self._request_count = 0
        self._last_request_time = None
        
    @abstractmethod
    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """Generate response from LLM."""
        pass
    
    @abstractmethod
    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate provider configuration."""
        pass
    
    async def _rate_limit_check(self) -> None:
        """Check and enforce rate limiting."""
        if self._last_request_time is not None:
            time_since_last = (datetime.now() - self._last_request_time).total_seconds()
            min_interval = 60.0 / self.rate_limit  # seconds between requests
            
            if time_since_last < min_interval:
                sleep_time = min_interval - time_since_last
                await asyncio.sleep(sleep_time)
        
        self._last_request_time = datetime.now()
        self._request_count += 1
    
    async def test_connection(self) -> bool:
        """Test connection to provider."""
        try:
            test_request = LLMRequest(
                prompt="Test connection",
                model=self.get_available_models()[0] if self.get_available_models() else "default"
            )
            response = await self.generate_response(test_request)
            return response is not None
        except Exception:
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get provider statistics."""
        return {
            "name": self.name,
            "request_count": self._request_count,
            "rate_limit": self.rate_limit,
            "last_request_time": self._last_request_time
        }