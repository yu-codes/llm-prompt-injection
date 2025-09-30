"""
Configuration System - Legacy Interface
配置系統 - 向後兼容介面

This module provides backward compatibility with the old configuration system.
All functionality has been moved to the dedicated config package.
"""

# Import from the new config package
from ..config import (
    AttackConfig, AttackSeverity, AttackCategory,
    PayloadConfig, EvaluationConfig, AttackSettings,
    ProviderConfig, SystemConfig, ApplicationConfig,
    ConfigurationError, ProviderConfigurationError,
    ConfigurationLoader, ConfigurationValidator,
    load_application_config, get_config_loader
)

# Legacy compatibility layer
class ConfigurationManager(ConfigurationLoader):
    """Legacy compatibility wrapper"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._app_config = None
    
    @property 
    def attack_configs(self):
        """Legacy property for attack configs"""
        if self._app_config is None:
            self._app_config = self.load_application_config()
        return self._app_config.attacks
    
    @property
    def settings(self):
        """Legacy property for system settings"""
        if self._app_config is None:
            self._app_config = self.load_application_config()
        return self._app_config.system
    
    def get_attack_by_id(self, attack_id: str):
        """Legacy method"""
        return self.attack_configs.get(attack_id)
    
    def get_enabled_attacks(self):
        """Legacy method"""
        return {id: config for id, config in self.attack_configs.items() if config.enabled}
    
    def get_attacks_by_category(self, category: str):
        """Legacy method"""
        return {
            id: config for id, config in self.get_enabled_attacks().items()
            if config.category.value == category
        }
    
    def get_all_attacks(self):
        """Legacy method"""
        return self.attack_configs
    
    def get_attack_info(self):
        """Legacy method"""
        return [
            {
                'id': attack_id,
                'name': config.name,
                'category': config.category.value,
                'severity': config.severity.value,
                'enabled': config.enabled,
                'payload_count': len(config.payloads),
                'description': config.description
            }
            for attack_id, config in self.attack_configs.items()
        ]


# Global instances for backward compatibility
_config_manager = None

def get_config_manager() -> ConfigurationManager:
    """獲取全局配置管理器實例"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigurationManager()
    return _config_manager

def get_attack_loader() -> ConfigurationManager:
    """向後兼容性接口"""
    return get_config_manager()

# Alias for new functions
get_application_config = load_application_config


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Models
    "AttackConfig", "AttackSeverity", "AttackCategory",
    "PayloadConfig", "EvaluationConfig", "AttackSettings", 
    "ProviderConfig", "SystemConfig", "ApplicationConfig",
    
    # Loaders
    "ConfigurationLoader", "ConfigurationValidator",
    "ConfigurationManager",  # Legacy
    
    # Functions
    "get_config_loader", "load_application_config", "get_application_config",
    "get_config_manager", "get_attack_loader",  # Legacy
    
    # Exceptions
    "ConfigurationError", "ProviderConfigurationError"
]