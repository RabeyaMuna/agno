from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class TeamSessionCreate(BaseModel):
    """Data sent to API to create an Team Session"""

    session_id: str
    team_data: dict[str, Any] | None = None


class TeamRunCreate(BaseModel):
    """Data sent to API to create an Team Run"""

    session_id: str
    team_session_id: str | None = None
    run_id: str | None = None
    run_data: dict[str, Any] | None = None
    team_data: dict[str, Any] | None = None
