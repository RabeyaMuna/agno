from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class AgentSessionCreate(BaseModel):
    """Data sent to API to create an Agent Session"""

    session_id: str
    agent_data: dict[str, Any] | None = None


class AgentRunCreate(BaseModel):
    """Data sent to API to create an Agent Run"""

    session_id: str
    team_session_id: str | None = None
    run_id: str | None = None
    run_data: dict[str, Any] | None = None
    agent_data: dict[str, Any] | None = None
