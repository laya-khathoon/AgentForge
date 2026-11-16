# AgentForge

A local-first AI assistant built in Python. **Status: terminal-chat milestone.**
It can send a message to a model running in Ollama on your computer and keep a
short conversation in memory. It is not an autonomous agent yet: it cannot
browse, run commands, read files, or use tools.

## What you need

- Python 3.10 or later.
- Ollama installed and running on the same computer.
- A downloaded local Ollama model. The default is `llama3.2:3b`.
  Its model download is about 2 GB; available memory and speed depend on your
  computer. You can choose another installed model with `--model`.

No Python packages, API key, paid API, or account are needed for this local
chat. Internet is needed to install Ollama and download the model initially.

## First run

1. Install Ollama using its [official instructions](https://docs.ollama.com/quickstart).
2. Open Ollama. In PowerShell or your terminal, download the default model:

   ```text
   ollama pull llama3.2:3b
   ```

3. Get the project, or update an existing copy:

   ```text
   git clone https://github.com/laya-khathoon/AgentForge.git
   cd AgentForge
   ```

   If you already have the project, open its folder and run `git pull` instead.
   Save or commit your own local changes first if Git reports a conflict.

4. From the AgentForge folder, start the chat:

   ```text
   python -m app.main
   ```

   On Windows, use `py -m app.main` if `python` is not available.

5. Type a message after `You:`. The model reply appears after `AgentForge:`.
   `/reset` clears the conversation. `/exit` quits. Ctrl+C also quits.

To use another model that you have downloaded:

```text
python -m app.main --model your-installed-model
```

The shell environment variable `OLLAMA_MODEL` can also set the model name.
This version does not load `.env` files. No credentials belong in the code.

## If something goes wrong

- **Cannot reach Ollama:** open the Ollama app. If it is not serving locally,
  run `ollama serve` in another terminal and leave it running. If it says the
  port is already in use, Ollama may already be running.
- **Model not found:** run `ollama pull llama3.2:3b`, or pass the name of an
  installed model. `ollama list` shows downloaded models.
- **Slow or timed-out reply:** loading a model can take time. The request times
  out after 120 seconds. Try a smaller installed model if needed.
- **Wrong answer:** local models can make mistakes. Check important claims.

## Privacy and limits

Requests go only to `http://127.0.0.1:11434/api/chat`. The Python app does not
write chat history to disk. It retains the last ten successful turns while
running; `/reset` or quitting clears them. Ollama is a separate program with
its own settings and logs, so do not treat this as a guarantee about all
software on your computer. Replies are displayed as text, never executed.

There is no persistent memory, file access, tool execution, agent loop,
web interface, or deployment yet.

## Run the tests

From the project folder:

```text
python -m unittest discover -s tests -t . -v
```

The tests use mock responses and do not need Ollama or a model download. They
cover the HTTP request format, reply parsing, server failures, conversation
history, reset/exit behavior, and the model option. Passing these tests does
not prove a real model is installed or working on your laptop.

## Project structure

```text
app/main.py        terminal loop and local Ollama client
app/agent/         agent logic (planned)
app/tools/         tools (planned)
tests/             offline unit tests
.env.example       reserved template; not loaded by this version
requirements.txt   empty: this milestone uses only Python's standard library
```

## Next milestone

After verifying a real local chat, add one safe read-only tool, with explicit
path restrictions, and tests. Build the action loop after that.

## References

- [Ollama chat API](https://docs.ollama.com/api/chat)
- [Local API introduction](https://docs.ollama.com/api/introduction)
- [Default model: llama3.2:3b](https://ollama.com/library/llama3.2:3b)

## License

MIT. See LICENSE. Model weights have their own license.
