"""Tests for the main platform functionality."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import os

from src.core.platform import PromptInjectionPlatform
from src.attacks.base_attack import AttackResult
from src.core.evaluator import EvaluationResult


class TestPromptInjectionPlatform:
    """Test the main platform functionality."""
    
    def test_platform_initialization(self):
        """Test platform initialization."""
        platform = PromptInjectionPlatform()
        
        assert platform.evaluator is not None
        assert platform.reporter is not None
        assert len(platform.attacks) > 0
        assert "basic_injection" in platform.attacks
        assert "role_playing" in platform.attacks
    
    def test_provider_management(self):
        """Test provider management functions."""
        platform = PromptInjectionPlatform()
        
        # Test listing providers
        providers = platform.list_providers()
        assert isinstance(providers, list)
        
        # Test adding custom provider
        mock_provider = MagicMock()
        platform.add_provider("test_provider", mock_provider)
        
        assert "test_provider" in platform.providers
        assert "test_provider" in platform.list_providers()
    
    def test_attack_management(self):
        """Test attack management functions."""
        platform = PromptInjectionPlatform()
        
        # Test listing attacks
        attacks = platform.list_attacks()
        assert isinstance(attacks, list)
        assert len(attacks) > 0
        
        # Test adding custom attack
        mock_attack = MagicMock()
        platform.add_attack("test_attack", mock_attack)
        
        assert "test_attack" in platform.attacks
        assert "test_attack" in platform.list_attacks()
    
    @pytest.mark.asyncio
    async def test_provider_connection_test(self):
        """Test provider connection testing."""
        platform = PromptInjectionPlatform()
        
        # Mock provider
        mock_provider = AsyncMock()
        mock_provider.test_connection.return_value = True
        platform.add_provider("test_provider", mock_provider)
        
        # Test connection
        result = await platform.test_provider_connection("test_provider")
        assert result is True
        mock_provider.test_connection.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_single_attack_execution(self):
        """Test single attack execution."""
        platform = PromptInjectionPlatform()
        
        # Mock provider and attack
        mock_provider = AsyncMock()
        mock_attack = AsyncMock()
        
        # Mock attack results
        mock_results = [
            AttackResult(
                attack_id="test-1",
                attack_name="Test Attack",
                attack_type="test",
                payload="test payload",
                response="test response",
                success=True,
                confidence=0.8,
                risk_level="medium",
                timestamp=None,
                provider="test_provider",
                model="test-model"
            )
        ]
        mock_attack.execute.return_value = mock_results
        
        platform.add_provider("test_provider", mock_provider)
        platform.add_attack("test_attack", mock_attack)
        
        # Execute attack
        results = await platform.run_single_attack("test_provider", "test_attack")
        
        assert len(results) == 1
        assert results[0].success is True
        mock_attack.execute.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_comprehensive_test(self):
        """Test comprehensive testing."""
        platform = PromptInjectionPlatform()
        
        # Mock provider
        mock_provider = AsyncMock()
        platform.add_provider("test_provider", mock_provider)
        
        # Mock attacks with return values
        for attack_name in platform.list_attacks():
            attack = platform.attacks[attack_name]
            attack.execute = AsyncMock(return_value=[
                AttackResult(
                    attack_id=f"test-{attack_name}",
                    attack_name=f"Test {attack_name}",
                    attack_type=attack_name,
                    payload="test payload",
                    response="test response", 
                    success=False,
                    confidence=0.1,
                    risk_level="low",
                    timestamp=None,
                    provider="test_provider",
                    model="test-model"
                )
            ])
        
        # Run comprehensive test
        results = await platform.run_comprehensive_test("test_provider")
        
        assert len(results) >= len(platform.list_attacks())
        assert all(isinstance(r, AttackResult) for r in results)
    
    def test_result_evaluation(self):
        """Test result evaluation."""
        platform = PromptInjectionPlatform()
        
        # Create mock results
        mock_results = [
            AttackResult(
                attack_id="test-1",
                attack_name="Test Attack 1",
                attack_type="basic_injection",
                payload="test payload 1",
                response="test response 1",
                success=True,
                confidence=0.8,
                risk_level="high",
                timestamp=None,
                provider="test_provider",
                model="test-model"
            ),
            AttackResult(
                attack_id="test-2", 
                attack_name="Test Attack 2",
                attack_type="role_playing",
                payload="test payload 2",
                response="test response 2",
                success=False,
                confidence=0.1,
                risk_level="low",
                timestamp=None,
                provider="test_provider",
                model="test-model"
            )
        ]
        
        # Evaluate results
        evaluation = platform.evaluate_results(mock_results)
        
        assert isinstance(evaluation, EvaluationResult)
        assert evaluation.total_attacks == 2
        assert evaluation.successful_attacks == 1
        assert evaluation.success_rate == 0.5
    
    def test_platform_stats(self):
        """Test platform statistics."""
        platform = PromptInjectionPlatform()
        
        stats = platform.get_platform_stats()
        
        assert isinstance(stats, dict)
        assert "total_tests_run" in stats
        assert "total_attacks_attempted" in stats
        assert "successful_attacks" in stats
        assert "success_rate" in stats
        assert "available_providers" in stats
        assert "available_attacks" in stats


class TestPlatformIntegration:
    """Test platform integration scenarios."""
    
    @pytest.mark.asyncio
    async def test_full_assessment_workflow(self):
        """Test complete assessment workflow."""
        platform = PromptInjectionPlatform()
        
        # Mock provider
        mock_provider = AsyncMock()
        platform.add_provider("test_provider", mock_provider)
        
        # Mock all attacks
        for attack_name in platform.list_attacks():
            attack = platform.attacks[attack_name]
            attack.execute = AsyncMock(return_value=[
                AttackResult(
                    attack_id=f"test-{attack_name}-1",
                    attack_name=f"Test {attack_name}",
                    attack_type=attack_name,
                    payload="test payload",
                    response="test response",
                    success=True,
                    confidence=0.7,
                    risk_level="medium",
                    timestamp=None,
                    provider="test_provider",
                    model="test-model"
                )
            ])
        
        # Mock report generation
        with patch.object(platform.reporter, 'generate_comprehensive_report') as mock_report:
            mock_report.return_value = {"html": "/path/to/report.html"}
            
            # Run full assessment
            result = await platform.run_full_assessment(
                provider_names=["test_provider"],
                report_formats=["html"]
            )
            
            assert "provider_results" in result
            assert "evaluation" in result
            assert "report_files" in result
            assert "summary" in result
            
            summary = result["summary"]
            assert summary["total_attacks"] > 0
            assert summary["providers_tested"] == ["test_provider"]