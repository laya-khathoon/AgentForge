"""Sixth AgentForge tool: count the days between two dates.

Argument format: `<date> to <date>` with dates written as YYYY-MM-DD, for
example `2026-11-27 to 2026-12-25`. Only the standard library parser is used.
"""
from datetime import date

_MAX_CHARS = 100


def _parse_date(text):
    """Return a date for YYYY-MM-DD text, or raise ValueError."""
    return date.fromisoformat(text.strip())
