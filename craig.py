#!/usr/bin/env python3
"""
Craig - The AI Compliance Manager

Main orchestrator for Craig's compliance management workflows.

Usage:
    python craig.py daily-check      # Run daily compliance check
    python craig.py weekly-summary   # Run weekly summary
    python craig.py query "<question>"  # Ask Craig a question
    python craig.py test             # Test integrations
    python craig.py --help           # Show help

Scheduled Usage (cron):
    0 9 * * 1-5 cd /path/to/craig && python craig.py daily-check
    0 16 * * 5 cd /path/to/craig && python craig.py weekly-summary
"""

import sys
import argparse
from datetime import datetime
from typing import Optional

# Import configuration first to validate environment
from config import config

# Import workflows
from workflows.daily_check import run_daily_check
from workflows.weekly_summary import run_weekly_summary

# Import integrations for testing
from integrations.slack import get_slack
from integrations.email import get_email
from integrations.vanta import get_vanta
from utils.memory import get_memory


def main():
    """Main entry point for Craig"""

    # Print banner
    print_banner()

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Craig - The AI Compliance Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python craig.py daily-check          # Run morning compliance check
  python craig.py weekly-summary       # Post weekly summary
  python craig.py test                 # Test all integrations
  python craig.py --dry-run daily-check  # Test without sending messages

For more information, see SETUP.md
        """
    )

    parser.add_argument(
        "command",
        choices=["daily-check", "weekly-summary", "query", "test"],
        help="Command to run"
    )

    parser.add_argument(
        "query_text",
        nargs="?",
        help="Question to ask Craig (only for 'query' command)"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run without actually sending messages"
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug output"
    )

    args = parser.parse_args()

    # Override config with CLI flags
    if args.dry_run:
        config.DRY_RUN = True
        print("🧪 DRY RUN MODE - No messages will be sent\n")

    if args.debug:
        config.DEBUG = True

    # Validate configuration
    valid, errors = config.validate()
    if not valid:
        print("❌ Configuration errors:")
        for error in errors:
            print(f"  - {error}")
        print("\nPlease check your .env file and ensure all required variables are set.")
        print("See .env.example for reference.\n")
        sys.exit(1)

    # Route to appropriate command
    if args.command == "daily-check":
        run_daily_check_command()
    elif args.command == "weekly-summary":
        run_weekly_summary_command()
    elif args.command == "query":
        run_query_command(args.query_text)
    elif args.command == "test":
        run_test_command()


def print_banner():
    """Print Craig's banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║   🤖 Craig - The AI Compliance Manager                   ║
    ║                                                          ║
    ║   Keeping your team compliant, one reminder at a time    ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_daily_check_command():
    """Execute the daily compliance check workflow"""
    print(f"Starting daily compliance check for {config.COMPANY_NAME}...\n")

    try:
        results = run_daily_check()

        # Exit with success code
        if results["errors"]:
            sys.exit(1)  # Some errors occurred
        else:
            sys.exit(0)  # All good

    except Exception as e:
        print(f"\n❌ Fatal error running daily check: {e}")
        sys.exit(1)


def run_weekly_summary_command():
    """Execute the weekly compliance summary workflow"""
    print(f"Generating weekly compliance summary for {config.COMPANY_NAME}...\n")

    try:
        results = run_weekly_summary()

        if results.get("error"):
            print(f"\n❌ Error: {results['error']}")
            sys.exit(1)
        elif results.get("summary_posted"):
            print("\n✅ Weekly summary posted successfully!")
            sys.exit(0)
        else:
            print("\n⚠️  Weekly summary not posted")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Fatal error running weekly summary: {e}")
        sys.exit(1)


def run_query_command(query_text: Optional[str]):
    """Execute an ad-hoc query to Craig"""
    if not query_text:
        print("❌ Error: Please provide a question to ask Craig")
        print("\nExample: python craig.py query \"Who needs to complete training?\"")
        sys.exit(1)

    print(f"Processing your question: {query_text}\n")
    print("🚧 Query functionality coming soon!")
    print("This will allow you to ask Craig questions like:")
    print("  - 'Who on the Engineering team needs to complete training?'")
    print("  - 'What's our current compliance percentage?'")
    print("  - 'Send a reminder to john@company.com about MFA setup'")
    print()


def run_test_command():
    """Test all integrations"""
    print("Testing Craig's integrations...\n")

    test_results = {
        "slack": False,
        "email": False,
        "vanta": False,
        "memory": False
    }

    # Test Slack
    print("1. Testing Slack integration...")
    try:
        slack = get_slack()
        test_results["slack"] = True
        print("   ✅ Slack connected successfully")
    except Exception as e:
        print(f"   ❌ Slack connection failed: {e}")

    # Test Email
    print("\n2. Testing Email integration...")
    try:
        email = get_email()
        test_results["email"] = True
        print("   ✅ SendGrid initialized successfully")
    except Exception as e:
        print(f"   ❌ Email connection failed: {e}")

    # Test Vanta
    print("\n3. Testing Vanta integration...")
    try:
        vanta = get_vanta()
        test_results["vanta"] = True
        print("   ✅ Vanta MCP integration initialized")
        print("   ℹ️  Note: Full Vanta testing requires MCP server running")
    except Exception as e:
        print(f"   ❌ Vanta integration failed: {e}")

    # Test Memory
    print("\n4. Testing Memory/State management...")
    try:
        memory = get_memory()
        # Test basic operations
        memory.mark_as_reminded("test@example.com", "test_task")
        is_reminded = memory.has_been_reminded("test@example.com", "test_task")
        if is_reminded:
            test_results["memory"] = True
            print("   ✅ Memory system working")
        else:
            print("   ❌ Memory system not persisting data")
    except Exception as e:
        print(f"   ❌ Memory system failed: {e}")

    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    all_passed = all(test_results.values())

    for service, passed in test_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {service.upper()}: {status}")

    print("="*60)

    if all_passed:
        print("\n🎉 All tests passed! Craig is ready to go.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Please check your configuration.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Craig shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
