import os

from pydantic import BaseModel, Field


class Config(BaseModel):
    mode: str = Field(..., env=os.getenv("MODE", "streamable-http"))
    host_addr: str = Field(..., env=os.getenv("HOST_ADDR", "0.0.0.0"))
    host_port: int = Field(..., env=os.getenv("HOST_PORT", 9595))
    log_level: int = Field(..., env=os.getenv("LOG_LEVEL", 10))
