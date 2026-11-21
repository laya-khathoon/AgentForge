"""One answer that may use a tool: ask the model, run a requested tool, ask again."""
from app.agent.parser import parse_tool_request
from app.tools.registry import ToolError, run_tool

TOOL_PROMPT = (
    "You have three tools. "
    "get_current_time: no argument, tells the current local date and time. "
    "calculate: argument is one arithmetic expression, e.g. TOOL: calculate 2 + 3 * 4. "
    "read_project_file: argument is a path inside this project, e.g. TOOL: read_project_file README.md . "
    "To use a tool, reply with exactly: TOOL: tool_name argument . Otherwise answer normally."
)


def answer_with_tools(chat_fn, messages, model):
    """Return the final reply. At most one tool call per answer (no endless loops)."""
    reply = chat_fn(messages, model=model)
    request = parse_tool_request(reply)
    if request is None:
        return reply
    name, argument = request
    try:
        result = run_tool(name, argument)
    except ToolError as exc:
        result = f"Tool error: {exc}"
    followup = messages + [
        {"role": "assistant", "content": reply},
        {"role": "user", "content": f"Tool result: {result}. Now answer my question."},
    ]
    return chat_fn(followup, model=model)
