"""A local terminal chat for AgentForge. Requires a running Ollama server."""
import argparse
import json
import os
import socket
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.agent.tool_chat import TOOL_PROMPT, answer_with_tools

CHAT_URL = "http://127.0.0.1:11434/api/chat"
DEFAULT_MODEL = "llama3.2:3b"
MAX_TURNS = 10
SYSTEM_MESSAGE = {
    "role": "system",
    "content": (
        "You are AgentForge, a helpful local chat assistant. Be clear and honest. "
        "You cannot run commands, browse, or read files. Do not claim you did."
         + TOOL_PROMPT
    ),
}


class ChatError(Exception):
    """An expected model/server failure that can be shown in the terminal."""


def chat(messages, model=DEFAULT_MODEL):
    """Get one non-streaming answer from local Ollama; never run model output."""
    payload = json.dumps({"model": model, "messages": messages, "stream": False})
    request = Request(CHAT_URL, data=payload.encode("utf-8"),
                      headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=120) as response:
            data = json.load(response)
    except HTTPError as exc:
        if exc.code == 404:
            raise ChatError(f"Model not found. Run: ollama pull {model}") from exc
        raise ChatError(f"Ollama returned HTTP {exc.code}. Check the Ollama app.") from exc
    except (URLError, TimeoutError, socket.timeout) as exc:
        raise ChatError("Cannot reach Ollama or the reply timed out. "
                        "Open Ollama, or run ollama serve, then try again.") from exc
    except (ValueError, UnicodeError) as exc:
        raise ChatError("Ollama returned an unreadable response. Try again.") from exc

    message = data.get("message") if isinstance(data, dict) else None
    content = message.get("content") if isinstance(message, dict) else None
    if not isinstance(content, str) or not content.strip():
        raise ChatError("Ollama returned no text. Try another prompt or model.")
    return content.strip()


def run_chat(model, input_fn=input, output_fn=print, chat_fn=chat):
    """Interactive session; history lives in memory only and is size-limited."""
    output_fn("AgentForge local chat")
    output_fn(f"Model: {model}. Commands: /reset, /exit")
    output_fn("One tool: get_current_time. No file access or autonomous actions yet.")
    history = [SYSTEM_MESSAGE.copy()]
    while True:
        try:
            text = input_fn("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            output_fn("Goodbye.")
            return
        if not text:
            continue
        if text.lower() in ("/exit", "/quit"):
            output_fn("Goodbye.")
            return
        if text.lower() == "/reset":
            history = [SYSTEM_MESSAGE.copy()]
            output_fn("Conversation cleared.")
            continue
        pending = history + [{"role": "user", "content": text}]
        try:
            reply = answer_with_tools(chat_fn, pending, model)
        except ChatError as exc:
            output_fn(f"Error: {exc}")
            continue
        except KeyboardInterrupt:
            output_fn("Reply canceled. Goodbye.")
            return
        output_fn(f"AgentForge: {reply}")
        history = pending + [{"role": "assistant", "content": reply}]
        # Keep only complete user/assistant turns plus the system instruction.
        history = [history[0]] + history[1:][-2 * MAX_TURNS:]


def main():
    parser = argparse.ArgumentParser(description="Chat with a local Ollama model.")
    parser.add_argument("--model", default=os.environ.get("OLLAMA_MODEL") or DEFAULT_MODEL,
                        help="An installed Ollama model (default: llama3.2:3b).")
    args = parser.parse_args()
    run_chat(args.model)


if __name__ == "__main__":
    main()
