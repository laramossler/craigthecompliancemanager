"""
Email integration for Craig using SendGrid
"""

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import Optional, List
from config import config


class EmailIntegration:
    """Wrapper for SendGrid email operations"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize SendGrid client

        Args:
            api_key: SendGrid API key (uses config if not provided)
        """
        self.api_key = api_key or config.SENDGRID_API_KEY
        self.client = SendGridAPIClient(api_key=self.api_key)
        self.from_email = Email(config.EMAIL_FROM_ADDRESS, config.EMAIL_FROM_NAME)
        self.dry_run = config.DRY_RUN

        print(f"✓ SendGrid initialized (from: {config.EMAIL_FROM_ADDRESS})")

    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        cc_emails: Optional[List[str]] = None,
        plain_text: Optional[str] = None
    ) -> bool:
        """
        Send an email via SendGrid

        Args:
            to_email: Recipient email address
            subject: Email subject line
            html_content: HTML body content
            cc_emails: Optional list of CC recipients
            plain_text: Optional plain text version (auto-generated if not provided)

        Returns:
            True if successful, False otherwise
        """
        if self.dry_run:
            print(f"[DRY RUN] Would send email to {to_email}:")
            print(f"  Subject: {subject}")
            if cc_emails:
                print(f"  CC: {', '.join(cc_emails)}")
            print(f"  Body preview: {html_content[:100]}...")
            return True

        try:
            # Create message
            message = Mail(
                from_email=self.from_email,
                to_emails=To(to_email),
                subject=subject,
                html_content=Content("text/html", html_content)
            )

            # Add plain text version if provided
            if plain_text:
                message.add_content(Content("text/plain", plain_text))

            # Add CC recipients
            if cc_emails:
                for cc_email in cc_emails:
                    message.add_cc(cc_email)

            # Send email
            response = self.client.send(message)

            if response.status_code in [200, 201, 202]:
                if config.DEBUG:
                    print(f"✓ Sent email to {to_email} (status: {response.status_code})")
                return True
            else:
                print(f"✗ Failed to send email to {to_email}: HTTP {response.status_code}")
                return False

        except Exception as e:
            print(f"✗ Error sending email to {to_email}: {str(e)}")
            return False

    def send_batch_emails(
        self,
        recipients: List[dict]
    ) -> dict:
        """
        Send multiple emails in batch

        Args:
            recipients: List of dicts with keys: to_email, subject, html_content, cc_emails (optional)

        Returns:
            Dict with {
                "total": int,
                "successful": int,
                "failed": int,
                "errors": List[str]
            }
        """
        results = {
            "total": len(recipients),
            "successful": 0,
            "failed": 0,
            "errors": []
        }

        for recipient in recipients:
            success = self.send_email(
                to_email=recipient["to_email"],
                subject=recipient["subject"],
                html_content=recipient["html_content"],
                cc_emails=recipient.get("cc_emails")
            )

            if success:
                results["successful"] += 1
            else:
                results["failed"] += 1
                results["errors"].append(f"Failed to send to {recipient['to_email']}")

        return results

    def send_reminder(
        self,
        to_email: str,
        employee_name: str,
        task_name: str,
        task_url: str,
        days_overdue: int,
        manager_email: Optional[str] = None
    ) -> bool:
        """
        Send a compliance reminder email using standard templates

        Args:
            to_email: Employee email
            employee_name: Employee first name
            task_name: Name of the compliance task
            task_url: URL to complete the task
            days_overdue: Number of days overdue
            manager_email: Optional manager email to CC (for escalations)

        Returns:
            True if successful
        """
        from utils.messages import templates

        if manager_email:
            # Escalation email
            subject, html_content = templates.email_escalation(
                employee_name=employee_name,
                manager_name="your manager",  # Could be looked up from org chart
                task_name=task_name,
                task_url=task_url,
                days_overdue=days_overdue
            )
            cc_emails = [manager_email]
        else:
            # Standard reminder email
            subject, html_content = templates.email_reminder(
                employee_name=employee_name,
                task_name=task_name,
                task_url=task_url,
                days_overdue=days_overdue
            )
            cc_emails = None

        return self.send_email(
            to_email=to_email,
            subject=subject,
            html_content=html_content,
            cc_emails=cc_emails
        )


# Global instance
_email_instance: Optional[EmailIntegration] = None


def get_email() -> EmailIntegration:
    """Get or create the global Email integration instance"""
    global _email_instance

    if _email_instance is None:
        _email_instance = EmailIntegration()

    return _email_instance
