"""
Configuration Package - 配置系統包
提供統一的配置管理接口
"""

from .models import (
    AttackConfig, AttackSeverity, AttackCategory,
    PayloadConfig, EvaluationConfig, AttackSettings,  
    ProviderConfig, SystemConfig, ApplicationConfig,
    ConfigurationError, ProviderConfigurationError
)

from .loader import ConfigurationLoader
from .validator import ConfigurationValidator  
from .factory import ConfigurationFactory

# 便捷函數
def load_application_config() -> ApplicationConfig:
    """載入應用程式配置"""
    return ConfigurationFactory.create_loader().load_application_config()

def get_config_loader() -> ConfigurationLoader:
    """獲取配置載入器"""
    return ConfigurationFactory.create_loader()

__all__ = [
    # Models
    "AttackConfig", "AttackSeverity", "AttackCategory",
    "PayloadConfig", "EvaluationConfig", "AttackSettings",
    "ProviderConfig", "SystemConfig", "ApplicationConfig",
    
    # Services
    "ConfigurationLoader", "ConfigurationValidator", "ConfigurationFactory",
    
    # Functions  
    "load_application_config", "get_config_loader",
    
    # Exceptions
    "ConfigurationError", "ProviderConfigurationError"
]