"""
Weekly compliance summary workflow

This workflow runs every Friday afternoon to:
1. Query Vanta for overall compliance metrics
2. Generate a summary of the week's progress
3. Post to the compliance channel
"""

from typing import Dict, Any, List
from datetime import datetime
import anthropic
from config import config
from integrations.slack import get_slack
from utils.messages import templates


class WeeklySummaryWorkflow:
    """Orchestrates Craig's weekly compliance summary"""

    def __init__(self):
        """Initialize workflow with integrations"""
        self.slack = get_slack()
        self.anthropic_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

        print(f"Weekly Summary Workflow initialized for {config.COMPANY_NAME}")

    def run(self) -> Dict[str, Any]:
        """
        Run the weekly compliance summary workflow

        Returns:
            Dict with results
        """
        print(f"\n{'='*60}")
        print(f"Craig's Weekly Compliance Summary - {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
        print(f"{'='*60}\n")

        results = {
            "summary_posted": False,
            "error": None,
            "timestamp": datetime.now().isoformat()
        }

        try:
            # Step 1: Query Vanta for weekly data
            print("📊 Gathering compliance data for the week...")
            weekly_data = self._query_vanta_weekly_data()

            # Step 2: Generate summary message
            print("✍️  Generating weekly summary...")
            summary_message = self._generate_summary_message(weekly_data)

            # Step 3: Post to Slack channel
            print(f"📢 Posting to {config.SLACK_COMPLIANCE_CHANNEL}...")
            success = self.slack.post_to_channel(
                channel=config.SLACK_COMPLIANCE_CHANNEL,
                message=summary_message
            )

            results["summary_posted"] = success

            if success:
                print("✓ Weekly summary posted successfully!")
            else:
                print("✗ Failed to post weekly summary")

        except Exception as e:
            error_msg = f"Error running weekly summary: {str(e)}"
            print(f"✗ {error_msg}")
            results["error"] = error_msg

        return results

    def _query_vanta_weekly_data(self) -> Dict[str, Any]:
        """
        Use Claude with MCP tools to query Vanta for weekly compliance data

        Returns:
            Dict with weekly compliance metrics
        """
        # This is where Craig (Claude) queries Vanta via MCP for weekly stats
        # For now, returning mock data structure

        # In production, Craig would:
        # 1. Query current compliance percentage
        # 2. Compare to last week's percentage
        # 3. Get list of completed tasks this week
        # 4. Get list of outstanding tasks
        # 5. Check upcoming deadlines

        mock_data = {
            "compliance_percentage": 87.0,
            "previous_week_percentage": 78.0,
            "completed_this_week": [
                {"name": "Sarah Chen", "task": "Security Awareness Training"},
                {"name": "Mike Wilson", "task": "Security Awareness Training"},
                {"name": "Jessica Park", "task": "MFA Setup (GitHub)"},
                {"name": "Alex Patel", "task": "MFA Setup (GitHub)"},
                {"name": "Priya Singh", "task": "Security Awareness Training"},
                {"name": "David Lee", "task": "MFA Setup (Slack)"},
                {"name": "Rachel Kim", "task": "Security Awareness Training"},
                {"name": "Lisa Wang", "task": "Security Awareness Training"},
            ],
            "outstanding_items": [
                {"name": "Tom Rodriguez", "task": "Security Awareness Training", "days_overdue": 16},
                {"name": "James Chen", "task": "Security Awareness Training", "days_overdue": 5},
                {"name": "Kevin Park", "task": "MFA Setup (GitHub)", "days_overdue": 3},
                {"name": "Amy Liu", "task": "Security Awareness Training", "days_overdue": 2},
            ],
            "upcoming_deadlines": [
                {"name": "SOC 2 Audit Prep", "date": "February 8"},
                {"name": "ISO 27001 Surveillance Audit", "date": "March 1"},
            ]
        }

        return mock_data if not config.DRY_RUN else {}

    def _generate_summary_message(self, data: Dict[str, Any]) -> str:
        """
        Generate the weekly summary message

        Args:
            data: Weekly compliance data

        Returns:
            Formatted message for Slack
        """
        if not data:
            return "📊 **Weekly Compliance Update**\n\nNo data available this week."

        return templates.weekly_summary(
            compliance_percentage=data.get("compliance_percentage", 0),
            completed_this_week=data.get("completed_this_week", []),
            outstanding_items=data.get("outstanding_items", []),
            upcoming_deadlines=data.get("upcoming_deadlines", [])
        )


def run_weekly_summary() -> Dict[str, Any]:
    """
    Convenience function to run the weekly summary

    Returns:
        Results dict
    """
    workflow = WeeklySummaryWorkflow()
    return workflow.run()
