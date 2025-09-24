"""OpenAI provider implementation."""

import os
import openai
from typing import Dict, Any, List, Optional
from datetime import datetime
import asyncio
import time

from .base import BaseProvider, LLMRequest, LLMResponse


class OpenAIProvider(BaseProvider):
    """OpenAI LLM provider implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("openai", config)
        
        # Initialize OpenAI client
        self.api_key = config.get("api_key") or os.getenv("OPENAI_API_KEY")
        self.base_url = config.get("base_url", "https://api.openai.com/v1")
        self.model = config.get("model", "gpt-3.5-turbo")
        
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
            
        self.client = openai.AsyncOpenAI(
            api_key=self.api_key,
            base_url=self.base_url,
            timeout=self.timeout
        )
        
    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """Generate response using OpenAI API."""
        await self._rate_limit_check()
        
        start_time = time.time()
        
        try:
            # Prepare messages
            messages = []
            if request.system_prompt:
                messages.append({"role": "system", "content": request.system_prompt})
            messages.append({"role": "user", "content": request.prompt})
            
            # Make API call with retries
            for attempt in range(self.max_retries):
                try:
                    response = await self.client.chat.completions.create(
                        model=request.model or self.model,
                        messages=messages,
                        temperature=request.temperature,
                        max_tokens=request.max_tokens,
                    )
                    
                    latency = time.time() - start_time
                    
                    return LLMResponse(
                        content=response.choices[0].message.content,
                        model=response.model,
                        provider=self.name,
                        tokens_used=response.usage.total_tokens if response.usage else None,
                        latency=latency,
                        timestamp=datetime.now(),
                        metadata={
                            "finish_reason": response.choices[0].finish_reason,
                            "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
                            "completion_tokens": response.usage.completion_tokens if response.usage else None,
                            "attempt": attempt + 1
                        }
                    )
                    
                except openai.RateLimitError as e:
                    if attempt < self.max_retries - 1:
                        wait_time = 2 ** attempt  # Exponential backoff
                        await asyncio.sleep(wait_time)
                        continue
                    raise e
                    
                except openai.APITimeoutError as e:
                    if attempt < self.max_retries - 1:
                        await asyncio.sleep(1)
                        continue
                    raise e
                    
        except Exception as e:
            return LLMResponse(
                content=f"Error: {str(e)}",
                model=request.model or self.model,
                provider=self.name,
                latency=time.time() - start_time,
                timestamp=datetime.now(),
                metadata={"error": str(e), "error_type": type(e).__name__}
            )
    
    def get_available_models(self) -> List[str]:
        """Get list of available OpenAI models."""
        return [
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-16k",
            "gpt-4",
            "gpt-4-turbo-preview",
            "gpt-4-32k"
        ]
    
    def validate_config(self) -> bool:
        """Validate OpenAI configuration."""
        if not self.api_key:
            return False
        if not self.base_url:
            return False
        if self.model not in self.get_available_models():
            return False
        return True
    
    async def get_model_info(self, model: str) -> Dict[str, Any]:
        """Get information about a specific model."""
        try:
            # This would typically call the models API endpoint
            # For now, return static info
            model_info = {
                "gpt-3.5-turbo": {
                    "max_tokens": 4096,
                    "cost_per_1k_tokens": {"input": 0.0015, "output": 0.002},
                    "description": "Most capable GPT-3.5 model"
                },
                "gpt-4": {
                    "max_tokens": 8192,
                    "cost_per_1k_tokens": {"input": 0.03, "output": 0.06},
                    "description": "More capable than GPT-3.5"
                },
                "gpt-4-turbo-preview": {
                    "max_tokens": 128000,
                    "cost_per_1k_tokens": {"input": 0.01, "output": 0.03},
                    "description": "Latest GPT-4 Turbo model"
                }
            }
            return model_info.get(model, {})
        except Exception:
            return {}
    
    def calculate_cost(self, tokens_used: int, model: str) -> float:
        """Calculate cost based on token usage."""
        try:
            # Simple cost calculation - would need more sophisticated logic
            # for different models and input/output token distinction
            cost_per_1k = {
                "gpt-3.5-turbo": 0.002,
                "gpt-4": 0.06,
                "gpt-4-turbo-preview": 0.03
            }
            
            base_cost = cost_per_1k.get(model, 0.002)
            return (tokens_used / 1000) * base_cost
        except Exception:
            return 0.0