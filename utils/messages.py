"""
Message templates and formatting utilities for Craig
"""

from datetime import datetime
from typing import Dict, Any


class MessageTemplates:
    """Message templates for different scenarios"""

    @staticmethod
    def slack_reminder(
        employee_name: str,
        task_name: str,
        task_url: str,
        days_overdue: int,
        estimated_minutes: int = 15
    ) -> str:
        """
        Generate a Slack reminder message

        Args:
            employee_name: First name of employee
            task_name: Name of the compliance task
            task_url: URL to complete the task
            days_overdue: Number of days the task is overdue (0 = due today)
            estimated_minutes: Estimated time to complete

        Returns:
            Formatted Slack message
        """
        if days_overdue == 0:
            urgency = f"is due today"
            tone = "Just a friendly reminder"
        elif days_overdue <= 3:
            urgency = f"is {days_overdue} days overdue"
            tone = "Quick heads up"
        else:
            urgency = f"is {days_overdue} days overdue"
            tone = "Important reminder"

        return f"""Hey {employee_name}! {tone} - your {task_name} {urgency}.

It takes about {estimated_minutes} minutes. Can you knock it out today?

{task_url}

Let me know if you have any questions! 🎯"""

    @staticmethod
    def email_reminder(
        employee_name: str,
        task_name: str,
        task_url: str,
        days_overdue: int,
        compliance_framework: str = "SOC 2"
    ) -> tuple[str, str]:
        """
        Generate an email reminder

        Returns:
            Tuple of (subject, html_body)
        """
        subject = f"Compliance Reminder: {task_name}"

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <p>Hi {employee_name},</p>

            <p>Your <strong>{task_name}</strong> is now <strong>{days_overdue} days overdue</strong>.
            This is required for our {compliance_framework} compliance and needs to be completed ASAP.</p>

            <p>
                <a href="{task_url}"
                   style="display: inline-block; padding: 12px 24px; background-color: #007bff;
                          color: white; text-decoration: none; border-radius: 4px; margin: 10px 0;">
                    Complete {task_name}
                </a>
            </p>

            <p>If you're running into any issues accessing the training, just reply to this email
            and I'll help troubleshoot.</p>

            <p>Thanks,<br>Craig</p>

            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="font-size: 12px; color: #666;">
                This is an automated reminder from Craig, your AI Compliance Manager.
                Questions? Reply to this email or message me on Slack.
            </p>
        </body>
        </html>
        """

        return subject, html_body

    @staticmethod
    def email_escalation(
        employee_name: str,
        manager_name: str,
        task_name: str,
        task_url: str,
        days_overdue: int
    ) -> tuple[str, str]:
        """
        Generate an escalation email (CC manager)

        Returns:
            Tuple of (subject, html_body)
        """
        subject = f"URGENT: {task_name} - {days_overdue} Days Overdue"

        html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <p>Hi {employee_name},</p>

            <p>Your <strong>{task_name}</strong> is now <strong style="color: #dc3545;">
            {days_overdue} days overdue</strong>, which is impacting our compliance audit timeline.</p>

            <p>I'm looping in {manager_name} to help prioritize this.</p>

            <p>
                <a href="{task_url}"
                   style="display: inline-block; padding: 12px 24px; background-color: #dc3545;
                          color: white; text-decoration: none; border-radius: 4px; margin: 10px 0;">
                    Complete {task_name} Now
                </a>
            </p>

            <p>If there are any blockers preventing you from completing this,
            let's get them resolved immediately.</p>

            <p>Thanks,<br>Craig</p>

            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="font-size: 12px; color: #666;">
                This is an escalated reminder from Craig, your AI Compliance Manager.
            </p>
        </body>
        </html>
        """

        return subject, html_body

    @staticmethod
    def celebration_message(employee_name: str, task_name: str) -> str:
        """
        Generate a celebration message when someone completes a task

        Returns:
            Slack message
        """
        return f"""Hey {employee_name}! 🎉

Just saw you completed your {task_name} - thank you! ✅

One less thing to worry about. Really appreciate you staying on top of it!"""

    @staticmethod
    def weekly_summary(
        compliance_percentage: float,
        completed_this_week: list[Dict[str, Any]],
        outstanding_items: list[Dict[str, Any]],
        upcoming_deadlines: list[Dict[str, Any]]
    ) -> str:
        """
        Generate weekly summary message for Slack channel

        Args:
            compliance_percentage: Overall compliance percentage
            completed_this_week: List of {name, task} dicts
            outstanding_items: List of {name, task, days_overdue} dicts
            upcoming_deadlines: List of {name, date} dicts

        Returns:
            Formatted Slack message
        """
        today = datetime.now().strftime("%B %d, %Y")

        # Build completed section
        completed_section = ""
        if completed_this_week:
            completed_names = ", ".join([item["name"] for item in completed_this_week[:5]])
            if len(completed_this_week) > 5:
                completed_names += f", and {len(completed_this_week) - 5} others"
            completed_section = f"- **{len(completed_this_week)} employees** completed compliance tasks ({completed_names})"
        else:
            completed_section = "- No completions this week"

        # Build outstanding section
        outstanding_section = ""
        if outstanding_items:
            for item in outstanding_items:
                urgency = "🔴" if item["days_overdue"] > 10 else "⚠️"
                outstanding_section += f"- {item['name']} - {item['task']} ({item['days_overdue']} days overdue) {urgency}\n"
        else:
            outstanding_section = "✅ No outstanding items!"

        # Build deadlines section
        deadlines_section = ""
        if upcoming_deadlines:
            for deadline in upcoming_deadlines:
                deadlines_section += f"- {deadline['name']}: {deadline['date']}\n"

        return f"""📊 **Weekly Compliance Update - {today}**

Hey team! Here's our compliance status heading into the weekend:

**🎉 This Week's Wins:**
{completed_section}
- Overall compliance: {compliance_percentage:.1f}% 📈

**⚠️ Still Outstanding ({len(outstanding_items)} items):**
{outstanding_section}

**📅 Upcoming Deadlines:**
{deadlines_section}

I'll continue monitoring and sending reminders. If anyone is blocked, just ping me and I'll help troubleshoot!

Have a great weekend! 🚀"""


# Export templates instance
templates = MessageTemplates()
