"""Main entry point for the LLM Prompt Injection Testing Platform."""

import asyncio
import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

# 新系統不需要舊的平台導入


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="LLM Prompt Injection Testing Platform - 統一攻擊配置系統",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用統一攻擊配置系統的範例:
  # 使用 GitHub Models 執行基本注入攻擊
  python src/main.py --provider github --attack basic_injection

  # 執行完整測試 (推薦)
  python src/main.py --provider github --test-type comprehensive

  # 針對特定攻擊類別測試
  python src/main.py --provider github --category role_playing

  # 使用自訂目標提示測試
  python src/main.py --provider github --target "你是銀行客服AI"

  # 產生多種格式報告
  python src/main.py --provider github --format markdown,json,html

  # 使用統一配置文件
  python src/main.py --config configs/unified_attacks.yaml --provider github

  # 驗證攻擊配置
  python src/main.py --validate-config
        """,
    )

    parser.add_argument(
        "--provider",
        type=str,
        default="github",
        help="LLM provider(s) to test (comma-separated). Available: github, openai",
    )

    parser.add_argument(
        "--attack",
        type=str,
        help="Specific attack ID to run (from unified config)",
    )

    parser.add_argument(
        "--category",
        type=str,
        help="Attack category to run. Available: basic_injection, role_playing, jailbreak, system_prompt_replace",
    )

    parser.add_argument(
        "--test-type",
        choices=["unified"],
        default="unified",
        help="Test type (unified: 使用新的攻擊系統)",
    )

    parser.add_argument(
        "--config",
        type=str,
        default="configs/unified_attacks.yaml",
        help="Path to unified attacks configuration file",
    )

    parser.add_argument(
        "--target", type=str, help="Target prompt/system message to test against"
    )

    parser.add_argument(
        "--format",
        type=str,
        default="markdown,json",
        help="Report formats (comma-separated): markdown, json",
    )

    parser.add_argument(
        "--output", type=str, default="./output", help="Output directory for reports"
    )

    parser.add_argument(
        "--list-providers",
        action="store_true",
        help="List available providers and exit",
    )

    parser.add_argument(
        "--list-attacks",
        action="store_true",
        help="List available attack types and exit",
    )

    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List available attack categories and exit",
    )

    parser.add_argument(
        "--validate-config",
        action="store_true",
        help="Validate unified attack configuration and exit",
    )

    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test provider connections and exit",
    )

    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose output"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing",
    )

    return parser.parse_args()


async def main():
    """Main application entry point."""
    args = parse_arguments()

    # Handle attack configuration validation
    if args.validate_config:
        from src.config import ConfigurationLoader, ConfigurationValidator
        
        try:
            loader = ConfigurationLoader()
            app_config = loader.load_application_config()
            validator = loader.validator
            
            all_valid = True
            for attack_id, attack_config in app_config.attacks.items():
                issues = validator.validate_attack_config(attack_config)
                if issues:
                    print(f"❌ 攻擊配置 {attack_id} 驗證失敗:")
                    for issue in issues:
                        print(f"   - {issue}")
                    all_valid = False
            
            if all_valid:
                print("✅ 攻擊配置驗證通過")
                print(f"📊 已載入 {len(app_config.attacks)} 個攻擊配置:")
                for attack_id, attack_config in app_config.attacks.items():
                    status = "✅" if attack_config.enabled else "❌"
                    print(f"   {status} {attack_config.name} ({attack_config.category.value}) - {len(attack_config.payloads)} payloads")
                    
        except Exception as e:
            print(f"❌ 配置載入失敗: {e}")
        return

    # 導入新系統組件
    from src.config import load_application_config as get_application_config, ConfigurationLoader
    from src.core.provider_manager import ProviderManager
    
    # 初始化組件
    app_config = get_application_config()
    attack_loader = ConfigurationLoader()
    provider_manager = ProviderManager()

    # Handle list commands
    if args.list_providers:
        providers = provider_manager.list_providers()
        print("🔌 Available providers:")
        for provider in providers:
            print(f"  - {provider}")
        return

    if args.list_attacks:
        print("🎯 Available attacks:")
        for attack_id, attack_config in app_config.attacks.items():
            status = "✅" if attack_config.enabled else "❌"
            print(f"  {status} {attack_id}: {attack_config.name}")
            print(f"    Category: {attack_config.category.value}, Severity: {attack_config.severity.value}")
            print(f"    Payloads: {len(attack_config.payloads)}")
        return

    if args.list_categories:
        print("📂 Available attack categories:")
        categories = {}
        for attack_id, attack_config in app_config.attacks.items():
            if not attack_config.enabled:
                continue
            cat = attack_config.category.value
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(attack_config.name)
        
        for category, attack_names in categories.items():
            print(f"  - {category}: {len(attack_names)} attacks")
            for name in attack_names:
                print(f"    • {name}")
        return

    # Handle connection test
    if args.test_connection:
        providers = (
            args.provider.split(",") if args.provider else provider_manager.list_providers()
        )
        print("Testing provider connections...")

        for provider_name in providers:
            provider = provider_manager.get_provider(provider_name.strip())
            if provider:
                success = await provider.test_connection()
                status = "✅ 成功" if success else "❌ 失敗"
                print(f"  {provider_name}: {status}")
            else:
                print(f"  {provider_name}: ❌ 提供商未找到")
        return

    # Parse providers and formats
    providers = [p.strip() for p in args.provider.split(",")]
    formats = [f.strip() for f in args.format.split(",")]

    # Validate providers
    available_providers = provider_manager.list_providers()
    invalid_providers = [p for p in providers if p not in available_providers]
    if invalid_providers:
        print(f"Error: Invalid providers: {invalid_providers}")
        print(f"Available providers: {available_providers}")
        return

    if args.dry_run:
        print("DRY RUN - Would execute:")
        print(f"  Providers: {providers}")
        print(f"  Test type: {args.test_type}")
        print(f"  Attack type: {args.attack or 'all'}")
        print(f"  Target prompt: {args.target or 'none'}")
        print(f"  Report formats: {formats}")
        return

    try:
        # Get provider instance for unified testing
        provider_name = providers[0]  # Use first provider for now
        provider_instance = provider_manager.get_provider(provider_name)
        
        if not provider_instance:
            print(f"❌ Failed to initialize provider: {provider_name}")
            return

        # Run tests based on type
        if args.test_type == "unified":
            # Use new attack configuration system (recommended)
            print(f"🚀 執行攻擊測試 - Provider: {provider_name}")
            
            # Import attack manager and report generator
            from src.core.attacks import AttackManager
            from src.core.report_generator import AttackReportGenerator
            
            attack_manager = AttackManager()
            report_generator = AttackReportGenerator(args.output)
            
            try:
                if args.attack:
                    # Execute specific attack by ID
                    results = await attack_manager.run_single_attack(
                        args.attack, provider_instance, args.target
                    )
                    attack_manager.test_results[args.attack] = results
                    
                elif args.category:
                    # Execute all attacks in category
                    results = await attack_manager.run_category_attacks(
                        args.category, provider_instance, args.target
                    )
                    
                else:
                    # Execute all enabled attacks
                    results = await attack_manager.run_all_attacks(
                        provider_instance, args.target
                    )
                
                # Print test summary
                attack_manager.print_test_summary()
                
                # Generate reports
                print(f"\n📄 生成測試報告...")
                summary = attack_manager.get_test_summary()
                
                # Generate reports based on requested formats
                for format_type in formats:
                    if format_type.lower() == 'markdown':
                        report_generator.generate_markdown_report(summary)
                    elif format_type.lower() == 'json':
                        report_generator.generate_json_report(summary)
                    elif format_type.lower() == 'csv':
                        report_generator.generate_csv_report(summary)
                
                print(f"✅ 攻擊測試完成，報告已保存到 {args.output}")
                
            except Exception as e:
                print(f"❌ 攻擊測試執行失敗: {e}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()

        else:
            # 不支持的測試類型，使用統一模式作為默認
            print(f"⚠️ 不支持的測試類型 '{args.test_type}'，使用統一模式替代")
            args.test_type = "unified"
            
            # 使用新的統一攻擊系統
            from src.core.attacks import AttackManager
            from src.core.report_generator import AttackReportGenerator
            
            # 初始化攻擊管理器和報告生成器
            attack_manager = AttackManager()
            report_generator = AttackReportGenerator(args.output)
            
            try:
                for provider_name in providers:
                    provider_instance = platform.get_provider(provider_name)
                    if not provider_instance:
                        print(f"❌ 提供商 '{provider_name}' 未找到")
                        continue
                    
                    print(f"🚀 執行攻擊測試 - Provider: {provider_name}")
                    
                    if args.attack:
                        # 執行特定攻擊
                        results = await attack_manager.run_single_attack(
                            args.attack, provider_instance, args.target
                        )
                    elif args.category:
                        # 執行特定類別攻擊
                        results = await attack_manager.run_attacks_by_category(
                            args.category, provider_instance, args.target
                        )
                        
                    else:
                        # 執行所有啟用的攻擊
                        results = await attack_manager.run_all_attacks(
                            provider_instance, args.target
                        )
                    
                    # 列印測試摘要
                    attack_manager.print_test_summary()
                    
                    # 生成報告
                    print(f"\n📄 生成測試報告...")
                    summary = attack_manager.get_test_summary()
                    
                    # 根據請求的格式生成報告
                    for format_type in formats:
                        if format_type.lower() == 'markdown':
                            report_generator.generate_markdown_report(summary)
                        elif format_type.lower() == 'json':
                            report_generator.generate_json_report(summary)
                        elif format_type.lower() == 'csv':
                            report_generator.generate_csv_report(summary)
                    
                    print(f"✅ 攻擊測試完成，報告已保存到 {args.output}")
                    
            except Exception as e:
                print(f"❌ 攻擊測試執行失敗: {e}")
                if args.verbose:
                    import traceback
                    traceback.print_exc()

        # Show attack configuration statistics
        if args.verbose and args.test_type == "unified":
            attacks = attack_loader.get_all_attacks()
            enabled_count = len(attack_loader.get_enabled_attacks())
            print(f"\n📊 攻擊配置統計:")
            print(f"   總攻擊數: {len(attacks)}")
            print(f"   啟用攻擊: {enabled_count}")
            print(f"   停用攻擊: {len(attacks) - enabled_count}")
            
            categories = attack_loader.get_categories()
            print(f"   攻擊類別: {len(categories)} ({', '.join(categories)})")

        # Show legacy platform stats for other modes
        elif args.verbose:
            stats = platform.get_platform_stats()
            print(f"\n📊 Platform Statistics:")
            print(f"   Tests run: {stats['total_tests_run']}")
            print(f"   Total attacks: {stats['total_attacks_attempted']}")
            print(f"   Overall success rate: {stats['success_rate']:.1%}")

    except KeyboardInterrupt:
        print("\n⚠ Test interrupted by user")

    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        if args.verbose:
            import traceback

            traceback.print_exc()


def check_environment():
    """Check if required environment variables are set."""
    # 檢查推薦的環境變數
    recommended_vars = {
        "GITHUB_TOKEN": "GitHub Models API (推薦 - 免費額度)",
        "OPENAI_API_KEY": "OpenAI API (可選 - 付費服務)"
    }
    
    available_providers = []
    missing_providers = []

    for var, description in recommended_vars.items():
        if os.getenv(var):
            available_providers.append(f"{var}: {description}")
        else:
            missing_providers.append(f"{var}: {description}")

    if available_providers:
        print("✅ 可用的提供商:")
        for provider in available_providers:
            print(f"   {provider}")
        print()

    if missing_providers:
        print("💡 可設定的額外提供商:")
        for provider in missing_providers:
            print(f"   {provider}")
        print("\n請在 .env 檔案中設定相關 API 金鑰以啟用更多提供商")
        print()


if __name__ == "__main__":
    print("🔒 LLM Prompt Injection Testing Platform")
    print("=" * 50)

    check_environment()

    # Run the async main function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        sys.exit(1)
