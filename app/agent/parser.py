"""Detect when the model asks for a tool. The only accepted form is: TOOL: name"""
import re

TOOL_REQUEST = re.compile(r"^\s*TOOL:\s*([a-z_]+)\s*$")


def parse_tool_request(reply):
    """Return the tool name if the whole reply is a tool request, else None."""
    match = TOOL_REQUEST.match(reply or "")
    return match.group(1) if match else None
