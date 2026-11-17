"""Registry of tools the agent may use. Only names listed here can ever run."""
from app.tools.clock import get_current_time


class ToolError(Exception):
    """Raised when a requested tool does not exist."""


TOOLS = {
    "get_current_time": get_current_time,
}


def run_tool(name):
    """Run a registered tool by name and return its text result."""
    tool = TOOLS.get(name)
    if tool is None:
        raise ToolError(f"Unknown tool: {name}")
    return tool()
