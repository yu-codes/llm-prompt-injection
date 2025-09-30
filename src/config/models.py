"""
Configuration Models - Professional Data Models
配置模型 - 專業數據模型

Defines all configuration data structures using proper validation and type checking.
"""

from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
import os


class AttackSeverity(Enum):
    """攻擊嚴重程度枚舉"""
    LOW = "low"
    MEDIUM = "medium" 
    HIGH = "high"
    CRITICAL = "critical"


class AttackCategory(Enum):
    """攻擊類別枚舉"""
    BASIC_INJECTION = "basic_injection"
    ROLE_PLAYING = "role_playing"
    JAILBREAK = "jailbreak"
    SYSTEM_PROMPT_REPLACE = "system_prompt_replace"
    ENCODED_INJECTION = "encoded_injection" 
    TEST_ATTACK = "test_attack"


@dataclass(frozen=True)
class PayloadConfig:
    """攻擊載荷配置"""
    id: str
    name: str
    content: str
    severity: AttackSeverity = AttackSeverity.MEDIUM
    tags: List[str] = field(default_factory=list)
    expected_behavior: str = "should_reject"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.id or not self.id.strip():
            raise ValueError("Payload ID cannot be empty")
        if not self.content or not self.content.strip():
            raise ValueError("Payload content cannot be empty")


@dataclass(frozen=True)
class EvaluationConfig:
    """評估配置"""
    success_indicators: List[str] = field(default_factory=list)
    role_adoption_indicators: List[str] = field(default_factory=list)
    mode_activation_indicators: List[str] = field(default_factory=list) 
    replacement_indicators: List[str] = field(default_factory=list)
    decoding_indicators: List[str] = field(default_factory=list)
    confidence_levels: Dict[str, float] = field(default_factory=lambda: {
        "critical": 0.95,
        "high": 0.8, 
        "medium": 0.5,
        "low": 0.2
    })


@dataclass(frozen=True)
class AttackSettings:
    """攻擊設置"""
    max_attempts: int = 3
    timeout: int = 30
    retry_on_error: bool = True
    delay_between_attempts: float = 0.5
    
    def __post_init__(self):
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        if self.timeout < 1:
            raise ValueError("timeout must be >= 1")
        if self.delay_between_attempts < 0:
            raise ValueError("delay_between_attempts must be >= 0")


@dataclass(frozen=True)
class AttackConfig:
    """攻擊配置"""
    id: str
    name: str
    description: str
    category: AttackCategory
    severity: AttackSeverity
    enabled: bool
    payloads: List[PayloadConfig]
    evaluation: EvaluationConfig
    settings: AttackSettings
    file_path: str


@dataclass(frozen=True)
class ProviderConfig:
    """LLM提供商配置"""
    name: str
    enabled: bool
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    rate_limit: Optional[Union[int, Dict[str, Any]]] = None
    additional_params: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Provider name cannot be empty")
        if self.timeout < 1:
            raise ValueError("timeout must be >= 1")
        if self.max_retries < 0:
            raise ValueError("max_retries must be >= 0")
        # 允許rate_limit是整數或字典


@dataclass(frozen=True)
class SystemConfig:
    """系統配置"""
    output_dir: str = "./output"
    log_level: str = "INFO"
    max_concurrent: int = 5
    request_delay: float = 1.0
    max_concurrent_tests: int = 5
    request_delay_seconds: float = 1.0
    enable_detailed_logging: bool = True
    
    def __post_init__(self):
        if self.max_concurrent_tests < 1:
            raise ValueError("max_concurrent_tests must be >= 1")
        if self.request_delay_seconds < 0:
            raise ValueError("request_delay_seconds must be >= 0")
        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError("Invalid log_level")

    @classmethod
    def from_env(cls) -> 'SystemConfig':
        """從環境變數創建系統配置"""
        return cls(
            output_dir=os.getenv("OUTPUT_DIR", "./output"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            max_concurrent_tests=int(os.getenv("MAX_CONCURRENT_TESTS", "5")),
            request_delay_seconds=float(os.getenv("REQUEST_DELAY_SECONDS", "1.0")),
            enable_detailed_logging=os.getenv("ENABLE_DETAILED_LOGGING", "true").lower() == "true"
        )


@dataclass(frozen=True)
class ApplicationConfig:
    """應用程式總配置"""
    system: SystemConfig
    providers: Dict[str, ProviderConfig]
    attacks: Dict[str, AttackConfig]
    
    def __post_init__(self):
        if not self.providers:
            raise ValueError("At least one provider must be configured")

    def get_enabled_providers(self) -> Dict[str, ProviderConfig]:
        """獲取啟用的提供商"""
        return {name: config for name, config in self.providers.items() if config.enabled}

    def get_enabled_attacks(self) -> Dict[str, AttackConfig]:
        """獲取啟用的攻擊"""
        return {id: config for id, config in self.attacks.items() if config.enabled}

    def get_attacks_by_category(self, category: AttackCategory) -> Dict[str, AttackConfig]:
        """根據類別獲取攻擊"""
        return {
            id: config for id, config in self.get_enabled_attacks().items()
            if config.category == category
        }


# ============================================================================
# Configuration Validation Errors
# ============================================================================

class ConfigurationError(Exception):
    """配置錯誤基類"""
    pass


class AttackConfigurationError(ConfigurationError):
    """攻擊配置錯誤"""
    pass


class ProviderConfigurationError(ConfigurationError):
    """提供商配置錯誤"""
    pass


class SystemConfigurationError(ConfigurationError):
    """系統配置錯誤"""
    pass


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Enums
    "AttackSeverity",
    "AttackCategory",
    
    # Configuration Models
    "PayloadConfig",
    "EvaluationConfig", 
    "AttackSettings",
    "AttackConfig",
    "ProviderConfig",
    "SystemConfig",
    "ApplicationConfig",
    
    # Exceptions
    "ConfigurationError",
    "AttackConfigurationError",
    "ProviderConfigurationError",
    "SystemConfigurationError"
]