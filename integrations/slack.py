"""
Slack API integration for Craig
"""

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from typing import Optional
from config import config


class SlackIntegration:
    """Wrapper for Slack API operations"""

    def __init__(self, bot_token: Optional[str] = None):
        """
        Initialize Slack client

        Args:
            bot_token: Slack bot token (uses config if not provided)
        """
        self.bot_token = bot_token or config.SLACK_BOT_TOKEN
        self.client = WebClient(token=self.bot_token)
        self.dry_run = config.DRY_RUN

        # Verify connection
        try:
            auth_response = self.client.auth_test()
            self.bot_user_id = auth_response["user_id"]
            self.team_id = auth_response["team_id"]
            print(f"✓ Connected to Slack (bot: {auth_response['user']})")
        except SlackApiError as e:
            print(f"✗ Failed to connect to Slack: {e.response['error']}")
            raise

    def send_dm(self, user_email: str, message: str) -> bool:
        """
        Send a direct message to a user

        Args:
            user_email: User's email address
            message: Message text to send

        Returns:
            True if successful, False otherwise
        """
        if self.dry_run:
            print(f"[DRY RUN] Would send Slack DM to {user_email}:")
            print(f"  {message[:100]}...")
            return True

        try:
            # Look up user by email
            user_response = self.client.users_lookupByEmail(email=user_email)
            user_id = user_response["user"]["id"]

            # Send DM
            response = self.client.chat_postMessage(
                channel=user_id,
                text=message,
                unfurl_links=False,
                unfurl_media=False
            )

            if config.DEBUG:
                print(f"✓ Sent Slack DM to {user_email}")

            return response["ok"]

        except SlackApiError as e:
            error_msg = e.response.get("error", "Unknown error")
            print(f"✗ Failed to send Slack DM to {user_email}: {error_msg}")

            if error_msg == "users_not_found":
                print(f"  → User {user_email} not found in Slack workspace")
            elif error_msg == "channel_not_found":
                print(f"  → Could not open DM channel with {user_email}")

            return False

    def post_to_channel(self, channel: str, message: str, thread_ts: Optional[str] = None) -> bool:
        """
        Post a message to a public channel

        Args:
            channel: Channel name (e.g., "#compliance-updates")
            message: Message text to send
            thread_ts: Optional thread timestamp to reply to

        Returns:
            True if successful, False otherwise
        """
        if self.dry_run:
            print(f"[DRY RUN] Would post to {channel}:")
            print(f"  {message[:100]}...")
            return True

        try:
            response = self.client.chat_postMessage(
                channel=channel,
                text=message,
                thread_ts=thread_ts,
                unfurl_links=False,
                unfurl_media=False
            )

            if config.DEBUG:
                print(f"✓ Posted to {channel}")

            return response["ok"]

        except SlackApiError as e:
            error_msg = e.response.get("error", "Unknown error")
            print(f"✗ Failed to post to {channel}: {error_msg}")

            if error_msg == "channel_not_found":
                print(f"  → Channel {channel} not found or bot not invited")

            return False

    def add_reaction(self, channel: str, timestamp: str, emoji: str) -> bool:
        """
        Add a reaction emoji to a message

        Args:
            channel: Channel ID where message was posted
            timestamp: Message timestamp
            emoji: Emoji name (without colons, e.g., "white_check_mark")

        Returns:
            True if successful, False otherwise
        """
        if self.dry_run:
            print(f"[DRY RUN] Would add reaction :{emoji}: to message")
            return True

        try:
            response = self.client.reactions_add(
                channel=channel,
                timestamp=timestamp,
                name=emoji
            )
            return response["ok"]

        except SlackApiError as e:
            if config.DEBUG:
                print(f"✗ Failed to add reaction: {e.response['error']}")
            return False

    def lookup_user_by_email(self, email: str) -> Optional[dict]:
        """
        Look up user information by email

        Args:
            email: User's email address

        Returns:
            User info dict or None if not found
        """
        try:
            response = self.client.users_lookupByEmail(email=email)
            return response["user"]
        except SlackApiError:
            return None


# Global instance
_slack_instance: Optional[SlackIntegration] = None


def get_slack() -> SlackIntegration:
    """Get or create the global Slack integration instance"""
    global _slack_instance

    if _slack_instance is None:
        _slack_instance = SlackIntegration()

    return _slack_instance
