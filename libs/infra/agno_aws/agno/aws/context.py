from __future__ import annotations

from pydantic import BaseModel


class AwsBuildContext(BaseModel):
    aws_region: str | None = None
    aws_profile: str | None = None
