"""One answer that may use a tool: ask the model, run a requested tool, ask again."""
from app.agent.parser import parse_tool_request
from app.tools.registry import ToolError, run_tool

TOOL_PROMPT = (
    "You have one tool: get_current_time. If you need the current date or time, "
    "reply with exactly: TOOL: get_current_time . Otherwise answer normally."
)


def answer_with_tools(chat_fn, messages, model):
    """Return the final reply. At most one tool call per answer (no endless loops)."""
    reply = chat_fn(messages, model=model)
    name = parse_tool_request(reply)
    if name is None:
        return reply
    try:
        result = run_tool(name)
    except ToolError as exc:
        result = f"Tool error: {exc}"
    followup = messages + [
        {"role": "assistant", "content": reply},
        {"role": "user", "content": f"Tool result: {result}. Now answer my question."},
    ]
    return chat_fn(followup, model=model)
