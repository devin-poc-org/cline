# Cline Python CLI - Usage Guide

## Installation

```bash
cd python-cli
pip install -e .
```

## Overview

The Python CLI mirrors all functionality of the Go CLI, providing the same commands, subcommands, and options.

## Global Flags

These flags are available for all commands:

- `--address <address>` - Cline Core gRPC address (default: localhost:51051)
- `-v, --verbose` - Verbose output
- `-F, --output-format <format>` - Output format: rich, json, or plain (default: rich)

## Commands

### Root Command

Create and follow a task directly:

```bash
# Interactive mode
cline-py

# With prompt
cline-py "Create a REST API with authentication"

# From stdin
echo "Create a todo app" | cline-py
cat prompt.txt | cline-py --yolo

# With options
cline-py "Build a web scraper" --mode act --yolo
cline-py "Add tests" -i screenshot.png -f config.json
```

**Flags:**
- `-i, --image <path>` - Attach image files (can be used multiple times)
- `-f, --file <path>` - Attach files (can be used multiple times)
- `-m, --mode <mode>` - Mode: act or plan (default: plan)
- `-s, --setting <key=value>` - Task settings (can be used multiple times)
- `-y, --yolo` - Enable yolo mode (non-interactive)
- `--no-interactive` - Enable yolo mode (non-interactive)
- `-o, --oneshot` - Full autonomous mode (plan + yolo)

### task - Task Management

Manage Cline tasks.

#### task new

Create a new task:

```bash
cline-py task new "Create a Python script"
echo "Build an API" | cline-py task new
cline-py task new "Add feature" --mode act --yolo
cline-py task new "Fix bug" -i error.png -f logs.txt
```

**Flags:**
- `-i, --image <path>` - Attach image files
- `-f, --file <path>` - Attach files
- `--address <address>` - Specific instance address
- `-m, --mode <mode>` - Mode: act or plan
- `-s, --setting <key=value>` - Task settings
- `-y, --yolo` - Enable yolo mode
- `--no-interactive` - Enable yolo mode

#### task pause

Pause the current task:

```bash
cline-py task pause
cline-py task pause --address localhost:51052
```

**Flags:**
- `--address <address>` - Specific instance address

#### task send

Send a followup message:

```bash
cline-py task send "Please add error handling"
echo "Use TypeScript" | cline-py task send
cline-py task send "Continue" --approve
cline-py task send --deny
cline-py task send --mode act
cline-py task send "Update" -i new-design.png
```

**Flags:**
- `-i, --image <path>` - Attach image files
- `-f, --file <path>` - Attach files
- `--address <address>` - Specific instance address
- `-m, --mode <mode>` - Mode: act or plan
- `-a, --approve` - Approve pending request
- `-d, --deny` - Deny pending request
- `-y, --yolo` - Enable yolo mode
- `--no-interactive` - Enable yolo mode

#### task chat

Chat with the current task interactively:

```bash
cline-py task chat
cline-py task chat --address localhost:51052
```

**Flags:**
- `--address <address>` - Specific instance address

#### task view

View task conversation:

```bash
# Show snapshot
cline-py task view

# Follow forever (non-interactive)
cline-py task view --follow

# Follow until completion
cline-py task view --follow-complete
```

**Flags:**
- `-f, --follow` - Follow conversation forever
- `-c, --follow-complete` - Follow until completion
- `--address <address>` - Specific instance address

#### task list

List recent task history:

```bash
cline-py task list
```

#### task open

Open an existing task by ID:

```bash
cline-py task open <task-id>
cline-py task open abc123 --mode act
cline-py task open abc123 -s model=gpt-4 --yolo
```

**Flags:**
- `--address <address>` - Specific instance address
- `-m, --mode <mode>` - Mode: act or plan
- `-s, --setting <key=value>` - Task settings
- `-y, --yolo` - Enable yolo mode
- `--no-interactive` - Enable yolo mode

#### task restore

Restore task to a checkpoint:

```bash
cline-py task restore <checkpoint-id>
cline-py task restore 1234567890 --type workspace
cline-py task restore 1234567890 --type taskAndWorkspace
```

**Flags:**
- `-t, --type <type>` - Restore type: task, workspace, or taskAndWorkspace (default: task)
- `--address <address>` - Specific instance address

### instance - Instance Management

Manage Cline instances.

#### instance list

List all registered instances:

```bash
cline-py instance list
```

#### instance default

Set the default instance:

```bash
cline-py instance default localhost:51051
```

#### instance new

Create a new instance:

```bash
cline-py instance new
cline-py instance new --default
```

**Flags:**
- `-d, --default` - Set as default instance

#### instance kill

Kill an instance:

```bash
# Kill specific instance
cline-py instance kill localhost:51051

# Kill all CLI instances
cline-py instance kill --all-cli
```

**Flags:**
- `-a, --all-cli` - Kill all CLI instances (excludes JetBrains)

### config - Configuration Management

Manage Cline configuration.

#### config list

List all configuration settings:

```bash
cline-py config list
cline-py config list --address localhost:51052
```

**Flags:**
- `--address <address>` - Specific instance address

#### config get

Get a specific setting:

```bash
cline-py config get api_provider
cline-py config get auto-approval-settings.actions.read-files
```

**Flags:**
- `--address <address>` - Specific instance address

#### config set

Set configuration variables:

```bash
cline-py config set api_provider=anthropic
cline-py config set model=claude-sonnet-4-5
cline-py config set auto-approval-settings.actions.read-files=true
cline-py config set key1=value1 key2=value2
```

**Flags:**
- `--address <address>` - Specific instance address

### auth - Authentication

Authenticate and configure providers.

#### Interactive Mode

Run without flags for interactive menu:

```bash
cline-py auth
```

#### Quick Setup Mode

Configure provider with flags:

```bash
# OpenAI
cline-py auth --provider openai-native --apikey sk-xxx --modelid gpt-4o

# Anthropic
cline-py auth -p anthropic -k sk-ant-xxx -m claude-sonnet-4-5-20250929

# OpenAI Compatible
cline-py auth -p openai -k xxx -m gpt-4 -b https://api.example.com/v1
```

**Flags:**
- `-p, --provider <id>` - Provider ID (openai-native, anthropic, gemini, etc.)
- `-k, --apikey <key>` - API key
- `-m, --modelid <id>` - Model ID
- `-b, --baseurl <url>` - Base URL (optional, for openai provider)

**Supported Providers:**
- openai-native
- openai (OpenAI Compatible)
- anthropic
- gemini
- openrouter
- xai
- cerebras
- ollama

### version - Version Information

Show version information:

```bash
# Full version info
cline-py version

# Short version only
cline-py version --short
```

**Flags:**
- `--short` - Show only version number

### logs - Log Management

Manage Cline log files.

#### logs list

List all log files:

```bash
cline-py logs list
```

#### logs clean

Delete old log files:

```bash
# Delete logs older than 7 days (default)
cline-py logs clean

# Delete logs older than 30 days
cline-py logs clean --older-than 30

# Delete all logs
cline-py logs clean --all

# Dry run (show what would be deleted)
cline-py logs clean --dry-run
cline-py logs clean --all --dry-run
```

**Flags:**
- `--older-than <days>` - Delete logs older than N days (default: 7)
- `--all` - Delete all log files
- `--dry-run` - Show what would be deleted without deleting

#### logs path

Print the logs directory path:

```bash
cline-py logs path
```

### doctor - System Health Check

Check system health and diagnose problems:

```bash
cline-py doctor
```

Performs checks for:
- Terminal configuration
- Python environment
- Required packages
- CLI updates

## Examples

### Basic Workflow

```bash
# Start a new task
cline-py "Create a REST API with user authentication"

# Pause if needed
cline-py task pause

# Send followup message
cline-py task send "Add rate limiting"

# Chat interactively
cline-py task chat
```

### Working with Multiple Instances

```bash
# Create new instance
cline-py instance new --default

# List instances
cline-py instance list

# Use specific instance
cline-py task new "Build feature" --address localhost:51052

# Switch default
cline-py instance default localhost:51052
```

### Configuration

```bash
# View all settings
cline-py config list

# Get specific setting
cline-py config get model

# Update settings
cline-py config set model=gpt-4o
cline-py config set auto-approval-settings.actions.read-files=true
```

### Authentication

```bash
# Interactive setup
cline-py auth

# Quick setup
cline-py auth -p anthropic -k sk-ant-xxx -m claude-sonnet-4-5-20250929
```

### Log Management

```bash
# List logs
cline-py logs list

# Clean old logs
cline-py logs clean --older-than 30

# Get logs directory
cline-py logs path
```

## Input Methods

### Command Line Arguments

```bash
cline-py "Your prompt here"
cline-py task new "Your prompt here"
```

### Standard Input (stdin)

```bash
echo "Your prompt" | cline-py
cat prompt.txt | cline-py --yolo
```

### Interactive Mode

```bash
# Run without arguments for interactive prompt
cline-py
```

## Output Formats

Control output format with `-F` or `--output-format`:

### Rich (default)

Formatted output with colors, tables, and markdown rendering:

```bash
cline-py instance list
cline-py instance list -F rich
```

### JSON

Machine-readable JSON output:

```bash
cline-py instance list -F json
```

### Plain

Simple text output for scripting:

```bash
cline-py instance list -F plain
```

## Environment Variables

- `CLINE_CONFIG_PATH` - Override config directory (default: ~/.cline)
- `NO_AUTO_UPDATE` - Disable automatic updates
- `CI` - Detected automatically, disables updates in CI

## Tips

1. **Use aliases** for frequently used commands:
   ```bash
   alias ct="cline-py task"
   alias ci="cline-py instance"
   ```

2. **Pipe prompts** from files:
   ```bash
   cat requirements.txt | cline-py "Implement these features"
   ```

3. **Combine with other tools**:
   ```bash
   git diff | cline-py "Review these changes"
   ```

4. **Use verbose mode** for debugging:
   ```bash
   cline-py -v task new "Debug this"
   ```

5. **Quick autonomous mode**:
   ```bash
   cline-py --oneshot "Quick task"
   # Equivalent to: cline-py --mode plan --yolo "Quick task"
   ```

## Troubleshooting

### Connection Issues

If you can't connect to Cline Core:

```bash
# Check if instance is running
cline-py instance list

# Start new instance
cline-py instance new

# Check with specific address
cline-py --address localhost:51051 instance list
```

### Health Check

Run doctor to diagnose issues:

```bash
cline-py doctor
```

### Verbose Output

Use verbose mode for detailed information:

```bash
cline-py -v task new "Your task"
```

## Differences from Go CLI

The Python CLI aims to mirror the Go CLI exactly. Key implementation notes:

1. **gRPC Communication**: Uses Python gRPC client libraries
2. **Display**: Uses `rich` library for formatted output
3. **Interactive Input**: Uses `prompt_toolkit` for multiline input
4. **Command Structure**: Uses `click` framework (similar to Cobra in Go)

All commands, subcommands, flags, and behaviors should match the Go CLI.
