"""
Memory management for tracking who Craig has already contacted
"""

import os
from datetime import datetime, timedelta
from typing import Set, Optional


class ReminderMemory:
    """
    Tracks who Craig has reminded today to prevent spam.

    Supports two backends:
    - In-memory (default): Simple set that resets when script restarts
    - Redis (production): Persistent storage with TTL
    """

    def __init__(self, use_redis: bool = False):
        self.use_redis = use_redis
        self._in_memory_reminders: Set[str] = set()
        self._redis_client = None

        if use_redis:
            try:
                import redis
                from config import config
                self._redis_client = redis.Redis(
                    host=config.REDIS_HOST,
                    port=config.REDIS_PORT,
                    db=config.REDIS_DB,
                    decode_responses=True
                )
                # Test connection
                self._redis_client.ping()
                print("✓ Connected to Redis for state management")
            except Exception as e:
                print(f"⚠ Redis connection failed: {e}. Falling back to in-memory storage.")
                self.use_redis = False

    def has_been_reminded(self, employee_email: str, task_type: str = "general") -> bool:
        """
        Check if an employee has already been reminded about a specific task today

        Args:
            employee_email: Employee's email address
            task_type: Type of task (e.g., "training", "mfa", "general")

        Returns:
            True if already reminded, False otherwise
        """
        key = self._get_key(employee_email, task_type)

        if self.use_redis and self._redis_client:
            return bool(self._redis_client.exists(key))
        else:
            return key in self._in_memory_reminders

    def mark_as_reminded(self, employee_email: str, task_type: str = "general") -> None:
        """
        Mark an employee as reminded for a specific task

        Args:
            employee_email: Employee's email address
            task_type: Type of task
        """
        key = self._get_key(employee_email, task_type)

        if self.use_redis and self._redis_client:
            # Set key with 24-hour expiration
            self._redis_client.setex(key, timedelta(hours=24), "1")
        else:
            self._in_memory_reminders.add(key)

    def clear_all(self) -> None:
        """Clear all reminders (useful for testing)"""
        if self.use_redis and self._redis_client:
            # Get all reminder keys and delete them
            pattern = "craig:reminder:*"
            keys = self._redis_client.keys(pattern)
            if keys:
                self._redis_client.delete(*keys)
        else:
            self._in_memory_reminders.clear()

    def get_reminder_count(self) -> int:
        """Get total number of reminders sent today"""
        if self.use_redis and self._redis_client:
            pattern = "craig:reminder:*"
            return len(self._redis_client.keys(pattern))
        else:
            return len(self._in_memory_reminders)

    @staticmethod
    def _get_key(employee_email: str, task_type: str) -> str:
        """Generate storage key for an employee/task combination"""
        return f"craig:reminder:{employee_email}:{task_type}"


# Global instance
_memory_instance: Optional[ReminderMemory] = None


def get_memory(use_redis: bool = None) -> ReminderMemory:
    """
    Get or create the global ReminderMemory instance

    Args:
        use_redis: Override redis setting. If None, uses config setting.

    Returns:
        ReminderMemory instance
    """
    global _memory_instance

    if _memory_instance is None:
        if use_redis is None:
            from config import config
            use_redis = config.USE_REDIS
        _memory_instance = ReminderMemory(use_redis=use_redis)

    return _memory_instance
