"""Registry of tools the agent may use. Only names listed here can ever run."""
from app.tools.calculator import calculate
from app.tools.clock import get_current_time
from app.tools.file_reader import FileReadError, read_project_file
from app.tools.unit_convert import unit_convert
from app.tools.word_count import word_count


class ToolError(Exception):
    """Raised when a requested tool does not exist."""


def _clock(_argument=None):
    return get_current_time()


TOOLS = {
    "get_current_time": _clock,
    "calculate": calculate,
    "read_project_file": read_project_file,
    "word_count": word_count,
    "unit_convert": unit_convert,
}


def run_tool(name, argument=None):
    """Run a registered tool by name and return its text result.

    A refused file read becomes a text result (not a crash), so the model can
    explain the refusal to the user.
    """
    tool = TOOLS.get(name)
    if tool is None:
        raise ToolError(f"Unknown tool: {name}")
    try:
        return tool(argument)
    except FileReadError as exc:
        return f"File tool: {exc}"
