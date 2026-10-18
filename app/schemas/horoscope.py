from typing import Any
from pydantic import BaseModel


class HoroscopeResponse(BaseModel):
    sign: str
    date: str | None = None
    horoscope: str | None = None
    scores: dict[str, int] | None = None
    lucky_number: int | None = None
    lucky_color: str | None = None
    mantra: str | None = None
    tip: str | None = None
    compatible_signs: list[str] | None = None


class FestivalItem(BaseModel):
    name: str
    date: str
    tithi: str | None = None
    description: str | None = None
    significance: str | None = None


class FestivalListResponse(BaseModel):
    festivals: list[dict[str, Any]]
