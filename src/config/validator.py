"""
Configuration Validator - 配置驗證器
專注於配置驗證邏輯
"""

import logging
from pathlib import Path
from typing import Dict, List, Any

from .models import AttackConfig, AttackCategory, AttackSeverity

logger = logging.getLogger(__name__)


class ConfigurationValidator:
    """配置驗證器 - 專門負責驗證配置的正確性"""
    
    def validate_attack_config(self, attack_config: AttackConfig) -> List[str]:
        """驗證攻擊配置對象"""
        issues = []
        
        if not attack_config.name.strip():
            issues.append("攻擊名稱不能為空")
        
        if not attack_config.payloads:
            issues.append("必須包含至少一個攻擊載荷")
        
        for i, payload in enumerate(attack_config.payloads):
            if not payload.content.strip():
                issues.append(f"載荷 {i+1} content 不能為空")
        
        return issues

    def validate_attack_yaml_data(self, file_path: Path, data: Dict[str, Any]) -> List[str]:
        """驗證攻擊 YAML 數據"""
        errors = []
        
        # 檢查必要字段
        required_fields = ['name', 'category', 'payloads']
        for field in required_fields:
            if field not in data:
                errors.append(f"Missing required field: {field}")
        
        # 驗證類別
        if 'category' in data:
            try:
                AttackCategory(data['category'])
            except ValueError:
                valid_categories = [c.value for c in AttackCategory]
                errors.append(f"Invalid category '{data['category']}'. Valid: {valid_categories}")
        
        # 驗證嚴重程度
        if 'severity' in data:
            try:
                AttackSeverity(data['severity'])
            except ValueError:
                valid_severities = [s.value for s in AttackSeverity]
                errors.append(f"Invalid severity '{data['severity']}'. Valid: {valid_severities}")
        
        # 驗證載荷
        if 'payloads' in data:
            payloads = data['payloads']
            if not isinstance(payloads, list):
                errors.append("'payloads' must be a list")
            else:
                for i, payload in enumerate(payloads):
                    if not isinstance(payload, dict):
                        errors.append(f"Payload {i+1} must be a dictionary")
                        continue
                    
                    if 'content' not in payload:
                        errors.append(f"Payload {i+1} missing 'content' field")
                    elif not payload['content'] or not str(payload['content']).strip():
                        errors.append(f"Payload {i+1} 'content' cannot be empty")
        
        return errors
    
    def validate_provider_config(self, name: str, config: Dict[str, Any]) -> List[str]:
        """驗證提供商配置"""
        errors = []
        
        # 檢查基本字段
        if 'enabled' in config and not isinstance(config.get('enabled'), bool):
            errors.append(f"Provider {name}: 'enabled' must be boolean")
        
        if 'timeout' in config:
            timeout = config['timeout']
            if not isinstance(timeout, (int, float)) or timeout < 1:
                errors.append(f"Provider {name}: 'timeout' must be positive number")
        
        if 'retry_attempts' in config:
            retries = config['retry_attempts']
            if not isinstance(retries, int) or retries < 0:
                errors.append(f"Provider {name}: 'retry_attempts' must be non-negative integer")
        
        if 'max_tokens' in config:
            max_tokens = config['max_tokens']
            if not isinstance(max_tokens, int) or max_tokens < 1:
                errors.append(f"Provider {name}: 'max_tokens' must be positive integer")
        
        # 檢查rate_limit結構（如果存在）
        if 'rate_limit' in config:
            rate_limit = config['rate_limit']
            if isinstance(rate_limit, dict):
                if 'requests_per_minute' in rate_limit:
                    rpm = rate_limit['requests_per_minute']
                    if not isinstance(rpm, int) or rpm < 1:
                        errors.append(f"Provider {name}: rate_limit.requests_per_minute must be positive integer")
        
        return errors