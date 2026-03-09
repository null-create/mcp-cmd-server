# MCP Shell Executor Server

A Model Context Protocol (MCP) server that provides safe shell command execution capabilities. This server allows executing a predefined set of safe shell commands while blocking potentially dangerous operations.

## Features

- **Safe Command Execution**: Only allows commands from a predefined allowlist to prevent security risks.
- **Timeout Support**: Configurable timeout for command execution.
- **Logging**: Comprehensive logging for monitoring and debugging.
- **Docker Support**: Easy deployment using Docker and Docker Compose.
- **FastMCP Integration**: Built on the FastMCP framework for MCP compliance.
- **Multiple Transport Modes**: Supports stdio, SSE, and streamable-http modes.

## Installation

### Prerequisites

- Python 3.12 or later
- pip

### Local Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd mcp-cmd-server
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   make init
   ```

   Or manually:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

## Configuration

The server can be configured using environment variables or a `.env` file:

- `MODE`: MCP transport mode (default: "streamable-http", options: "stdio", "sse", "streamable-http")
- `HOST_ADDR`: Host address to bind to (default: "0.0.0.0")
- `HOST_PORT`: Port to listen on (default: 9595)
- `LOG_LEVEL`: Logging level as integer (default: 10, DEBUG)

## Usage

### Running Locally

Activate the virtual environment and run the server:

```bash
source venv/bin/activate
python main.py --mode streamable-http
```

The server will start on the configured host and port.

### Transport Modes

- `stdio`: Standard input/output mode for local MCP clients
- `sse`: Server-Sent Events mode for web-based clients
- `streamable-http`: HTTP streaming mode (default)

### Using the Tool

The server exposes a `run_command` tool that accepts:

- `command`: The shell command to execute (must start with an allowed base command)
- `timeout`: Maximum execution time in seconds (default: 30)

Example response:
```json
{
  "stdout": "output here",
  "stderr": "",
  "returncode": 0
}
```

## Docker Deployment

### Using Docker Compose

1. Build and start the container:
   ```bash
   make run
   ```

   Or manually:
   ```bash
   docker-compose up -d --build
   ```

2. Stop the container:
   ```bash
   make stop
   ```

   Or manually:
   ```bash
   docker-compose down
   ```

The server will be available on port 9595.

## Allowed Commands

The server only executes commands whose base (first token) is in the allowlist. The current allowed commands include:

- Filesystem navigation & inspection: `ls`, `cat`, `head`, `tail`, `pwd`, `find`, `du`, `df`, `stat`, `file`, `wc`
- Text processing: `grep`, `awk`, `sed`, `sort`, `uniq`, `cut`, `tr`, `diff`
- System information: `echo`, `date`, `uptime`, `whoami`, `uname`, `ps`, `env`, `which`, `lsof`

To modify the allowlist, edit `tools/cmd.py`.

## Dependencies

- `mcp>=1.0.0`
- `pydantic~=2.12.5`

## Security

This server is designed with security in mind:

- Commands are validated against an allowlist before execution.
- No arbitrary code execution is allowed.
- Logging helps track all command executions.
- Timeout prevents runaway processes.

## License

MIT