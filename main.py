import logging

from mcp.server.fastmcp import FastMCP

from config import Config
from tools.exec import run_command
from tools.models import CommandRequest, CommandResponse

# Global configs
config = Config()

logger = logging.getLogger(__file__)
logging.basicConfig(
    level=config.log_level, format="%(asctime)s - %(levelname)s - %(message)s"
)

mcp = FastMCP(
    name="shell-executor", host=config.host_addr, port=config.host_port, debug=True
)


@mcp.tool(
    name="run_command",
    description="Execute a shell command and return its output. Only commands whose base (first token) appear in "
    "the server's allowlist will be executed. Everything else is rejected before any subprocess is "
    "spawned.",
)
def run_command_tool(command: str, timeout: int = 30) -> dict:
    """
    Execute a shell command and return its output.

    Only commands whose base (first token) appear in the server's allowlist
    will be executed. Everything else is rejected before any subprocess is spawned.

    Args:
        command: The shell command to execute.
        timeout: Maximum time in seconds to wait for the command (default: 30).

    Returns:
        A dict with keys: stdout, stderr, returncode.
        If the command is blocked, returncode will be -1 and stderr will explain why.
    """
    try:
        cmd = CommandRequest(command=command, timeout=timeout)
        run_command_result = run_command(cmd)
        return run_command_result.model_dump()
    except Exception as e:
        logger.error(f"Error executing command '{command}': {e}")
        return CommandResponse(
            stdout="", stderr=f"Error executing command: {str(e)}", returncode=-1
        ).model_dump()


if __name__ == "__main__":
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt as e:
        logger.info("Shutting down server.")
