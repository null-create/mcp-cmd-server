import json
import logging
import subprocess

from .cmd import ALLOWED_COMMANDS
from .models import CommandRequest, CommandResponse


logger = logging.getLogger(__file__)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


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
        logger.warning(
            f"Blocked command: '{command}'. Reason: base '{base}' not in allowlist."
        )
        return False, (
            f"'{base}' is not in the list of allowed commands. "
            f"Permitted commands are: {allowed}"
        )

    return True, ""


def run_command(command: CommandRequest) -> CommandResponse:
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
    is_safe, reason = check_command_safety(command.command)
    if not is_safe:
        return CommandResponse(stdout="", stderr=f"Blocked: {reason}", returncode=-1)

    logger.info("Executing command: '%s'", command.command)
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=command.timeout,
        )
        logger.info("Command executed. Return code: %d", result.returncode)
        response = CommandResponse(
            stdout=result.stdout, stderr=result.stderr, returncode=result.returncode
        )
        logger.info("Command output: %s", json.dumps(response.model_dump()), indent=2)
        return response
    except subprocess.TimeoutExpired:
        logger.error("Command '%s' timed out after %d seconds.", command, timeout)
        return CommandResponse(
            stdout="",
            stderr=f"Command timed out after {command.timeout} seconds.",
            returncode=-1,
        )
    except Exception as e:
        logger.error("Error executing command '%s': %s", command, str(e))
        return CommandResponse(
            stdout="", stderr=f"Error executing command: {str(e)}", returncode=-1
        )
