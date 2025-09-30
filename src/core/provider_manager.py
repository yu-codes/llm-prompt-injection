"""
Simple Provider Manager
簡單提供商管理器

Manages LLM providers for the platform.
"""

from typing import Dict, Optional
from src.providers.base import BaseProvider
from src.providers.openai_provider import OpenAIProvider
from src.providers.github_provider import GitHubProvider


class ProviderManager:
    """提供商管理器"""
    
    def __init__(self):
        self.providers: Dict[str, BaseProvider] = {}
        self._initialize_providers()
    
    def _initialize_providers(self) -> None:
        """初始化可用的提供商"""
        # OpenAI Provider
        import os
        openai_config = {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        }
        
        if openai_config["api_key"]:
            try:
                openai_provider = OpenAIProvider(openai_config)
                self.providers["openai"] = openai_provider
                print("✓ OpenAI provider initialized")
            except Exception as e:
                print(f"⚠ OpenAI provider initialization failed: {e}")
        else:
            print("⚠ OpenAI API key not found in environment variables")
        
        # GitHub Models Provider
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            try:
                github_provider = GitHubProvider(
                    token=github_token,
                    model=os.getenv("GITHUB_MODEL", "gpt-4o-mini")
                )
                self.providers["github"] = github_provider
                print("✓ GitHub Models provider initialized")
            except Exception as e:
                print(f"⚠ GitHub provider initialization failed: {e}")
        else:
            print("⚠ GITHUB_TOKEN not found in environment variables")
    
    def get_provider(self, name: str) -> Optional[BaseProvider]:
        """獲取指定的提供商"""
        return self.providers.get(name)
    
    def list_providers(self) -> list[str]:
        """列出所有可用的提供商"""
        return list(self.providers.keys())
    
    def add_provider(self, name: str, provider: BaseProvider) -> None:
        """添加新的提供商"""
        self.providers[name] = provider
        print(f"✓ Added provider: {name}")