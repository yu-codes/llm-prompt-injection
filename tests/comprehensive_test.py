#!/usr/bin/env python3
"""
綜合測試腳本 - 測試 LLM Prompt Injection Testing Platform 的所有核心功能
Comprehensive Test Script for LLM Prompt Injection Testing Platform
"""

import asyncio
import sys
import time
from pathlib import Path
from typing import Dict, List, Any
import json
import tempfile
import shutil

# 添加 src 到 Python 路徑
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    from src.core.platform import PromptInjectionPlatform
    from src.providers.github_provider import GitHubProvider
    from src.providers.openai_provider import OpenAIProvider
    from src.core.basic_injection import BasicInjectionAttack
    from src.core.role_playing import RolePlayingAttack
    from src.core.reporter import ReportGenerator
    from src.core.evaluator import AttackEvaluator
except ImportError as e:
    print(f"❌ 導入錯誤: {e}")
    print("請確保在專案根目錄執行此腳本")
    sys.exit(1)


class ComprehensiveTestSuite:
    """綜合測試套件"""
    
    def __init__(self):
        self.test_results = {}
        self.platform = None
        self.test_count = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test(self, test_name: str, success: bool, message: str = ""):
        """記錄測試結果"""
        self.test_count += 1
        if success:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
            
        print(f"{status} - {test_name}")
        if message:
            print(f"      {message}")
            
        self.test_results[test_name] = {
            "success": success,
            "message": message,
            "timestamp": time.time()
        }
    
    async def test_platform_initialization(self):
        """測試平台初始化"""
        try:
            self.platform = PromptInjectionPlatform()
            self.log_test("平台初始化", True, "Platform successfully initialized")
        except Exception as e:
            self.log_test("平台初始化", False, f"Error: {e}")
            return False
        return True
    
    async def test_provider_creation(self):
        """測試提供商創建"""
        try:
            # 測試 GitHub Provider
            github_provider = GitHubProvider("test-token")
            self.log_test("GitHub Provider 創建", True, f"Models: {github_provider.supported_models}")
            
            # 測試 OpenAI Provider (如果有 API key)
            import os
            if os.getenv("OPENAI_API_KEY"):
                openai_provider = OpenAIProvider()
                self.log_test("OpenAI Provider 創建", True, "OpenAI provider created successfully")
            else:
                self.log_test("OpenAI Provider 創建", True, "Skipped - no API key provided")
                
        except Exception as e:
            self.log_test("Provider 創建", False, f"Error: {e}")
            return False
        return True
    
    async def test_attack_modules(self):
        """測試攻擊模組"""
        try:
            # 測試基本注入攻擊
            basic_attack = BasicInjectionAttack()
            payloads = basic_attack.get_payloads()
            self.log_test("基本注入攻擊模組", len(payloads) > 0, f"Generated {len(payloads)} payloads")
            
            # 測試角色扮演攻擊
            role_attack = RolePlayingAttack()
            role_payloads = role_attack.get_payloads()
            self.log_test("角色扮演攻擊模組", len(role_payloads) > 0, f"Generated {len(role_payloads)} role payloads")
            
        except Exception as e:
            self.log_test("攻擊模組測試", False, f"Error: {e}")
            return False
        return True
    
    async def test_report_generation(self):
        """測試報告生成"""
        try:
            # 創建臨時輸出目錄
            with tempfile.TemporaryDirectory() as temp_dir:
                reporter = ReportGenerator(temp_dir)
                
                # 創建模擬測試結果
                mock_results = []
                mock_evaluation = type('MockEval', (), {
                    'total_attacks': 5,
                    'successful_attacks': 2,
                    'success_rate': 0.4,
                    'average_confidence': 0.75,
                    'risk_distribution': {'high': 1, 'medium': 1, 'low': 3},
                    'attack_type_breakdown': {
                        'basic_injection': {'successful': 1, 'total': 3, 'success_rate': 0.33},
                        'role_playing': {'successful': 1, 'total': 2, 'success_rate': 0.5}
                    },
                    'provider_analysis': {},
                    'timestamp': '2024-01-01T00:00:00',
                    'metadata': {}
                })()
                
                # 生成報告
                report_files = reporter.generate_comprehensive_report(
                    mock_results, 
                    mock_evaluation, 
                    formats=["markdown", "json"]
                )
                
                # 檢查報告檔案是否生成
                markdown_exists = Path(report_files.get("markdown", "")).exists()
                json_exists = Path(report_files.get("json", "")).exists()
                
                self.log_test("Markdown 報告生成", markdown_exists, "Markdown report generated")
                self.log_test("JSON 報告生成", json_exists, "JSON report generated")
                
        except Exception as e:
            self.log_test("報告生成測試", False, f"Error: {e}")
            return False
        return True
    
    async def test_evaluator(self):
        """測試評估器"""
        try:
            evaluator = AttackEvaluator()
            
            # 模擬攻擊結果
            mock_response = "I cannot help with that request as it violates my guidelines."
            result = evaluator.evaluate_response(mock_response, {"expected": "should_reject"})
            
            self.log_test("評估器功能", result is not None, f"Evaluation result: {result}")
            
        except Exception as e:
            self.log_test("評估器測試", False, f"Error: {e}")
            return False
        return True
    
    async def test_configuration_loading(self):
        """測試配置文件加載"""
        try:
            # 檢查配置文件是否存在
            config_files = [
                "configs/defaults.yaml",
                "configs/providers.yaml", 
                "configs/custom_attacks.yaml"
            ]
            
            for config_file in config_files:
                if Path(config_file).exists():
                    self.log_test(f"{config_file} 存在性檢查", True, f"Config file found: {config_file}")
                else:
                    self.log_test(f"{config_file} 存在性檢查", False, f"Config file missing: {config_file}")
                    
            # 測試 YAML 加載
            import yaml
            for config_file in config_files:
                if Path(config_file).exists():
                    try:
                        with open(config_file, 'r', encoding='utf-8') as f:
                            yaml.safe_load(f)
                        self.log_test(f"{config_file} YAML 語法", True, "Valid YAML syntax")
                    except yaml.YAMLError as e:
                        self.log_test(f"{config_file} YAML 語法", False, f"Invalid YAML: {e}")
                        
        except Exception as e:
            self.log_test("配置文件測試", False, f"Error: {e}")
            return False
        return True
    
    async def test_template_system(self):
        """測試模板系統"""
        try:
            template_file = Path("src/templates/prompt_injection_template.md")
            
            if template_file.exists():
                # 讀取模板內容
                template_content = template_file.read_text(encoding='utf-8')
                
                # 檢查模板是否包含必要的佔位符
                required_placeholders = [
                    "{{generated_at}}",
                    "{{total_attacks}}",
                    "{{success_rate}}",
                    "{{risk_level}}"
                ]
                
                missing_placeholders = []
                for placeholder in required_placeholders:
                    if placeholder not in template_content:
                        missing_placeholders.append(placeholder)
                
                if not missing_placeholders:
                    self.log_test("模板系統", True, f"Template contains all required placeholders")
                else:
                    self.log_test("模板系統", False, f"Missing placeholders: {missing_placeholders}")
            else:
                self.log_test("模板系統", False, "Template file not found")
                
        except Exception as e:
            self.log_test("模板系統測試", False, f"Error: {e}")
            return False
        return True
    
    async def test_environment_variables(self):
        """測試環境變數"""
        import os
        
        # 檢查 .env.example 是否存在
        env_example = Path(".env.example")
        if env_example.exists():
            self.log_test(".env.example 存在", True, "Environment example file found")
        else:
            self.log_test(".env.example 存在", False, "Environment example file missing")
        
        # 檢查關鍵環境變數
        key_vars = ["GITHUB_TOKEN", "OPENAI_API_KEY"]
        for var in key_vars:
            value = os.getenv(var)
            if value:
                self.log_test(f"環境變數 {var}", True, f"Set (length: {len(value)})")
            else:
                self.log_test(f"環境變數 {var}", True, f"Not set (optional)")
    
    async def test_script_executability(self):
        """測試腳本可執行性"""
        scripts = [
            "scripts/run_platform.sh",
            "scripts/test_functionality.sh",
            "scripts/validate_configs.sh"
        ]
        
        for script in scripts:
            script_path = Path(script)
            if script_path.exists():
                # 檢查是否可執行
                import stat
                if script_path.stat().st_mode & stat.S_IEXEC:
                    self.log_test(f"{script} 可執行性", True, "Script is executable")
                else:
                    self.log_test(f"{script} 可執行性", False, "Script is not executable")
            else:
                self.log_test(f"{script} 存在性", False, "Script file missing")
    
    async def test_docker_configuration(self):
        """測試 Docker 配置"""
        docker_files = ["Dockerfile", "docker-compose.yml"]
        
        for docker_file in docker_files:
            if Path(docker_file).exists():
                self.log_test(f"{docker_file} 存在", True, f"Docker config found: {docker_file}")
            else:
                self.log_test(f"{docker_file} 存在", False, f"Docker config missing: {docker_file}")
    
    async def test_output_directory_creation(self):
        """測試輸出目錄創建"""
        try:
            # 測試創建輸出目錄
            test_output_dir = Path("test_output_temp")
            test_output_dir.mkdir(exist_ok=True)
            
            # 創建子目錄
            (test_output_dir / "reports").mkdir(exist_ok=True)
            (test_output_dir / "data").mkdir(exist_ok=True)
            
            self.log_test("輸出目錄創建", True, "Output directories created successfully")
            
            # 清理測試目錄
            shutil.rmtree(test_output_dir)
            
        except Exception as e:
            self.log_test("輸出目錄創建", False, f"Error: {e}")
            return False
        return True
    
    async def run_all_tests(self):
        """執行所有測試"""
        print("🧪 開始執行綜合功能測試")
        print("=" * 60)
        
        # 執行各項測試
        test_functions = [
            self.test_platform_initialization,
            self.test_provider_creation,
            self.test_attack_modules,
            self.test_report_generation,
            self.test_evaluator,
            self.test_configuration_loading,
            self.test_template_system,
            self.test_environment_variables,
            self.test_script_executability,
            self.test_docker_configuration,
            self.test_output_directory_creation
        ]
        
        for test_func in test_functions:
            try:
                await test_func()
            except Exception as e:
                self.log_test(test_func.__name__, False, f"Unexpected error: {e}")
        
        # 輸出測試結果摘要
        print("\n" + "=" * 60)
        print("📊 測試結果摘要")
        print(f"總測試數: {self.test_count}")
        print(f"通過: {self.passed_tests}")
        print(f"失敗: {self.failed_tests}")
        print(f"成功率: {(self.passed_tests/self.test_count*100):.1f}%")
        
        if self.failed_tests == 0:
            print("\n🎉 所有測試通過！平台準備就緒。")
            return True
        else:
            print(f"\n⚠️  {self.failed_tests} 個測試失敗，請檢查上述錯誤訊息。")
            return False


async def main():
    """主函數"""
    test_suite = ComprehensiveTestSuite()
    success = await test_suite.run_all_tests()
    
    # 保存測試結果
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump(test_suite.test_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📝 詳細測試結果已保存至 test_results.json")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)