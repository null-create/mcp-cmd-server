import json
import logging
import subprocess

from mcp.server.fastmcp import FastMCP

from config import Config
from commands import ALLOWED_COMMANDS

# Global configs
config = Config()

logger = logging.getLogger(__file__)
logging.basicConfig(level=config.log_level, format="%(asctime)s - %(levelname)s - %(message)s")

mcp = FastMCP(name="shell-executor", host=config.host_addr, port=config.host_port, debug=True)


def check_command_safety(command: str) -> tuple[bool, str]:
    """
    Returns (is_safe, reason).
    Blocks the command if its base (first token) is not in ALLOWED_COMMANDS.
    """
    tokens = command.strip().split()
    if not tokens:
        return False, "Empty command."

    base = tokens[0]
    if base not in ALLOWED_COMMANDS:
        allowed = ", ".join(sorted(ALLOWED_COMMANDS))
        logger.warning(f"Blocked command: '{command}'. Reason: base '{base}' not in allowlist.")
        return False, (
            f"'{base}' is not in the list of allowed commands. "
            f"Permitted commands are: {allowed}"
        )

    return True, ""


@mcp.tool(name="run_command",
          description="Execute a shell command and return its output. Only commands whose base (first token) appear in "
                      "the server's allowlist will be executed. Everything else is rejected before any subprocess is "
                      "spawned.")
def run_command(command: str, timeout: int = 30) -> dict:
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
    is_safe, reason = check_command_safety(command)
    if not is_safe:
        return {
            "stdout": "",
            "stderr": f"Blocked: {reason}",
            "returncode": -1,
        }

    logger.info("Executing command: '%s'", command)
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        logger.info("Command executed. Return code: %d", result.returncode)
        response = {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
        }
        logger.info("Command output: %s", json.dumps(response, indent=2))
        return response
    except subprocess.TimeoutExpired:
        logger.error("Command '%s' timed out after %d seconds.", command, timeout)
        return {
            "stdout": "",
            "stderr": f"Command timed out after {timeout} seconds.",
            "returncode": -1,
        }
    except Exception as e:
        logger.error("Error executing command '%s': %s", command, str(e))
        return {
            "stdout": "",
            "stderr": str(e),
            "returncode": -1,
        }


if __name__ == "__main__":
    try:
        mcp.run(transport="streamable-http")
    except KeyboardInterrupt as e:
        logger.info("Shutting down server.")
