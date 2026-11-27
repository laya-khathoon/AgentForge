"""Sixth AgentForge tool: count the days between two dates.

Argument format: `<date> to <date>` with dates written as YYYY-MM-DD, for
example `2026-11-27 to 2026-12-25`. Only the standard library parser is used.
"""
from datetime import date

_MAX_CHARS = 100


def _parse_date(text):
    """Return a date for YYYY-MM-DD text, or raise ValueError."""
    return date.fromisoformat(text.strip())


def _days_between(first, second):
    """Signed number of days from first to second."""
    return (second - first).days


def _describe(days):
    """Turn a day count into text such as '28 days (4 weeks)'."""
    size = abs(days)
    weeks, rest = divmod(size, 7)
    label = "day" if size == 1 else "days"
    if weeks == 0:
        return f"{size} {label}"
    parts = [f"{weeks} week" + ("" if weeks == 1 else "s")]
    if rest:
        parts.append(f"{rest} day" + ("" if rest == 1 else "s"))
    return f"{size} {label} ({' '.join(parts)})"
