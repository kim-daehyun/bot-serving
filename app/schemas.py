from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


class FePredictRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str = Field(..., description="Session identifier")
    duration_ms: float = Field(..., ge=0, description="Stage/session duration in ms")
    mouse_teleport_rate: float = Field(..., ge=0, description="Mouse teleport rate")
    mousemove_count: float = Field(..., ge=0, description="Mousemove count")

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
    ts_payment_ready: float = Field(..., ge=0, description="Payment-ready to terminal time")
    ts_whole_session: float = Field(..., ge=0, description="Whole session time from login to confirm")
    req_interval_cv_pre_hold: float = Field(..., ge=0, description="Request interval CV before first hold")
    req_interval_cv_hold_gap: float = Field(..., ge=0, description="Absolute CV gap between post-hold and pre-hold")

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