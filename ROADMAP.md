# AgentForge roadmap

Seven phases from a local terminal chat to a demo-able autonomous agent. The
rule for every phase: the model's output is data, never code to run, and every
new capability gets offline tests before the next one starts.

## Phase 1 - Local chat (done)

Send one message to a local Ollama model over HTTP and print the reply.
No packages, no API key.

## Phase 2 - Conversation (done)

Keep the last ten turns in memory so follow-up questions work.
`/reset` clears, `/exit` quits.

## Phase 3 - Tools (in progress)

The model asks for a tool with `TOOL: tool_name argument`; only names in the
registry can run. Done: `get_current_time`, `calculate`, `read_project_file`
(read-only, project folder only), `word_count`, `unit_convert`, `date_diff`. One answer can now chain up to 3 tool calls
(`MAX_TOOL_CALLS` in `app/agent/tool_chat.py`); after the cap the model must
answer with the results it has. Next: Phase 4, the first approved write action.

## Phase 4 - Approved actions

A fourth tool that can change something (for example, write a note file in one
allowed folder). Every write needs a typed yes from the user first.

## Phase 5 - Planning

Break a bigger request into steps, show the plan, and walk it with the tools.
Still local, still approval-gated for anything that writes.

## Phase 6 - Interface

A small web UI (FastAPI + a simple page) on top of the same agent core, so the
chat is not tied to the terminal.

## Phase 7 - Packaging

Docker image and a short demo script, so the whole agent runs with one command
on a fresh machine.
