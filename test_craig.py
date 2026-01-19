#!/usr/bin/env python3
"""
Test Craig in a safe environment

This script lets you test Craig without needing all the integrations set up.
It will use mock data and run in dry-run mode.
"""

import os
import sys

# Make sure we're in dry-run mode for testing
os.environ['DRY_RUN'] = 'true'
os.environ['DEBUG'] = 'true'

print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   🧪 Craig Test Mode                                     ║
║                                                          ║
║   Running Craig safely with mock data                    ║
║   No real messages will be sent!                         ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

""")

def test_daily_check():
    """Test Craig's daily compliance check workflow"""
    print("=" * 60)
    print("Testing Daily Compliance Check Workflow")
    print("=" * 60)
    print()

    from workflows.daily_check import DailyCheckWorkflow

    workflow = DailyCheckWorkflow()
    results = workflow.run()

    print("\n" + "=" * 60)
    print("Daily Check Test Complete!")
    print("=" * 60)
    print(f"✓ Checked {results['total_checked']} employees")
    print(f"✓ Would send {results['slack_sent']} Slack messages")
    print(f"✓ Would send {results['emails_sent']} emails")
    print(f"✓ Would escalate {results['escalations']} to managers")

    if results['errors']:
        print(f"\n⚠️  Encountered {len(results['errors'])} errors:")
        for error in results['errors']:
            print(f"  - {error}")

    return results

def test_weekly_summary():
    """Test Craig's weekly summary workflow"""
    print("\n" + "=" * 60)
    print("Testing Weekly Summary Workflow")
    print("=" * 60)
    print()

    from workflows.weekly_summary import WeeklySummaryWorkflow

    workflow = WeeklySummaryWorkflow()
    results = workflow.run()

    print("\n" + "=" * 60)
    print("Weekly Summary Test Complete!")
    print("=" * 60)

    if results.get('summary_posted'):
        print("✓ Summary would be posted to Slack")
    elif results.get('error'):
        print(f"✗ Error: {results['error']}")

    return results

def test_integrations():
    """Test that integrations can initialize"""
    print("\n" + "=" * 60)
    print("Testing Integrations")
    print("=" * 60)
    print()

    test_results = {
        "anthropic": False,
        "slack": False,
        "email": False,
    }

    # Test Anthropic (most important for testing)
    print("1. Testing Anthropic API...")
    try:
        from config import config
        if config.ANTHROPIC_API_KEY and config.ANTHROPIC_API_KEY != "your_anthropic_api_key_here":
            print("   ✅ Anthropic API key configured")
            test_results["anthropic"] = True
        else:
            print("   ⚠️  Anthropic API key not set (needed for full functionality)")
            print("      → Edit .env and add your key to ANTHROPIC_API_KEY")
    except Exception as e:
        print(f"   ✗ Error: {e}")

    # Test Slack (optional for testing)
    print("\n2. Testing Slack integration...")
    try:
        from integrations.slack import SlackIntegration
        slack = SlackIntegration()
        print("   ✅ Slack integration initialized (in dry-run mode)")
        test_results["slack"] = True
    except Exception as e:
        print(f"   ⚠️  Slack not configured yet (optional for testing): {e}")

    # Test Email (optional for testing)
    print("\n3. Testing Email integration...")
    try:
        from integrations.email import EmailIntegration
        email = EmailIntegration()
        print("   ✅ Email integration initialized (in dry-run mode)")
        test_results["email"] = True
    except Exception as e:
        print(f"   ⚠️  Email not configured yet (optional for testing): {e}")

    print("\n" + "=" * 60)
    print("Integration Test Summary")
    print("=" * 60)

    if test_results["anthropic"]:
        print("✅ Ready to test Craig with mock data!")
    else:
        print("⚠️  Add your Anthropic API key to .env to continue")

    return test_results

def main():
    """Run all tests"""

    # First test integrations
    integration_results = test_integrations()

    if not integration_results["anthropic"]:
        print("\n" + "=" * 60)
        print("Action Required")
        print("=" * 60)
        print("Please edit .env and set your Anthropic API key:")
        print("  ANTHROPIC_API_KEY=sk-ant-your-key-here")
        print("\nThen run this script again: python test_craig.py")
        return

    # Ask what to test
    print("\n" + "=" * 60)
    print("What would you like to test?")
    print("=" * 60)
    print("1. Daily compliance check workflow")
    print("2. Weekly summary workflow")
    print("3. Both workflows")
    print("4. Exit")
    print()

    choice = input("Enter your choice (1-4): ").strip()

    if choice == "1":
        test_daily_check()
    elif choice == "2":
        test_weekly_summary()
    elif choice == "3":
        test_daily_check()
        test_weekly_summary()
    elif choice == "4":
        print("\n👋 Goodbye!\n")
        return
    else:
        print("\n❌ Invalid choice. Please run again and select 1-4.")
        return

    # Show next steps
    print("\n" + "=" * 60)
    print("Next Steps")
    print("=" * 60)
    print("""
Great! Craig is working in test mode with mock data.

To use Craig with real compliance data, you'll need:

1. ✅ Anthropic API key (you have this!)
2. ⬜ Vanta API credentials → See SETUP.md section "Set Up Vanta"
3. ⬜ Slack bot token → See SETUP.md section "Set Up Slack Bot"
4. ⬜ SendGrid API key → See SETUP.md section "Set Up SendGrid"

Want to keep testing with mock data?
  python test_craig.py

Want to see the full CLI?
  python craig.py --help

Ready to deploy for real?
  1. Get API keys (see SETUP.md)
  2. Update .env with real credentials
  3. Set DRY_RUN=false in .env
  4. Run: python craig.py daily-check

Questions? Check README.md or SETUP.md
""")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Test interrupted. Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
