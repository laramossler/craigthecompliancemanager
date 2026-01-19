"""
Daily compliance check workflow

This workflow runs every weekday morning to:
1. Query Vanta for failing tests
2. Identify employees who need reminders
3. Send appropriate messages via Slack or email
4. Track who's been reminded
"""

from typing import List, Dict, Any
from datetime import datetime
import anthropic
from config import config
from integrations.slack import get_slack
from integrations.email import get_email
from utils.memory import get_memory
from utils.messages import templates


class DailyCheckWorkflow:
    """Orchestrates Craig's daily compliance check"""

    def __init__(self):
        """Initialize workflow with integrations"""
        self.slack = get_slack()
        self.email = get_email()
        self.memory = get_memory()
        self.anthropic_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)

        print(f"Daily Check Workflow initialized for {config.COMPANY_NAME}")

    def run(self) -> Dict[str, Any]:
        """
        Run the daily compliance check workflow

        Returns:
            Dict with results: {
                "total_checked": int,
                "slack_sent": int,
                "emails_sent": int,
                "escalations": int,
                "errors": List[str]
            }
        """
        print(f"\n{'='*60}")
        print(f"Craig's Daily Compliance Check - {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
        print(f"{'='*60}\n")

        results = {
            "total_checked": 0,
            "slack_sent": 0,
            "emails_sent": 0,
            "escalations": 0,
            "errors": [],
            "timestamp": datetime.now().isoformat()
        }

        try:
            # Step 1: Use Claude with MCP to query Vanta
            print("📊 Querying Vanta for compliance data...")
            compliance_data = self._query_vanta_via_claude()

            # Step 2: Process each employee with outstanding tasks
            if compliance_data:
                results["total_checked"] = len(compliance_data)
                for employee in compliance_data:
                    self._process_employee(employee, results)
            else:
                print("✓ No compliance issues found - everyone is up to date!")

            # Step 3: Print summary
            self._print_summary(results)

        except Exception as e:
            error_msg = f"Error running daily check: {str(e)}"
            print(f"✗ {error_msg}")
            results["errors"].append(error_msg)

        return results

    def _query_vanta_via_claude(self) -> List[Dict[str, Any]]:
        """
        Use Claude with MCP tools to query Vanta for failing compliance tests

        Returns:
            List of employees with compliance issues
        """
        # This is where Craig (Claude) queries Vanta via MCP
        # For now, returning mock data structure

        # In production, this would be something like:
        # response = self.anthropic_client.messages.create(
        #     model=config.ANTHROPIC_MODEL,
        #     max_tokens=4000,
        #     system=config.get_system_prompt(),
        #     messages=[{
        #         "role": "user",
        #         "content": "Query Vanta for all employees with failing compliance tests..."
        #     }]
        # )
        # Then parse Claude's structured response

        # Mock data for development
        mock_data = [
            {
                "email": "sarah@company.com",
                "name": "Sarah Chen",
                "first_name": "Sarah",
                "task_name": "Security Awareness Training",
                "task_url": "https://knowbe4.com/training/abc123",
                "days_overdue": 3,
                "manager_email": None
            },
            {
                "email": "mike@company.com",
                "name": "Mike Wilson",
                "first_name": "Mike",
                "task_name": "Security Awareness Training",
                "task_url": "https://knowbe4.com/training/def456",
                "days_overdue": 10,
                "manager_email": None
            }
        ]

        return mock_data if not config.DRY_RUN else []

    def _process_employee(self, employee: Dict[str, Any], results: Dict[str, Any]) -> None:
        """
        Process a single employee's compliance issues

        Args:
            employee: Employee data dict
            results: Results dict to update
        """
        email = employee["email"]
        first_name = employee["first_name"]
        task_name = employee["task_name"]
        task_url = employee["task_url"]
        days_overdue = employee["days_overdue"]
        manager_email = employee.get("manager_email")

        # Check if we've already reminded them today
        if self.memory.has_been_reminded(email, task_name):
            print(f"  ↷ Skipping {first_name} - already reminded today")
            return

        # Determine action based on days overdue
        action = self._determine_action(days_overdue)

        print(f"  → {first_name} ({email}): {task_name} - {days_overdue} days overdue")
        print(f"     Action: {action}")

        success = False

        if action == "slack":
            # Send Slack reminder
            message = templates.slack_reminder(
                employee_name=first_name,
                task_name=task_name,
                task_url=task_url,
                days_overdue=days_overdue
            )
            success = self.slack.send_dm(email, message)

            if success:
                results["slack_sent"] += 1
                self.memory.mark_as_reminded(email, task_name)

        elif action == "email":
            # Send email reminder
            success = self.email.send_reminder(
                to_email=email,
                employee_name=first_name,
                task_name=task_name,
                task_url=task_url,
                days_overdue=days_overdue
            )

            if success:
                results["emails_sent"] += 1
                self.memory.mark_as_reminded(email, task_name)

        elif action == "escalate":
            # Send email with manager CC
            success = self.email.send_reminder(
                to_email=email,
                employee_name=first_name,
                task_name=task_name,
                task_url=task_url,
                days_overdue=days_overdue,
                manager_email=manager_email
            )

            if success:
                results["emails_sent"] += 1
                results["escalations"] += 1
                self.memory.mark_as_reminded(email, task_name)
                print(f"     ⚠️  Escalated to manager")

        if not success:
            error_msg = f"Failed to remind {first_name} ({email})"
            results["errors"].append(error_msg)

    def _determine_action(self, days_overdue: int) -> str:
        """
        Determine what action to take based on days overdue

        Args:
            days_overdue: Number of days the task is overdue

        Returns:
            "slack", "email", or "escalate"
        """
        if days_overdue < config.FIRST_EMAIL_DAYS:
            return "slack"
        elif days_overdue < config.MANAGER_CC_DAYS:
            return "email"
        else:
            return "escalate"

    def _print_summary(self, results: Dict[str, Any]) -> None:
        """Print summary of daily check results"""
        print(f"\n{'='*60}")
        print("Daily Check Summary")
        print(f"{'='*60}")
        print(f"  Total employees checked: {results['total_checked']}")
        print(f"  Slack reminders sent: {results['slack_sent']}")
        print(f"  Email reminders sent: {results['emails_sent']}")
        print(f"  Escalations (manager CC'd): {results['escalations']}")

        if results["errors"]:
            print(f"\n  ⚠️  Errors ({len(results['errors'])}):")
            for error in results["errors"]:
                print(f"    - {error}")

        print(f"{'='*60}\n")


def run_daily_check() -> Dict[str, Any]:
    """
    Convenience function to run the daily check

    Returns:
        Results dict
    """
    workflow = DailyCheckWorkflow()
    return workflow.run()
