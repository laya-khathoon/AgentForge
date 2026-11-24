# AgentForge

A local-first AI assistant built in Python. **Status: tool-using chat milestone.**
It sends messages to a model running in Ollama on your computer, keeps a short
conversation in memory, and can use three safe tools: the current time, a
calculator, and a read-only project file reader. It is not an autonomous agent
yet: it cannot browse, run commands, or write files.

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
   `/tools` lists the tools. `/reset` clears the conversation. `/exit` quits. Ctrl+C also quits.

To use another model that you have downloaded:

```text
python -m app.main --model your-installed-model
```

The shell environment variable `OLLAMA_MODEL` can also set the model name.
This version does not load `.env` files. No credentials belong in the code.

## Tools

A tool is a plain Python function listed in `app/tools/registry.py`. Only listed
names can run. The system prompt tells the model to ask for a tool by replying
`TOOL: tool_name argument`, where the argument is optional. `app/agent/parser.py`
checks the reply, `app/agent/tool_chat.py` runs the tool and gives the result
back to the model. One answer can chain up to 3 tool calls, so the model can
combine tools (for example read a file, then calculate with its contents); at
the cap it must answer with the results it already has.

Current tools:

- `get_current_time` - no argument. Tells the current local date and time.
- `calculate` - argument is one arithmetic expression, for example
  `TOOL: calculate 2 + 3 * 4`. Safe by construction: no `eval()`, only numbers
  and `+ - * / // % **` with parentheses, and oversized operands are refused.
- `read_project_file` - argument is a path relative to the project folder, for
  example `TOOL: read_project_file README.md`. Read-only: it cannot write or
  delete, refuses paths outside the project, hidden files (`.env`, `.git`) and
  non-text files, and truncates files larger than 20 KB.
- `word_count` - argument is some text, for example
  `TOOL: word_count good morning everyone`. Replies with the number of words,
  lines and characters; refuses empty input and text over 20,000 characters.

Try them: ask "what time is it?", "what is 128 times 46?", or
"summarize the README file", or "how many words are in this sentence?".

## If something goes wrong

- **Cannot reach Ollama:** open the Ollama app. If it is not serving locally,
  run `ollama serve` in another terminal and leave it running. If it says the
  port is already in use, Ollama may already be running.
- **Model not found:** run `ollama pull llama3.2:3b`, or pass the name of an
  installed model. `ollama list` shows downloaded models.
- **Slow or timed-out reply:** loading a model can take time. The request times
  out after 120 seconds. Try a smaller installed model if needed.
- **Wrong answer:** local models can make mistakes. Check important claims.
- **The model does not use a tool:** small local models sometimes ignore the
  tool instructions. Rephrase the question, or try a larger installed model.

## Privacy and limits

Requests go only to `http://127.0.0.1:11434/api/chat`. The Python app does not
write chat history to disk. It retains the last ten successful turns while
running; `/reset` or quitting clears them. Ollama is a separate program with
its own settings and logs, so do not treat this as a guarantee about all
software on your computer. Replies are displayed as text, never executed.

There is no persistent memory, agent loop, web interface, or deployment yet.
The file tool reads only inside this project folder and can never write.

## Run the tests

From the project folder:

```text
python -m unittest discover -s tests -t . -v
```

The tests use mock responses and do not need Ollama or a model download. They
cover the HTTP request format, reply parsing, server failures, conversation
history, reset/exit behavior, the model option, the tool parser, the
calculator, the read-only file tool, and the tool-using answer loop. Passing
these tests does not prove a real model is installed or working on your laptop.

## Project structure

```text
app/main.py        terminal loop and local Ollama client
app/agent/         parser and tool-using answer loop
app/tools/         clock.py, calculator.py, file_reader.py and registry.py
tests/             offline unit tests
.env.example       reserved template; not loaded by this version
requirements.txt   empty: this milestone uses only Python's standard library
```

## Next milestone

Let one answer chain a small number of tool calls (with a hard cap), then add a
fourth tool the user must approve before it runs. Build the full action loop
after that. See ROADMAP.md for the full seven-phase plan.

## References

- [Ollama chat API](https://docs.ollama.com/api/chat)
- [Local API introduction](https://docs.ollama.com/api/introduction)
- [Default model: llama3.2:3b](https://ollama.com/library/llama3.2:3b)

## License

MIT. See LICENSE. Model weights have their own license.
