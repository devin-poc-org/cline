# Cline Python CLI

A Python implementation of the Cline CLI that mirrors the functionality of the Go CLI.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Development Setup](#development-setup)
- [Debugging](#debugging)
- [Testing](#testing)
- [Architecture](#architecture)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Install from Source

1. Clone the repository and navigate to the python-cli directory:
   ```bash
   cd python-cli
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

3. Verify installation:
   ```bash
   python3 -m cline_cli.main --help
   ```

### Dependencies

The following packages will be installed automatically:
- `click>=8.0.0` - CLI framework
- `grpcio>=1.50.0` - gRPC communication
- `grpcio-tools>=1.50.0` - gRPC code generation
- `prompt_toolkit>=3.0.0` - Interactive prompts
- `rich>=13.0.0` - Rich terminal output
- `protobuf>=4.21.0` - Protocol buffers

## Quick Start

### Basic Usage

Run the CLI directly using Python:

```bash
# Show help
python3 -m cline_cli.main --help

# Create a task with a prompt
python3 -m cline_cli.main "Create a REST API with authentication"

# Interactive mode
python3 -m cline_cli.main

# Pipe input from stdin
echo "Build a todo app" | python3 -m cline_cli.main

# With options
python3 -m cline_cli.main "Add tests" --mode act --yolo
```

### Common Commands

```bash
# Task management
python3 -m cline_cli.main task new "Create a Python script"
python3 -m cline_cli.main task list
python3 -m cline_cli.main task view
python3 -m cline_cli.main task pause

# Instance management
python3 -m cline_cli.main instance list
python3 -m cline_cli.main instance new

# Configuration
python3 -m cline_cli.main config list
python3 -m cline_cli.main config set model=gpt-4o

# Authentication
python3 -m cline_cli.main auth --provider anthropic --apikey sk-ant-xxx --modelid claude-sonnet-4-5

# Version info
python3 -m cline_cli.main version

# System health check
python3 -m cline_cli.main doctor
```

## Usage Examples

### Creating Tasks

```bash
# Simple task
python3 -m cline_cli.main "Create a web scraper"

# With images and files
python3 -m cline_cli.main "Fix this bug" -i screenshot.png -f error.log

# With settings
python3 -m cline_cli.main "Build API" -s model=gpt-4o -s temperature=0.7

# In yolo mode (non-interactive)
python3 -m cline_cli.main "Quick task" --yolo

# Full autonomous mode
python3 -m cline_cli.main "Implement feature" --oneshot
```

### Working with Multiple Instances

```bash
# List all instances
python3 -m cline_cli.main instance list

# Create new instance
python3 -m cline_cli.main instance new --default

# Use specific instance
python3 -m cline_cli.main --address localhost:51052 task list

# Set default instance
python3 -m cline_cli.main instance default localhost:51052
```

### Configuration Management

```bash
# View all settings
python3 -m cline_cli.main config list

# Get specific setting
python3 -m cline_cli.main config get model

# Update settings
python3 -m cline_cli.main config set model=gpt-4o
python3 -m cline_cli.main config set auto-approval-settings.actions.read-files=true
```

### Output Formats

```bash
# Rich format (default) - styled terminal output
python3 -m cline_cli.main instance list

# JSON format - for scripting
python3 -m cline_cli.main -F json instance list

# Plain format - simple text
python3 -m cline_cli.main -F plain instance list
```

## Development Setup

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

This installs:
- `pytest>=7.0.0` - Testing framework

### Project Structure

```
python-cli/
├── cline_cli/
│   ├── __init__.py
│   ├── main.py              # CLI entry point
│   ├── commands/            # Command implementations
│   │   ├── task.py
│   │   ├── instance.py
│   │   ├── config.py
│   │   ├── auth.py
│   │   ├── version.py
│   │   ├── logs.py
│   │   └── doctor.py
│   ├── core/                # Business logic
│   │   ├── task_manager.py
│   │   ├── instance_manager.py
│   │   ├── config_manager.py
│   │   ├── auth_manager.py
│   │   ├── logs_manager.py
│   │   ├── doctor.py
│   │   └── grpc_client.py   # gRPC communication
│   └── utils/               # Utilities
│       ├── display.py       # Output formatting
│       ├── global_config.py # Global configuration
│       └── interactive.py   # Interactive prompts
├── tests/                   # Test suite
├── .vscode/
│   └── launch.json          # VS Code debug configurations
├── setup.py                 # Package configuration
├── pytest.ini               # Pytest configuration
├── requirements-dev.txt     # Development dependencies
├── README.md                # This file
└── USAGE.md                 # Detailed usage guide
```

## Debugging

### VS Code Setup

The repository includes a `.vscode/launch.json` file with pre-configured debug configurations:

1. **Python: Cline CLI** - Debug the CLI with no arguments (interactive mode)
2. **Python: Cline CLI with Args** - Debug with custom arguments
3. **Python: Task New** - Debug task creation
4. **Python: Instance List** - Debug instance listing
5. **Python: Config List** - Debug configuration listing
6. **Python: Version** - Debug version command
7. **Python: Doctor** - Debug health check
8. **Python: Current File** - Debug the currently open file
9. **Python: Run Tests** - Debug all tests
10. **Python: Run Current Test File** - Debug current test file

### Using the Debugger

1. Open the project in VS Code
2. Open the file you want to debug
3. Set breakpoints by clicking in the gutter
4. Press `F5` or select "Run > Start Debugging"
5. Choose a debug configuration from the dropdown

### Manual Debugging

You can also debug manually using Python's debugger:

```bash
# Using pdb
python3 -m pdb -m cline_cli.main task list

# Using ipdb (if installed)
python3 -m ipdb -m cline_cli.main task list
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_commands.py

# Run specific test
pytest tests/test_commands.py::TestTaskCommands::test_task_help

# Run with coverage
pytest --cov=cline_cli --cov-report=html
```

### Test Structure

The test suite includes:
- **58 unit tests** covering all commands and functionality
- Command tests for all CLI commands
- Manager tests for business logic
- Display tests for output formatting
- Configuration tests for global settings

All tests are located in the `tests/` directory and use pytest.

## Architecture

### Command Flow

```
User Input → CLI (main.py)
           ↓
    Command Module (commands/)
           ↓
    Manager Class (core/)
           ↓
    gRPC Client (core/grpc_client.py)
           ↓
    Cline Core Service
```

### Key Components

1. **CLI Layer** (`main.py`, `commands/`)
   - Handles user input and command parsing
   - Uses Click framework for command structure
   - Validates arguments and options

2. **Business Logic** (`core/`)
   - Manager classes handle domain logic
   - Separate concerns (tasks, instances, config, etc.)
   - Coordinate between CLI and gRPC client

3. **Communication** (`core/grpc_client.py`)
   - gRPC client for communication with cline-core
   - Currently placeholder implementation
   - Needs protobuf-generated code

4. **Display** (`utils/display.py`)
   - Formats output in rich, json, or plain formats
   - Uses Rich library for styled terminal output
   - Handles tables, markdown, and progress indicators

## Important Notes

### gRPC Implementation Status

⚠️ **The gRPC client is currently a placeholder.** All gRPC methods in `core/grpc_client.py` are stubs that need to be implemented with actual protobuf-generated code. The CLI interface is complete and tested, but it won't communicate with cline-core until the gRPC layer is implemented.

### Next Steps

To make this CLI fully functional:

1. Generate Python gRPC code from protobuf definitions
2. Implement actual gRPC methods in `core/grpc_client.py`
3. Add integration tests with real cline-core instance
4. Test all workflows end-to-end

## Troubleshooting

### Command Not Found

If you get "command not found" errors, the Python bin directory may not be in your PATH. Use the full module path:

```bash
python3 -m cline_cli.main [command]
```

### Import Errors

If you get import errors, ensure you've installed the package:

```bash
pip install -e .
```

### Connection Errors

If you get connection errors, ensure cline-core is running:

```bash
python3 -m cline_cli.main instance list
```

### Getting Help

For detailed usage information, see [USAGE.md](USAGE.md) or run:

```bash
python3 -m cline_cli.main --help
python3 -m cline_cli.main <command> --help
```
