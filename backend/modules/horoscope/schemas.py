"""Horoscope response and request schemas."""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional


class HoroscopeRequest(BaseModel):
    sign: str = Field(..., description="Zodiac sign name (e.g. aries, taurus, mesha)")
    period: str = Field("daily", description="daily, weekly, or monthly")
    language: str = Field("en", description="Language code")


class HoroscopeResponse(BaseModel):
    sign: str
    period: str
    language: str
    prediction: str
    score: int
    aspects: Dict[str, Any]
    lucky_number: int
    lucky_color: str
