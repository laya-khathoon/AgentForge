"""Fourth AgentForge tool: count the words, lines and characters in a text."""

_MAX_CHARS = 20000


def word_count(text=None):
    """Return the word, line and character counts of `text` as one line of text."""
    if text is not None and not isinstance(text, str):
        return "Cannot count: give some text"
    if not text or not text.strip():
        return "Nothing to count. Give some text after the tool name."
    if len(text) > _MAX_CHARS:
        return f"Cannot count: text is too long (maximum {_MAX_CHARS} characters)"
    words = len(text.split())
    lines = len(text.strip().splitlines())
    return f"{words} words, {lines} lines, {len(text)} characters"
