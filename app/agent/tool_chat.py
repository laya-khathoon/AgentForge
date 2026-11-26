"""One answer that may use tools: ask the model, run requested tools, ask again."""
from app.agent.parser import parse_tool_request
from app.tools.registry import ToolError, run_tool

MAX_TOOL_CALLS = 3

TOOL_PROMPT = (
    "You have five tools. "
    "get_current_time: no argument, tells the current local date and time. "
    "calculate: argument is one arithmetic expression, e.g. TOOL: calculate 2 + 3 * 4. "
    "read_project_file: argument is a path inside this project, e.g. TOOL: read_project_file README.md . "
    "word_count: argument is some text, e.g. TOOL: word_count good morning everyone. "
    "unit_convert: argument is a number, a unit, 'to' and a unit, e.g. TOOL: unit_convert 5 km to miles. "
    "To use a tool, reply with exactly: TOOL: tool_name argument . Otherwise answer normally."
)


def answer_with_tools(chat_fn, messages, model):
    """Return the final reply, chaining up to MAX_TOOL_CALLS tool calls.

    Each tool result goes back to the model, so one answer can combine several
    tools (for example read a file, then calculate with its contents). After
    the cap the model is told to answer with what it has, which stops endless
    tool loops without crashing the chat.
    """
    conversation = list(messages)
    for _ in range(MAX_TOOL_CALLS):
        reply = chat_fn(conversation, model=model)
        request = parse_tool_request(reply)
        if request is None:
            return reply
        name, argument = request
        try:
            result = run_tool(name, argument)
        except ToolError as exc:
            result = f"Tool error: {exc}"
        conversation = conversation + [
            {"role": "assistant", "content": reply},
            {"role": "user", "content": f"Tool result: {result}."},
        ]
    conversation = conversation + [
        {"role": "user", "content": (
            "You have reached the tool limit for this answer. "
            "Answer my question now using the tool results above, "
            "without requesting more tools."
        )},
    ]
    final = chat_fn(conversation, model=model)
    if parse_tool_request(final) is not None:
        return (
            "I reached my tool limit for this answer and could not finish. "
            "Please ask again in a simpler way."
        )
    return final
