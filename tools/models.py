from pydantic import BaseModel


class CommandRequest(BaseModel):
    command: str
    timeout: int = 30  # Default timeout of 30 seconds


class CommandResponse(BaseModel):
    stdout: str
    stderr: str
    returncode: int
