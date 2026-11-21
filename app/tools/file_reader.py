"""Third AgentForge tool: read a text file inside the project folder.

Read-only by design: no writing, no deleting, no paths outside the project
root, no hidden files (so .env and .git stay private), and a size cap so a
large file cannot flood the chat.
"""
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MAX_BYTES = 20_000
TEXT_SUFFIXES = {".py", ".txt", ".md", ".toml", ".cfg", ".json", ".csv", ".yaml", ".yml"}


class FileReadError(Exception):
    """A refused read, explained in words the model can relay to the user."""


def read_project_file(relative_path):
    """Return the text of a project file, or raise FileReadError with the reason."""
    if not relative_path or not relative_path.strip():
        raise FileReadError("give a file path relative to the project folder")
    candidate = (PROJECT_ROOT / relative_path.strip()).resolve()
    if candidate != PROJECT_ROOT and PROJECT_ROOT not in candidate.parents:
        raise FileReadError("only files inside the project folder can be read")
    if any(part.startswith(".") for part in candidate.relative_to(PROJECT_ROOT).parts):
        raise FileReadError("hidden files and folders are private")
    if candidate.suffix.lower() not in TEXT_SUFFIXES:
        raise FileReadError(f"'{candidate.suffix or 'that file'}' is not a readable text file")
    if not candidate.is_file():
        raise FileReadError(f"no such file: {relative_path.strip()}")
    data = candidate.read_bytes()
    truncated = len(data) > MAX_BYTES
    try:
        text = data[:MAX_BYTES].decode("utf-8")
    except UnicodeDecodeError:
        raise FileReadError("that file is not readable text")
    if truncated:
        text += "\n[... file truncated at 20 KB ...]"
    return text
