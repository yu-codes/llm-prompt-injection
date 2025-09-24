"""Main platform controller that orchestrates all components."""

import os
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path

from ..providers.base import BaseProvider
from ..providers.openai_provider import OpenAIProvider
from ..attacks.base_attack import BaseAttack, AttackResult
from ..attacks.basic_injection import BasicInjectionAttack
from ..attacks.role_playing import RolePlayingAttack
from .evaluator import AttackEvaluator, EvaluationResult
from .reporter import ReportGenerator


class PromptInjectionPlatform:
    """Main platform for orchestrating prompt injection tests."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.providers = {}
        self.attacks = {}
        self.evaluator = AttackEvaluator()
        self.reporter = ReportGenerator(
            output_dir=self.config.get("output_directory", "./output")
        )
        
        # Initialize components
        self._initialize_attacks()
        self._initialize_providers()
        
        # Stats tracking
        self.stats = {
            "total_tests_run": 0,
            "total_attacks_attempted": 0,
            "successful_attacks": 0,
            "start_time": datetime.now()
        }
    
    def _initialize_providers(self) -> None:
        """Initialize available LLM providers."""
        # OpenAI Provider
        openai_config = {
            "api_key": os.getenv("OPENAI_API_KEY"),
            "base_url": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
            "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        }
        
        if openai_config["api_key"]:
            try:
                self.providers["openai"] = OpenAIProvider(openai_config)
                print("✓ OpenAI provider initialized")
            except Exception as e:
                print(f"✗ Failed to initialize OpenAI provider: {e}")
        else:
            print("⚠ OpenAI API key not found in environment variables")
    
    def _initialize_attacks(self) -> None:
        """Initialize available attack types."""
        self.attacks["basic_injection"] = BasicInjectionAttack()
        self.attacks["role_playing"] = RolePlayingAttack()
        print(f"✓ Initialized {len(self.attacks)} attack types")
    
    def add_provider(self, name: str, provider: BaseProvider) -> None:
        """Add a custom LLM provider."""
        self.providers[name] = provider
        print(f"✓ Added provider: {name}")
    
    def add_attack(self, name: str, attack: BaseAttack) -> None:
        """Add a custom attack type."""
        self.attacks[name] = attack
        print(f"✓ Added attack type: {name}")
    
    def list_providers(self) -> List[str]:
        """List available providers."""
        return list(self.providers.keys())
    
    def list_attacks(self) -> List[str]:
        """List available attack types.""" 
        return list(self.attacks.keys())
    
    async def test_provider_connection(self, provider_name: str) -> bool:
        """Test connection to a specific provider."""
        if provider_name not in self.providers:
            print(f"✗ Provider '{provider_name}' not found")
            return False
        
        provider = self.providers[provider_name]
        try:
            is_connected = await provider.test_connection()
            if is_connected:
                print(f"✓ Connection to {provider_name} successful")
            else:
                print(f"✗ Connection to {provider_name} failed")
            return is_connected
        except Exception as e:
            print(f"✗ Error testing {provider_name}: {e}")
            return False
    
    async def run_single_attack(
        self,
        provider_name: str,
        attack_type: str,
        target_prompt: Optional[str] = None
    ) -> List[AttackResult]:
        """Run a single attack type against a provider."""
        
        if provider_name not in self.providers:
            raise ValueError(f"Provider '{provider_name}' not available")
        
        if attack_type not in self.attacks:
            raise ValueError(f"Attack type '{attack_type}' not available")
        
        provider = self.providers[provider_name]
        attack = self.attacks[attack_type]
        
        print(f"🎯 Running {attack_type} attack against {provider_name}...")
        
        try:
            results = await attack.execute(provider, target_prompt)
            successful = sum(1 for r in results if r.success)
            
            print(f"✓ Completed {attack_type}: {successful}/{len(results)} successful")
            
            # Update stats
            self.stats["total_attacks_attempted"] += len(results)
            self.stats["successful_attacks"] += successful
            
            return results
            
        except Exception as e:
            print(f"✗ Error during {attack_type} attack: {e}")
            return []
    
    async def run_comprehensive_test(
        self,
        provider_name: str,
        attack_types: Optional[List[str]] = None,
        target_prompt: Optional[str] = None
    ) -> List[AttackResult]:
        """Run comprehensive tests against a provider."""
        
        if provider_name not in self.providers:
            raise ValueError(f"Provider '{provider_name}' not available")
        
        if attack_types is None:
            attack_types = list(self.attacks.keys())
        
        print(f"🚀 Starting comprehensive test against {provider_name}")
        print(f"   Attack types: {', '.join(attack_types)}")
        
        all_results = []
        
        for attack_type in attack_types:
            if attack_type in self.attacks:
                results = await self.run_single_attack(provider_name, attack_type, target_prompt)
                all_results.extend(results)
            else:
                print(f"⚠ Skipping unknown attack type: {attack_type}")
        
        self.stats["total_tests_run"] += 1
        
        print(f"✅ Comprehensive test completed: {len(all_results)} total attacks")
        return all_results
    
    async def run_multi_provider_test(
        self,
        provider_names: Optional[List[str]] = None,
        attack_types: Optional[List[str]] = None,
        target_prompt: Optional[str] = None
    ) -> Dict[str, List[AttackResult]]:
        """Run tests against multiple providers."""
        
        if provider_names is None:
            provider_names = list(self.providers.keys())
        
        if not provider_names:
            raise ValueError("No providers available for testing")
        
        print(f"🌐 Starting multi-provider test")
        print(f"   Providers: {', '.join(provider_names)}")
        
        all_provider_results = {}
        
        for provider_name in provider_names:
            if provider_name in self.providers:
                print(f"\n--- Testing {provider_name} ---")
                results = await self.run_comprehensive_test(provider_name, attack_types, target_prompt)
                all_provider_results[provider_name] = results
            else:
                print(f"⚠ Skipping unavailable provider: {provider_name}")
        
        print(f"\n✅ Multi-provider test completed for {len(all_provider_results)} providers")
        return all_provider_results
    
    def evaluate_results(self, results: List[AttackResult]) -> EvaluationResult:
        """Evaluate attack results."""
        print("📊 Evaluating results...")
        evaluation = self.evaluator.evaluate_results(results)
        
        print(f"   Success rate: {evaluation.success_rate:.1%}")
        print(f"   Risk distribution: {evaluation.risk_distribution}")
        
        return evaluation
    
    def generate_report(
        self,
        results: List[AttackResult],
        evaluation: EvaluationResult,
        formats: List[str] = ["html", "json"],
        report_name: Optional[str] = None
    ) -> Dict[str, str]:
        """Generate comprehensive report."""
        print("📝 Generating report...")
        
        generated_files = self.reporter.generate_comprehensive_report(
            results, evaluation, formats, report_name
        )
        
        print("✓ Report generated:")
        for format_type, file_path in generated_files.items():
            print(f"   {format_type.upper()}: {file_path}")
        
        return generated_files
    
    async def run_full_assessment(
        self,
        provider_names: Optional[List[str]] = None,
        attack_types: Optional[List[str]] = None,
        target_prompt: Optional[str] = None,
        report_formats: List[str] = ["html", "json"]
    ) -> Dict[str, Any]:
        """Run full security assessment and generate reports."""
        
        print("🔒 Starting full security assessment...")
        
        # Run tests
        provider_results = await self.run_multi_provider_test(
            provider_names, attack_types, target_prompt
        )
        
        # Combine all results
        all_results = []
        for results in provider_results.values():
            all_results.extend(results)
        
        # Evaluate
        evaluation = self.evaluate_results(all_results)
        
        # Generate report
        report_files = self.generate_report(
            all_results, evaluation, report_formats
        )
        
        # Summary
        print("\n" + "="*60)
        print("🎯 SECURITY ASSESSMENT SUMMARY")
        print("="*60)
        print(f"Total attacks: {len(all_results)}")
        print(f"Successful attacks: {evaluation.successful_attacks}")
        print(f"Success rate: {evaluation.success_rate:.1%}")
        print(f"Average confidence: {evaluation.average_confidence:.2f}")
        print(f"Risk distribution: {evaluation.risk_distribution}")
        print("="*60)
        
        return {
            "provider_results": provider_results,
            "evaluation": evaluation,
            "report_files": report_files,
            "summary": {
                "total_attacks": len(all_results),
                "successful_attacks": evaluation.successful_attacks,
                "success_rate": evaluation.success_rate,
                "providers_tested": list(provider_results.keys()),
                "attack_types_used": list(set(r.attack_type for r in all_results))
            }
        }
    
    def get_platform_stats(self) -> Dict[str, Any]:
        """Get platform usage statistics."""
        uptime = datetime.now() - self.stats["start_time"]
        
        return {
            "uptime_seconds": uptime.total_seconds(),
            "total_tests_run": self.stats["total_tests_run"],
            "total_attacks_attempted": self.stats["total_attacks_attempted"],
            "successful_attacks": self.stats["successful_attacks"],
            "available_providers": len(self.providers),
            "available_attacks": len(self.attacks),
            "success_rate": (
                self.stats["successful_attacks"] / self.stats["total_attacks_attempted"]
                if self.stats["total_attacks_attempted"] > 0 else 0.0
            )
        }