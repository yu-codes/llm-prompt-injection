"""
Configuration Loader - 配置載入器  
專注於從文件載入配置數據
"""

import os
import yaml
import logging
from pathlib import Path
from typing import Dict, Optional

from .models import (
    AttackConfig, PayloadConfig, EvaluationConfig, AttackSettings, 
    ProviderConfig, SystemConfig, ApplicationConfig,
    AttackCategory, AttackSeverity,
    ConfigurationError, ProviderConfigurationError
)
from .validator import ConfigurationValidator

logger = logging.getLogger(__name__)


class ConfigurationLoader:
    """配置載入器 - 專門負責從文件載入配置"""
    
    def __init__(self, 
                 attacks_dir: str = "configs/attacks",
                 providers_config: str = "configs/providers.yaml",
                 base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir) if base_dir else Path(".")
        self.attacks_dir = self.base_dir / attacks_dir
        self.providers_config_path = self.base_dir / providers_config
        self.validator = ConfigurationValidator()
    
    def load_attack_config(self, file_path: Path) -> Optional[AttackConfig]:
        """載入單個攻擊配置"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not data:
                logger.warning(f"Empty config file: {file_path}")
                return None
            
            # 驗證配置
            validation_errors = self.validator.validate_attack_yaml_data(file_path, data)
            if validation_errors:
                raise ConfigurationError(
                    f"Validation errors in {file_path}:\n" + "\n".join(f"  - {error}" for error in validation_errors)
                )
            
            # 創建配置對象
            return self._create_attack_config(data, file_path)
            
        except yaml.YAMLError as e:
            logger.error(f"YAML parsing error in {file_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to load attack config {file_path}: {e}")
            return None
    
    def _create_attack_config(self, data: Dict, file_path: Path) -> AttackConfig:
        """從數據創建攻擊配置對象"""
        # 創建載荷配置
        payloads = []
        for i, payload_data in enumerate(data.get('payloads', [])):
            payload = PayloadConfig(
                id=payload_data.get('id', f"payload_{i}"),
                name=payload_data.get('name', f"Payload {i+1}"),
                content=payload_data['content'],
                severity=AttackSeverity(payload_data.get('severity', 'medium')),
                tags=payload_data.get('tags', []),
                expected_behavior=payload_data.get('expected_behavior', 'should_reject'),
                metadata=payload_data.get('metadata', {})
            )
            payloads.append(payload)
        
        # 創建評估配置
        eval_data = data.get('evaluation', {})
        evaluation = EvaluationConfig(
            success_indicators=eval_data.get('success_indicators', []),
            role_adoption_indicators=eval_data.get('role_adoption_indicators', []),
            mode_activation_indicators=eval_data.get('mode_activation_indicators', []),
            replacement_indicators=eval_data.get('replacement_indicators', []),
            decoding_indicators=eval_data.get('decoding_indicators', []),
            confidence_levels=eval_data.get('confidence_levels', {})
        )
        
        # 創建設置配置
        settings_data = data.get('settings', {})
        settings = AttackSettings(
            max_attempts=settings_data.get('max_attempts', 3),
            timeout=settings_data.get('timeout', 30),
            retry_on_error=settings_data.get('retry_on_error', True),
            delay_between_attempts=settings_data.get('delay_between_attempts', 0.5)
        )
        
        return AttackConfig(
            id=file_path.stem,  # 使用文件名作為 ID
            name=data['name'],
            description=data.get('description', ''),
            category=AttackCategory(data['category']),
            severity=AttackSeverity(data.get('severity', 'medium')),
            enabled=data.get('enabled', True),
            payloads=payloads,
            evaluation=evaluation,
            settings=settings,
            file_path=str(file_path)
        )
    
    def load_all_attacks(self) -> Dict[str, AttackConfig]:
        """載入所有攻擊配置"""
        attacks = {}
        
        if not self.attacks_dir.exists():
            logger.warning(f"Attacks directory not found: {self.attacks_dir}")
            return attacks
        
        yaml_files = list(self.attacks_dir.glob("*.yaml")) + list(self.attacks_dir.glob("*.yml"))
        
        for yaml_file in yaml_files:
            attack_config = self.load_attack_config(yaml_file)
            if attack_config:
                attack_id = yaml_file.stem
                attacks[attack_id] = attack_config
                logger.info(f"Loaded attack config: {attack_config.name}")
        
        logger.info(f"Loaded {len(attacks)} attack configurations")
        return attacks
    
    def load_application_config(self) -> ApplicationConfig:
        """載入完整的應用程式配置"""
        # 載入攻擊配置
        attacks = self.load_all_attacks()
        
        # 載入提供商配置
        providers = self._load_providers_config()
        
        # 載入系統配置
        system = self._load_system_config()
        
        return ApplicationConfig(
            attacks=attacks,
            providers=providers, 
            system=system
        )
    
    def _load_system_config(self) -> SystemConfig:
        """載入系統配置"""
        return SystemConfig(
            output_dir=os.getenv("OUTPUT_DIR", "./output"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            max_concurrent=int(os.getenv("MAX_CONCURRENT_TESTS", "5")),
            request_delay=float(os.getenv("REQUEST_DELAY_SECONDS", "1.0"))
        )
    
    def _load_providers_config(self) -> Dict[str, ProviderConfig]:
        """載入提供商配置"""
        providers = {}
        
        # 首先載入環境變量中的提供商
        providers.update(self._load_env_providers())
        
        # 然後載入配置文件中的提供商
        if self.providers_config_path.exists():
            try:
                providers.update(self._load_file_providers())
            except Exception as e:
                logger.warning(f"Failed to load providers config: {e}")
        
        return providers
    
    def _load_env_providers(self) -> Dict[str, ProviderConfig]:
        """從環境變量載入提供商配置"""
        providers = {}
        
        # OpenAI
        if os.getenv("OPENAI_API_KEY"):
            providers["openai"] = ProviderConfig(
                name="openai",
                enabled=True,
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
                model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            )
        
        # GitHub Models
        if os.getenv("GITHUB_TOKEN"):
            providers["github"] = ProviderConfig(
                name="github", 
                enabled=True,
                api_key=os.getenv("GITHUB_TOKEN"),
                base_url="https://models.inference.ai.azure.com",
                model=os.getenv("GITHUB_MODEL", "gpt-4o-mini")
            )
        
        return providers
    
    def _load_file_providers(self) -> Dict[str, ProviderConfig]:
        """從配置文件載入提供商配置"""
        providers = {}
        
        try:
            with open(self.providers_config_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load providers config: {e}")
            return providers
        
        providers_data = data.get('providers', {})
        
        for name, config_data in providers_data.items():
            try:
                # 驗證提供商配置
                validation_errors = self.validator.validate_provider_config(name, config_data)
                if validation_errors:
                    logger.warning(f"Provider {name} validation errors: {validation_errors}")
                    continue
                
                provider_config = ProviderConfig(
                    name=name,
                    enabled=config_data.get('enabled', True),
                    api_key=self._resolve_env_var(config_data.get('api_key')),
                    base_url=config_data.get('base_url'),
                    model=config_data.get('model', config_data.get('default_model')),
                    timeout=config_data.get('timeout', 30),
                    max_retries=config_data.get('max_retries', config_data.get('retry_attempts', 3)),
                    rate_limit=config_data.get('rate_limit'),
                    additional_params={k: v for k, v in config_data.items() 
                                    if k not in ['name', 'enabled', 'api_key', 'base_url', 
                                               'model', 'timeout', 'max_retries', 'rate_limit']}
                )
                providers[name] = provider_config
                logger.info(f"Loaded provider config: {name}")
                
            except Exception as e:
                logger.error(f"Failed to load provider config {name}: {e}")
        
        return providers
    
    def _resolve_env_var(self, value: Optional[str]) -> Optional[str]:
        """解析環境變量"""
        if not value:
            return None
        
        if value.startswith("${") and value.endswith("}"):
            env_var = value[2:-1]
            return os.getenv(env_var)
        
        return value