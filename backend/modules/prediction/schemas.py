"""Pydantic Schemas for Prediction & Life Domain Module."""

from datetime import date
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: float = Field(..., ge=0, lt=24)
    city: Optional[str] = "Pune"


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


class DomainRequest(BaseModel):
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)
    city: str = Field(..., min_length=1)


class TimingWindow(BaseModel):
    start_date: date
    end_date: date
    peak_date: date
    peak_score: float
    confidence: str
    mahadasha: str
    antardasha: str
    pratyantardasha: str
    reasons: list[str]
    drivers: list[str]
    sub_scores: dict


class TimingBlock(BaseModel):
    timing_windows: list[TimingWindow]
    peak_window: Optional[TimingWindow]
    next_12_months_summary: str
    methodology: str
    engine_version: str


class PredictionResponse(BaseModel):
    engine_version: str
    input_hash: str
    lagna: str
    mahadasha: str
    antardasha: str
    yogas_detected: list
    domains: Dict[str, Any]
    disclaimer: Optional[str] = None
