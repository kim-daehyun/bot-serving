from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


class FePredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(..., description="Session identifier")

    duration_ms: float = Field(..., ge=0, description="Stage/session duration in ms")
    mouse_activity_rate: float = Field(..., ge=0, description="Mouse activity rate")
    mouse_teleport_rate: float = Field(..., ge=0, description="Mouse teleport rate")

    @field_validator("session_id")
    @classmethod
    def validate_session_id(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("session_id must not be empty")
        return value


class BePredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(..., description="Session identifier")

    endpoint_burst_max_1s: float = Field(..., ge=0, description="Max burst in 1 second")
    req_interval_cv: float = Field(..., ge=0, description="Coefficient of variation of request interval")
    target_retry_count: float = Field(..., ge=0, description="Retry count for same target")
    payment_ready_to_terminal_ms: float = Field(..., ge=0, description="Time from payment_ready to terminal state")

    @field_validator("session_id")
    @classmethod
    def validate_session_id(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("session_id must not be empty")
        return value


class PredictResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str
    model_type: Literal["fe", "be"]
    label: Literal["human", "bot"]
    bot_score: float = Field(..., ge=0.0, le=1.0)
    threshold: float = Field(..., ge=0.0, le=1.0)
    model_name: Optional[str] = None


class HealthResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["ok", "error"]
    fe_loaded: bool
    be_loaded: bool
    fe_model_path: str
    be_model_path: str