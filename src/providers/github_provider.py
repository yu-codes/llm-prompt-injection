"""GitHub Models provider implementation."""

import aiohttp
from typing import Dict, Any, List
from src.providers.base import BaseProvider, LLMRequest, LLMResponse


class GitHubProvider(BaseProvider):
    """GitHub Models API provider implementation."""
    
    def __init__(self, token: str, model: str = "gpt-4o-mini", 
                 endpoint: str = "https://models.inference.ai.azure.com"):
        """Initialize GitHub Models provider."""
        # 構建配置字典以符合BaseProvider要求
        config = {
            "api_key": token,
            "base_url": endpoint,
            "model": model
        }
        super().__init__("github", config)
        
        self.token = token
        self.model = model
        self.endpoint = endpoint
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    async def generate_response(self, request: LLMRequest) -> LLMResponse:
        """Generate response using GitHub Models API."""
        # 構建消息列表
        messages = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        messages.append({"role": "user", "content": request.prompt})
        
        payload = {
            "model": request.model or self.model,
            "messages": messages,
            "max_tokens": request.max_tokens or 1000,
            "temperature": request.temperature
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.endpoint}/chat/completions",
                headers=self.headers,
                json=payload
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data["choices"][0]["message"]["content"]
                    return LLMResponse(
                        content=content,
                        model=request.model or self.model,
                        usage=data.get("usage", {}),
                        metadata={"response_data": data}
                    )
                else:
                    error_text = await response.text()
                    return LLMResponse(
                        content=f"Error: {error_text}",
                        model=request.model or self.model,
                        error=f"GitHub Models API error: {response.status} - {error_text}"
                    )

    async def test_connection(self) -> bool:
        """Test connection to GitHub Models API."""
        try:
            test_request = LLMRequest(
                prompt="Say 'Hello' if you can respond.",
                system_prompt="You are a helpful assistant.",
                max_tokens=10,
                temperature=0.1
            )
            response = await self.generate_response(test_request)
            return bool(response.content) and not response.error
        except Exception:
            return False

    def get_available_models(self) -> List[str]:
        """Get list of available models."""
        return [
            "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", 
            "o1-preview", "o1-mini",
            "claude-3-5-sonnet", "claude-3-haiku"
        ]

    def validate_config(self) -> bool:
        """Validate provider configuration."""
        return bool(self.token and self.model and self.endpoint)
