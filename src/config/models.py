"""Configuration models using Pydantic."""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from pathlib import Path
import yaml


class ProviderConfig(BaseModel):
    """Base provider configuration."""
    
    enabled: bool = Field(default=True)
    timeout: int = Field(default=30)
    max_retries: int = Field(default=3)
    rate_limit: int = Field(default=10)


class AttackConfig(BaseModel):
    """Attack configuration model."""
    
    name: str
    type: str
    description: str
    payload: str
    expected_behavior: str = Field(default="should_reject")
    severity: str = Field(default="medium")
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EvaluationCriteria(BaseModel):
    """Evaluation criteria configuration."""
    
    attack_type: str
    success_indicators: List[str] = Field(default_factory=list)
    failure_indicators: List[str] = Field(default_factory=list)
    threshold: float = Field(default=0.5)
    weight: float = Field(default=1.0)


class ConfigManager:
    """Configuration file manager."""
    
    def __init__(self, config_dir: str = "./configs"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
    def load_yaml(self, filename: str) -> Dict[str, Any]:
        """Load YAML configuration file."""
        file_path = self.config_dir / filename
        if not file_path.exists():
            return {}
            
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    def save_yaml(self, filename: str, data: Dict[str, Any]) -> None:
        """Save data to YAML configuration file."""
        file_path = self.config_dir / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
    
    def load_attack_patterns(self) -> List[AttackConfig]:
        """Load attack patterns from configuration."""
        data = self.load_yaml("attack_patterns.yaml")
        attacks = []
        
        for attack_data in data.get("attacks", []):
            attacks.append(AttackConfig(**attack_data))
            
        return attacks
    
    def load_evaluation_criteria(self) -> List[EvaluationCriteria]:
        """Load evaluation criteria from configuration."""
        data = self.load_yaml("evaluation_criteria.yaml")
        criteria = []
        
        for criteria_data in data.get("criteria", []):
            criteria.append(EvaluationCriteria(**criteria_data))
            
        return criteria
    
    def load_providers_config(self) -> Dict[str, ProviderConfig]:
        """Load providers configuration."""
        data = self.load_yaml("providers.yaml")
        providers = {}
        
        for name, config in data.get("providers", {}).items():
            providers[name] = ProviderConfig(**config)
            
        return providers