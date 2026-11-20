from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from time import time
from typing import Any

from agno.media import AudioResponse, ImageArtifact
from agno.models.message import Citations, MessageMetrics


class ModelResponseEvent(str, Enum):
    """Events that can be sent by the model provider"""

    tool_call_confirmation_required = "ToolCallConfirmationRequired"
    tool_call_external_execution_required = "ToolCallExternalExecutionRequired"
    tool_call_started = "ToolCallStarted"
    tool_call_completed = "ToolCallCompleted"
    assistant_response = "AssistantResponse"


@dataclass
class ToolExecution:
    """Execution of a tool"""

    tool_call_id: str | None = None
    tool_name: str | None = None
    tool_args: dict[str, Any] | None = None
    tool_call_error: bool | None = None
    result: str | None = None
    metrics: MessageMetrics | None = None

    # If True, the agent will stop executing after this tool call.
    stop_after_tool_call: bool = False

    created_at: int = int(time())

    requires_confirmation: bool | None = None
    confirmed: bool | None = None

    external_execution_required: bool | None = None


@dataclass
class ModelResponse:
    """Response from the model provider"""

    role: str | None = None

    content: str | None = None
    parsed: Any | None = None
    audio: AudioResponse | None = None
    image: ImageArtifact | None = None

    # Model tool calls
    tool_calls: list[dict[str, Any]] = field(default_factory=list)

    # Actual tool executions
    tool_executions: list[ToolExecution] | None = field(default_factory=list)

    event: str = ModelResponseEvent.assistant_response.value

    provider_data: dict[str, Any] | None = None

    thinking: str | None = None
    redacted_thinking: str | None = None
    reasoning_content: str | None = None

    citations: Citations | None = None

    response_usage: Any | None = None

    created_at: int = int(time())

    extra: dict[str, Any] | None = None


class FileType(str, Enum):
    MP4 = "mp4"
    GIF = "gif"
    MP3 = "mp3"
