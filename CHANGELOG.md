# Changelog

Milestones of the build, newest first. The roadmap lives in ROADMAP.md.

## 2026-11-22 - Chained tool calls

One answer can now chain up to 3 tool calls (`MAX_TOOL_CALLS` in
`app/agent/tool_chat.py`), so the model can combine tools, for example read a
file and then calculate with its contents. After the cap it must answer with
the results it already has. Covered by offline tests.

## 2026-11-21 - Calculator and file reader tools

Two more safe tools: `calculate` (arithmetic without `eval`) and
`read_project_file` (read-only, project folder only, hidden files refused).

## 2026-11-17 - Tool-using chat

The model can ask for a tool by replying `TOOL: name argument`; only names in
the registry can run. First tool: `get_current_time`. `/tools` lists the
tools in the chat.

## 2026-11-16 - Local chat with memory

Terminal chat with a local Ollama model, keeping a bounded session history so
follow-up questions work. `/reset` clears the conversation, `/exit` quits.

## 2026-10-12 - Project setup

Initial project skeleton.
