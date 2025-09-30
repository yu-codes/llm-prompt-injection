"""
Configuration Factory - 配置工廠
提供配置對象的創建和管理
"""

from typing import Optional
from .loader import ConfigurationLoader
from .validator import ConfigurationValidator


class ConfigurationFactory:
    """配置工廠 - 統一創建配置相關對象"""
    
    _loader_instance: Optional[ConfigurationLoader] = None
    _validator_instance: Optional[ConfigurationValidator] = None
    
    @classmethod
    def create_loader(cls, 
                      attacks_dir: str = "configs/attacks",
                      providers_config: str = "configs/providers.yaml",
                      base_dir: Optional[str] = None) -> ConfigurationLoader:
        """創建配置載入器"""
        if cls._loader_instance is None:
            cls._loader_instance = ConfigurationLoader(
                attacks_dir=attacks_dir,
                providers_config=providers_config,
                base_dir=base_dir
            )
        return cls._loader_instance
    
    @classmethod
    def create_validator(cls) -> ConfigurationValidator:
        """創建配置驗證器"""
        if cls._validator_instance is None:
            cls._validator_instance = ConfigurationValidator()
        return cls._validator_instance
    
    @classmethod 
    def reset(cls):
        """重置工廠實例（用於測試）"""
        cls._loader_instance = None
        cls._validator_instance = None