"""AI Prediction Orchestrator for Marriage, Career, and Life Domains."""

from modules.kundali.varga import generate_full_chart
from modules.kundali.cities import get_city

from modules.narrative.llm_client import ask_llm
from modules.narrative.prompt_builder import build_prediction_prompt


class NarrativeEngine:
    @staticmethod
    def generate_predictions(
        year: int, month: int, day: int, hour: float, city: str = "Pune", lang: str = "en"
    ) -> dict:
        """Generate full natal chart and synthesize localized AI marriage & career predictions."""
        coords = get_city(city)
        if coords is None:
            lat, lon = 18.5204, 73.8567
        else:
            lat, lon, _ = coords

        chart = generate_full_chart(year, month, day, hour, lat, lon)

        marriage_prompt = build_prediction_prompt(chart, "marriage", lang=lang)
        career_prompt = build_prediction_prompt(chart, "career", lang=lang)

        marriage_output = ask_llm(marriage_prompt)
        career_output = ask_llm(career_prompt)

        return {
            "chart": chart,
            "marriage_prediction": marriage_output,
            "career_prediction": career_output,
            "raw_marriage_score": chart.get("marriage_prediction", {}).get("score", 75),
            "raw_career_score": chart.get("career_prediction", {}).get("score", 78),
        }


prediction_service = NarrativeEngine()
