# Cline Python CLI

A Python implementation of the Cline CLI that mirrors the functionality of the Go CLI.

## Installation

```bash
pip install -e .
```

## Usage

```bash
cline-py [prompt]
```

This Python CLI provides the same functionality as the Go CLI, including:

- Task management (create, pause, send, chat, view, list, open, restore)
- Instance management (list, default, new, kill)
- Configuration management (list, get, set)
- Authentication
- Version information
- Log management
- System health checks

## Requirements

- Python 3.8 or higher
- grpcio
- click
- prompt_toolkit (for interactive features)

## Features

All commands and subcommands from the Go CLI are implemented:

- `cline-py [prompt]` - Create and follow a task
- `cline-py task` - Task management commands
- `cline-py instance` - Instance management commands
- `cline-py config` - Configuration management commands
- `cline-py auth` - Authentication commands
- `cline-py version` - Version information
- `cline-py logs` - Log management commands
- `cline-py doctor` - System health checks

For detailed usage, run `cline-py --help` or `cline-py <command> --help`.
