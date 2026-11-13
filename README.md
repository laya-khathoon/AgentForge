# AgentForge

A free, locally powered autonomous AI agent, built in Python with open-source tools.

**Status: early work in progress.** This repo is currently the project skeleton: the folder structure is in place and the entry point runs. The agent itself is being built next.

## What it does today

Running the app prints a startup message confirming the environment works:

```
$ python app/main.py
AgentForge Autonomous AI Agent
Project environment is working!
Next: connect our local AI model.
```

## Project structure

```
app/
  main.py        entry point
  agent/         agent logic (planned)
  tools/         tools the agent can use (planned)
tests/           unit tests
.env.example     template for environment variables
```

## Run it

You only need Python 3 installed - no packages yet:

```bash
git clone https://github.com/laya-khathoon/AgentForge.git
cd AgentForge
python app/main.py
```

## Run the tests

There is one small test that checks the startup messages. It uses Python's built-in `unittest`, so nothing needs installing:

```bash
python -m unittest discover -s tests -t .
```

## Roadmap

- Connect a local AI model as the agent's brain
- Give the agent its first tools
- Add more tests as features are built
