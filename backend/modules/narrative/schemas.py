"""Pydantic Schemas for Narrative Module."""

from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class NarrativeRequest(BaseModel):
    year: int = Field(..., example=1990)
    month: int = Field(..., example=5)
    day: int = Field(..., example=15)
    hour: float = Field(..., example=14.5)
    city: str = Field("Pune", example="Pune")
    lang: str = Field("en", example="en")


class NarrativeResponse(BaseModel):
    chart: Dict[str, Any]
    marriage_prediction: str
    career_prediction: str
    raw_marriage_score: int
    raw_career_score: int


class ChatRequest(BaseModel):
    message: str
    chart: Optional[Dict[str, Any]] = None
    lang: str = "en"


class ChatResponse(BaseModel):
    reply: str
    topic: Optional[str] = "general"
    chart_context: Optional[Dict[str, Any]] = None


class NarrativeJobRequest(BaseModel):
    input_hash: str
    year: int
    month: int
    day: int
    hour: float
    city: str = "Pune"
    lang: str = "en"
    engine_version: str = "2.0.0"
    prompt_version: str = "1.0.0"


class NarrativeJobResult(BaseModel):
    marriage_prediction: Optional[str] = None
    career_prediction: Optional[str] = None
    raw_marriage_score: Optional[int] = None
    raw_career_score: Optional[int] = None
    chart: Optional[Dict[str, Any]] = None


class NarrativeJobStatus(BaseModel):
    job_id: str
    status: str  # queued, running, completed, failed
    input_hash: str
    language: str = "en"
    created_at: str
    result: Optional[NarrativeJobResult] = None
    error: Optional[str] = None

