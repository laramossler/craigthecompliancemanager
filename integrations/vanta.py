"""
Vanta MCP integration for Craig

This module provides a wrapper around the Vanta MCP server tools.
Craig will use Anthropic's SDK with MCP support to query Vanta data.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
import anthropic
from config import config


class VantaIntegration:
    """
    Wrapper for Vanta MCP server operations

    Note: This uses the Anthropic SDK with MCP tools support.
    The actual MCP server connection is configured in claude_desktop_config.json
    """

    def __init__(self, anthropic_client: Optional[anthropic.Anthropic] = None):
        """
        Initialize Vanta integration

        Args:
            anthropic_client: Anthropic client (creates new one if not provided)
        """
        self.client = anthropic_client or anthropic.Anthropic(
            api_key=config.ANTHROPIC_API_KEY
        )
        print("✓ Vanta MCP integration initialized")

    def get_failing_tests(
        self,
        framework_filter: Optional[str] = None,
        test_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all failing compliance tests from Vanta

        Args:
            framework_filter: Optional framework to filter by (e.g., "soc2", "iso27001")
            test_type: Optional test type to filter by

        Returns:
            List of failing test objects
        """
        # This is a simplified wrapper - in production, you'd call the Vanta MCP
        # tools through the Anthropic SDK with MCP support

        # For now, this returns mock data structure
        # Real implementation would use: client.messages.create() with tool_choice
        return []

    def get_test_entities(
        self,
        test_id: str,
        status_filter: str = "FAILING"
    ) -> List[Dict[str, Any]]:
        """
        Get entities (employees) failing a specific test

        Args:
            test_id: Vanta test ID
            status_filter: Status to filter by (default: "FAILING")

        Returns:
            List of employee entities with test status
        """
        # Real implementation would use MCP tools
        return []

    def get_person(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get person details from Vanta

        Args:
            email: Person's email address

        Returns:
            Person object or None
        """
        # Real implementation would use MCP tools
        return None

    def get_compliance_metrics(self) -> Dict[str, Any]:
        """
        Get overall compliance metrics

        Returns:
            Dict with compliance stats
        """
        # Real implementation would aggregate test results
        return {
            "total_tests": 0,
            "passing_tests": 0,
            "failing_tests": 0,
            "compliance_percentage": 0.0
        }


class VantaQuery:
    """
    High-level Vanta query interface for Craig

    This class provides a simpler interface for common queries that Craig makes.
    It wraps the Vanta MCP integration and handles data parsing.
    """

    def __init__(self, vanta_integration: Optional[VantaIntegration] = None):
        """Initialize with Vanta integration"""
        self.vanta = vanta_integration or VantaIntegration()

    def get_employees_needing_training(self) -> List[Dict[str, Any]]:
        """
        Get all employees who need to complete security training

        Returns:
            List of dicts: {
                "email": str,
                "name": str,
                "days_overdue": int,
                "task_name": str,
                "task_url": str,
                "manager_email": str (optional)
            }
        """
        # Query Vanta for security training test
        # Real implementation would:
        # 1. Find security training test ID
        # 2. Get all failing entities
        # 3. Enrich with person data
        # 4. Calculate days overdue
        # 5. Return structured data

        return []

    def get_employees_missing_mfa(self, service: str = "github") -> List[Dict[str, Any]]:
        """
        Get all employees who need to enable MFA

        Args:
            service: Service name (e.g., "github", "slack", "google")

        Returns:
            List of employee dicts
        """
        return []

    def get_team_compliance_status(self, team_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get compliance status for a team or entire org

        Args:
            team_name: Optional team name filter

        Returns:
            Dict with compliance breakdown
        """
        return {
            "team_name": team_name or "All Teams",
            "total_employees": 0,
            "compliant_employees": 0,
            "non_compliant_employees": 0,
            "compliance_percentage": 0.0,
            "outstanding_tasks": []
        }


# Note: Since we're using Claude with MCP, the actual Vanta queries
# will be handled by Craig (the AI agent) using MCP tools directly.
# This module provides a structured interface for Python code to interact
# with Vanta data, but the primary integration happens through Claude's
# MCP tool use.

# For the real implementation, Craig will use prompts like:
# "Query Vanta for all employees failing security training tests"
# And Claude will automatically use the MCP tools to get the data.


def create_vanta_query_prompt(query_type: str, **kwargs) -> str:
    """
    Create a prompt for Craig to query Vanta data

    Args:
        query_type: Type of query (e.g., "failing_training", "missing_mfa")
        **kwargs: Additional parameters for the query

    Returns:
        Formatted prompt for Claude
    """
    prompts = {
        "failing_training": """Query Vanta to get all employees who have not completed their security awareness training.

For each employee, I need:
- Email address
- Full name
- How many days overdue their training is
- Direct link to complete the training
- Their manager's email (if available)

Return the data in a structured format I can use to send reminders.""",

        "missing_mfa": f"""Query Vanta to get all employees who have not enabled MFA for {kwargs.get('service', 'GitHub')}.

For each employee, I need:
- Email address
- Full name
- How many days this has been flagged
- Setup guide link

Return the data in a structured format.""",

        "compliance_summary": """Query Vanta to get overall compliance metrics.

I need:
- Total number of employees
- Number passing all compliance tests
- Number with outstanding items
- Overall compliance percentage
- Breakdown by test type (training, MFA, background checks, etc.)

Return as a summary I can share in our weekly update.""",

        "team_status": f"""Query Vanta for compliance status of the {kwargs.get('team_name', 'Engineering')} team.

For each team member, show:
- Name
- Outstanding compliance items (if any)
- Days overdue for each item

Return a team summary."""
    }

    return prompts.get(query_type, "")


# Global instance
_vanta_instance: Optional[VantaIntegration] = None


def get_vanta() -> VantaIntegration:
    """Get or create the global Vanta integration instance"""
    global _vanta_instance

    if _vanta_instance is None:
        _vanta_instance = VantaIntegration()

    return _vanta_instance
