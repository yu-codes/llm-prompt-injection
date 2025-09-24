"""Main entry point for the LLM Prompt Injection Testing Platform."""

import asyncio
import argparse
import os
import sys
from pathlib import Path
from typing import List, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.platform import PromptInjectionPlatform


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="LLM Prompt Injection Testing Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run basic test with OpenAI
  python src/main.py --provider openai --attack basic_injection

  # Run comprehensive test
  python src/main.py --provider openai --test-type comprehensive

  # Run against multiple providers
  python src/main.py --provider openai,anthropic --test-type full

  # Test with custom prompt
  python src/main.py --provider openai --target "You are a helpful assistant"

  # Generate specific report formats
  python src/main.py --provider openai --format html,json,pdf
        """
    )
    
    parser.add_argument(
        "--provider", 
        type=str,
        default="openai",
        help="LLM provider(s) to test (comma-separated). Available: openai"
    )
    
    parser.add_argument(
        "--attack",
        type=str,
        help="Specific attack type to run. Available: basic_injection, role_playing"
    )
    
    parser.add_argument(
        "--test-type",
        choices=["single", "comprehensive", "full"],
        default="comprehensive",
        help="Type of test to run"
    )
    
    parser.add_argument(
        "--target",
        type=str,
        help="Target prompt/system message to test against"
    )
    
    parser.add_argument(
        "--format",
        type=str,
        default="html,json",
        help="Report formats (comma-separated): html, json, pdf"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default="./output",
        help="Output directory for reports"
    )
    
    parser.add_argument(
        "--list-providers",
        action="store_true",
        help="List available providers and exit"
    )
    
    parser.add_argument(
        "--list-attacks",
        action="store_true",
        help="List available attack types and exit"
    )
    
    parser.add_argument(
        "--test-connection",
        action="store_true",
        help="Test provider connections and exit"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without executing"
    )
    
    return parser.parse_args()


async def main():
    """Main application entry point."""
    args = parse_arguments()
    
    # Initialize platform
    config = {
        "output_directory": args.output,
        "verbose": args.verbose
    }
    
    platform = PromptInjectionPlatform(config)
    
    # Handle list commands
    if args.list_providers:
        providers = platform.list_providers()
        print("Available providers:")
        for provider in providers:
            print(f"  - {provider}")
        return
    
    if args.list_attacks:
        attacks = platform.list_attacks()
        print("Available attack types:")
        for attack in attacks:
            print(f"  - {attack}")
        return
    
    # Handle connection test
    if args.test_connection:
        providers = args.provider.split(",") if args.provider else platform.list_providers()
        print("Testing provider connections...")
        
        for provider_name in providers:
            await platform.test_provider_connection(provider_name.strip())
        return
    
    # Parse providers and formats
    providers = [p.strip() for p in args.provider.split(",")]
    formats = [f.strip() for f in args.format.split(",")]
    
    # Validate providers
    available_providers = platform.list_providers()
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
        # Run tests based on type
        if args.test_type == "single" and args.attack:
            # Single attack type
            if len(providers) > 1:
                print("Single attack mode supports only one provider")
                return
            
            results = await platform.run_single_attack(
                providers[0], args.attack, args.target
            )
            
            evaluation = platform.evaluate_results(results)
            platform.generate_report(results, evaluation, formats)
            
        elif args.test_type == "comprehensive":
            # Comprehensive test against one provider
            if len(providers) > 1:
                print("Comprehensive test mode supports only one provider")
                return
            
            attack_types = [args.attack] if args.attack else None
            results = await platform.run_comprehensive_test(
                providers[0], attack_types, args.target
            )
            
            evaluation = platform.evaluate_results(results)
            platform.generate_report(results, evaluation, formats)
            
        elif args.test_type == "full":
            # Full assessment across multiple providers
            attack_types = [args.attack] if args.attack else None
            
            assessment_result = await platform.run_full_assessment(
                providers, attack_types, args.target, formats
            )
            
            # Print summary
            summary = assessment_result["summary"]
            print(f"\n📋 Assessment completed:")
            print(f"   Providers tested: {len(summary['providers_tested'])}")
            print(f"   Total attacks: {summary['total_attacks']}")
            print(f"   Success rate: {summary['success_rate']:.1%}")
        
        # Show platform stats
        if args.verbose:
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
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("⚠ Warning: Missing environment variables:")
        for var in missing_vars:
            print(f"   {var}")
        print("\nPlease set these in your .env file or environment")
        print("Some providers may not be available")
        print()


if __name__ == "__main__":
    print("🔒 LLM Prompt Injection Testing Platform")
    print("="*50)
    
    check_environment()
    
    # Run the async main function
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"\n💥 Fatal error: {e}")
        sys.exit(1)