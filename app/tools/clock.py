"""First AgentForge tool: tell the current local date and time."""
from datetime import datetime


def get_current_time(now=None):
    """Return the current local time as text. `now` lets tests pass a fixed time."""
    moment = now or datetime.now()
    return moment.strftime("%A, %d %B %Y, %I:%M %p")
