from typing import Any
from pydantic import BaseModel, Field


class BirthData(BaseModel):
    name: str = "Seeker"
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: float = Field(..., ge=0, lt=24)
    place: str = "Unknown"


class KundaliRequest(BaseModel):
    year: int = Field(..., ge=1900, le=2100)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)
    city: str = Field(..., min_length=1)


class KundaliChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    chart: dict[str, Any]


class PlanetDetail(BaseModel):
    name: str
    sign: str
    degree: str
    degree_decimal: float
    house: int
    nakshatra: str
    pada: int
    navamsa: str
    strength: str
    retrograde: bool


class KundaliResponse(BaseModel):
    lagna: str
    lagna_degree: str
    lagna_degree_decimal: float
    lagna_nakshatra: str
    lagna_pada: int
    houses: dict[int, list[str]]
    d9_houses: dict[int, list[str]]
    d9_lagna: str
    planets: list[PlanetDetail]
    tithi_number: int
    tithi_name: str
    paksha: str
    nakshatra: str
    nakshatra_pada: int
    yoga_name: str
    karana_name: str
    ayanamsa: float
    jd: float
    mahadasha: str
    dasha_balance: str
    antardasha: str
    antardasha_list: list[dict[str, Any]]
    scores: dict[str, int]
    yogas: list[dict[str, Any]]
    doshas: list[dict[str, Any]]
