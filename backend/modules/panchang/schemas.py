from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class PanchangRequest(BaseModel):
    model_config = ConfigDict(extra="allow")

    city: Optional[str] = Field(default="Pune")
    date_str: Optional[str] = None  # Format YYYY-MM-DD
    lat: Optional[float] = None
    lon: Optional[float] = None
    timezone: Optional[str] = None
    user_rashi: Optional[str] = None
    user_nakshatra: Optional[str] = None


class ProfileResolveRequest(BaseModel):
    """Resolve natal Moon sign (Rashi) and Nakshatra from birth details."""
    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    birth_date: str  # YYYY-MM-DD
    birth_time: Optional[str] = None  # HH:MM (24h)
    birth_place: Optional[str] = Field(default="Pune")
    lat: Optional[float] = None
    lon: Optional[float] = None


class DecisionRequest(BaseModel):
    """Interactive Decision Assistant request."""
    model_config = ConfigDict(extra="allow")

    activity: str = Field(..., description="Activity type: travel, investment, meeting, spiritual, purchase")
    city: Optional[str] = Field(default="Pune")
    user_rashi: Optional[str] = None
    user_nakshatra: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None


class PanchangResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    date_str: Optional[str] = None
    city: str
    lat: Optional[float] = None
    lon: Optional[float] = None
    resolved_timezone: Optional[str] = "Asia/Kolkata"
    local_datetime: Optional[str] = None
    mode: Optional[str] = "general"  # "general" | "personalized"

    tithi: Optional[str] = None
    tithi_name: Optional[str] = None
    paksha: Optional[str] = None
    tithi_progress: Optional[float] = None
    tithi_end: Optional[str] = None

    nakshatra: Optional[str] = None
    nakshatra_pada: Optional[int] = None
    nakshatra_end: Optional[str] = None

    yoga: Optional[str] = None
    yoga_name: Optional[str] = None
    yoga_end: Optional[str] = None

    karana: Optional[str] = None
    karana_name: Optional[str] = None
    karana_end: Optional[str] = None

    sunrise: Optional[str] = None
    sunset: Optional[str] = None

    rahu: Optional[str] = None
    yamaganda: Optional[str] = None
    gulika: Optional[str] = None
    abhijit: Optional[str] = None
    brahma: Optional[str] = None

    today_score: Optional[float] = None
    rule_alignment_score: Optional[float] = None
    confidence_score: Optional[float] = None
    current_period_summary: Optional[str] = None
    next_auspicious_window: Optional[Dict[str, Any]] = None

    choghadiya_day: Optional[List[Dict[str, Any]]] = None
    choghadiya_night: Optional[List[Dict[str, Any]]] = None
    current_choghadiya: Optional[Dict[str, Any]] = None

    horas: Optional[List[Dict[str, Any]]] = None
    current_hora: Optional[Dict[str, Any]] = None

    disha_shool: Optional[Dict[str, Any]] = None
    dos_and_donts: Optional[Dict[str, Any]] = None
    planets: Optional[List[Dict[str, Any]]] = None
    samvat: Optional[Dict[str, Any]] = None

    # ── Personalization Layer ──
    personalization: Optional[Dict[str, Any]] = None
