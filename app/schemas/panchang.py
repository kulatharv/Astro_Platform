from pydantic import BaseModel, Field


class PanchangRequest(BaseModel):
    city: str = Field(..., min_length=1)
    date_str: str | None = None  # Format YYYY-MM-DD optional


class PanchangResponse(BaseModel):
    date: str | None = None
    city: str
    tithi: str | None = None
    nakshatra: str | None = None
    yoga: str | None = None
    karana: str | None = None
    vara: str | None = None
    sunrise: str | None = None
    sunset: str | None = None
    rahu_kaal: str | None = None
    gulika_kaal: str | None = None
    yamaganda: str | None = None
    abhijit_muhurta: str | None = None
