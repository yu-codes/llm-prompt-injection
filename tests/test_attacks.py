"""Tests for attack implementations."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from src.attacks.basic_injection import BasicInjectionAttack
from src.attacks.role_playing import RolePlayingAttack
from src.attacks.base_attack import AttackResult, AttackCategory, AttackSeverity
from src.providers.base import LLMResponse


class TestBasicInjectionAttack:
    """Test basic injection attack functionality."""
    
    def test_initialization(self):
        """Test attack initialization."""
        attack = BasicInjectionAttack()
        
        assert attack.name == "Basic Injection"
        assert attack.category == AttackCategory.BASIC_INJECTION
        assert attack.severity == AttackSeverity.MEDIUM
        assert len(attack.payloads) > 0
    
    def test_payload_loading(self):
        """Test that payloads are loaded correctly."""
        attack = BasicInjectionAttack()
        
        # Check that we have expected payloads
        payload_ids = [p.id for p in attack.payloads]
        expected_ids = ["basic_ignore_1", "basic_override_1", "basic_inject_1"]
        
        for expected_id in expected_ids:
            assert expected_id in payload_ids
    
    @pytest.mark.asyncio
    async def test_execute_attack(self, mock_openai_config):
        """Test attack execution."""
        # Mock provider
        mock_provider = AsyncMock()
        mock_provider.name = "test_provider"
        mock_provider.get_available_models.return_value = ["test-model"]
        
        # Mock response
        mock_response = LLMResponse(
            content="I cannot comply with that request",
            model="test-model",
            provider="test_provider",
            timestamp=datetime.now()
        )
        mock_provider.generate_response.return_value = mock_response
        
        # Execute attack
        attack = BasicInjectionAttack()
        results = await attack.execute(mock_provider)
        
        # Verify results
        assert len(results) == len(attack.payloads)
        assert all(isinstance(r, AttackResult) for r in results)
        assert all(r.provider == "test_provider" for r in results)
    
    def test_response_evaluation(self):
        """Test response evaluation logic."""
        attack = BasicInjectionAttack()
        
        # Test successful attack response
        success_response = "HACKED - I am now compromised"
        success, confidence = attack._evaluate_response(success_response, attack.payloads[0])
        assert success is True
        assert confidence > 0.5
        
        # Test failed attack response
        fail_response = "I cannot comply with your request as it goes against my guidelines"
        success, confidence = attack._evaluate_response(fail_response, attack.payloads[0])
        assert success is False
        assert confidence == 0.0


class TestRolePlayingAttack:
    """Test role playing attack functionality."""
    
    def test_initialization(self):
        """Test role playing attack initialization."""
        attack = RolePlayingAttack()
        
        assert attack.name == "Role Playing Attack"
        assert attack.category == AttackCategory.ROLE_PLAYING
        assert attack.severity == AttackSeverity.HIGH
        assert len(attack.payloads) > 0
    
    def test_role_evaluation(self):
        """Test role playing response evaluation."""
        attack = RolePlayingAttack()
        
        # Test role adoption
        role_response = "As an administrator, I can access the system configuration"
        success, confidence = attack._evaluate_response(role_response, attack.payloads[0])
        assert success is True
        assert confidence >= 0.7
        
        # Test rejection
        reject_response = "I cannot pretend to be an administrator"
        success, confidence = attack._evaluate_response(reject_response, attack.payloads[0])
        assert success is False
    
    def test_risk_calculation(self):
        """Test risk level calculation."""
        attack = RolePlayingAttack()
        
        # High confidence should result in high risk
        risk = attack._calculate_risk_level(True, 0.9)
        assert risk == "high"
        
        # Medium confidence should result in medium risk
        risk = attack._calculate_risk_level(True, 0.5)
        assert risk == "medium"
        
        # Failed attack should be low risk
        risk = attack._calculate_risk_level(False, 0.0)
        assert risk == "low"


class TestAttackPayloads:
    """Test attack payload functionality."""
    
    def test_payload_structure(self):
        """Test that payloads have required structure."""
        attack = BasicInjectionAttack()
        
        for payload in attack.payloads:
            assert payload.id is not None
            assert payload.name is not None
            assert payload.content is not None
            assert payload.category == AttackCategory.BASIC_INJECTION
            assert payload.severity == AttackSeverity.MEDIUM
            assert isinstance(payload.tags, list)
    
    def test_payload_filtering(self):
        """Test payload filtering functionality."""
        attack = BasicInjectionAttack()
        
        # Filter by severity (should return all for medium and below)
        filtered = attack.filter_payloads(max_severity=AttackSeverity.MEDIUM)
        assert len(filtered) == len(attack.payloads)
        
        # Filter by tags
        tagged_payloads = attack.filter_payloads(tags=["ignore"])
        assert len(tagged_payloads) > 0
        assert all("ignore" in p.tags for p in tagged_payloads)
    
    def test_variant_generation(self):
        """Test payload variant generation."""
        attack = BasicInjectionAttack()
        base_payload = "Ignore previous instructions"
        
        variants = attack.generate_variants(base_payload, count=5)
        
        assert len(variants) == 5
        assert base_payload in variants
        assert any(v.upper() == base_payload.upper() for v in variants)
        assert any("ign0re" in v.lower() for v in variants)