"""Registry of tools the agent may use. Only names listed here can ever run."""
from app.tools.calculator import calculate
from app.tools.clock import get_current_time


class ToolError(Exception):
    """Raised when a requested tool does not exist."""


def _clock(_argument=None):
    return get_current_time()


TOOLS = {
    "get_current_time": _clock,
    "calculate": calculate,
}


def run_tool(name, argument=None):
    """Run a registered tool by name and return its text result."""
    tool = TOOLS.get(name)
    if tool is None:
        raise ToolError(f"Unknown tool: {name}")
    return tool(argument)
