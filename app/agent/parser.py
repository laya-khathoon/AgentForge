"""Detect when the model asks for a tool. The accepted form is: TOOL: name [argument]"""
import re

TOOL_REQUEST = re.compile(r"^\s*TOOL:\s*([a-z_]+)(?:[ \t]+(\S.*?))?\s*$")


def parse_tool_request(reply):
    """Return (tool_name, argument) if the whole reply is a tool request, else None.

    The argument is the text after the tool name (for example the expression in
    "TOOL: calculate 2 + 2"), or None when the tool needs no argument.
    """
    match = TOOL_REQUEST.match(reply or "")
    if not match:
        return None
    return match.group(1), match.group(2)
