"""Base attack interface for prompt injection attacks."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class AttackSeverity(Enum):
    """Attack severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AttackCategory(Enum):
    """Attack category types."""
    BASIC_INJECTION = "basic_injection"
    ROLE_PLAYING = "role_playing"
    CONTEXT_SWITCHING = "context_switching"
    JAILBREAK = "jailbreak"
    DATA_EXTRACTION = "data_extraction"
    PROMPT_LEAKING = "prompt_leaking"


@dataclass
class AttackResult:
    """Result of an attack attempt."""
    
    attack_id: str
    attack_name: str
    attack_type: str
    payload: str
    response: str
    success: bool
    confidence: float
    risk_level: str
    timestamp: datetime
    provider: str
    model: str
    latency: Optional[float] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AttackPayload:
    """Attack payload definition."""
    
    id: str
    name: str
    content: str
    category: AttackCategory
    severity: AttackSeverity
    description: str
    tags: List[str] = None
    expected_behavior: str = "should_reject"
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.metadata is None:
            self.metadata = {}


class BaseAttack(ABC):
    """Abstract base class for attack implementations."""
    
    def __init__(self, name: str, category: AttackCategory, severity: AttackSeverity):
        self.name = name
        self.category = category
        self.severity = severity
        self.payloads = []
        self._load_payloads()
    
    @abstractmethod
    def _load_payloads(self) -> None:
        """Load attack payloads."""
        pass
    
    @abstractmethod
    async def execute(self, provider, target_prompt: str = None) -> List[AttackResult]:
        """Execute the attack."""
        pass
    
    def add_payload(self, payload: AttackPayload) -> None:
        """Add a payload to this attack."""
        self.payloads.append(payload)
    
    def get_payloads(self) -> List[AttackPayload]:
        """Get all payloads for this attack."""
        return self.payloads
    
    def filter_payloads(self, max_severity: AttackSeverity = None, tags: List[str] = None) -> List[AttackPayload]:
        """Filter payloads based on criteria."""
        filtered = self.payloads
        
        if max_severity:
            severity_order = {
                AttackSeverity.LOW: 1,
                AttackSeverity.MEDIUM: 2,
                AttackSeverity.HIGH: 3,
                AttackSeverity.CRITICAL: 4
            }
            max_level = severity_order[max_severity]
            filtered = [p for p in filtered if severity_order[p.severity] <= max_level]
        
        if tags:
            filtered = [p for p in filtered if any(tag in p.tags for tag in tags)]
        
        return filtered
    
    def generate_variants(self, base_payload: str, count: int = 5) -> List[str]:
        """Generate variants of a base payload."""
        # Simple variations - could be enhanced with more sophisticated techniques
        variants = [base_payload]
        
        # Case variations
        variants.append(base_payload.upper())
        variants.append(base_payload.lower())
        variants.append(base_payload.title())
        
        # Spacing variations
        variants.append(base_payload.replace(" ", "  "))
        variants.append(base_payload.replace(" ", "\n"))
        
        # Punctuation variations
        variants.append(base_payload + ".")
        variants.append(base_payload + "!")
        variants.append(base_payload + "?")
        
        # Encoding variations
        variants.append(base_payload.replace("ignore", "ign0re"))
        variants.append(base_payload.replace("system", "syst3m"))
        
        return variants[:count]
    
    def get_attack_info(self) -> Dict[str, Any]:
        """Get information about this attack."""
        return {
            "name": self.name,
            "category": self.category.value,
            "severity": self.severity.value,
            "payload_count": len(self.payloads),
            "description": self.__doc__ or "No description available"
        }