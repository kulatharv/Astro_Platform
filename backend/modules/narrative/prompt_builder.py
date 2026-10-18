"""Token-optimized astrological prompt formatting utilities with multi-language (i18n) support."""

from shared.i18n.translation import SUPPORTED_LANGUAGES, translate_astrology_term


def build_prediction_prompt(chart: dict, prediction_type: str, lang: str = "en") -> str:
    """Build a controlled, short-format astrology prediction prompt localized per requested language."""
    prediction_data = chart.get(f"{prediction_type}_prediction", {})
    score = prediction_data.get("score", 75)
    level = prediction_data.get("level", "Moderate")
    reasons = prediction_data.get("reasons", [])

    short_reasons = reasons[:2]
    formatted_reasons = ", ".join(short_reasons) if short_reasons else "Planetary positions and Dasha activation"

    lang_name = SUPPORTED_LANGUAGES.get(lang.lower(), "English") if isinstance(SUPPORTED_LANGUAGES, dict) else "English"

    prompt = f"""
You are AstroAI, a precise and professional Vedic astrologer.

Generate a short astrology summary based on this chart calculation:
- Prediction Type: {prediction_type.capitalize()}
- Score: {score}/100
- Level: {level}
- Key Astrological Factors: {formatted_reasons}

Rules:
- Maximum 4-5 sentences.
- Mention score and level clearly.
- Highlight 1-2 key astrological factors.
- End with a constructive, actionable recommendation.
- Avoid fatalistic language.
- MANDATORY: Write your entire response strictly in {lang_name} (language code: {lang}).
"""
    return prompt.strip()


def build_chat_prompt(chart: dict, message: str, lang: str = "en") -> str:
    """Build a contextual prompt answering user life questions localized per requested language."""
    basic = chart.get("basic_details", {}) if isinstance(chart, dict) else {}
    lagna = translate_astrology_term(basic.get("lagna", "Aries"), lang)
    dasha = chart.get("dasha", {}).get("current_mahadasha", "Jupiter") if isinstance(chart, dict) else "Jupiter"
    yogas = chart.get("advanced_yogas", []) if isinstance(chart, dict) else []

    lang_name = SUPPORTED_LANGUAGES.get(lang.lower(), "English") if isinstance(SUPPORTED_LANGUAGES, dict) else "English"

    prompt = f"""
You are AstroAI, an expert Vedic astrologer.
Answer the user's question using their birth chart context:
- Lagna: {lagna}
- Current Mahadasha: {dasha}
- Active Yogas: {', '.join(yogas[:3]) if yogas else 'None'}

User Question: {message}

Instructions:
- Provide a clear, empowering, and accurate astrological interpretation.
- Reference house and planetary principles relevant to their question.
- Keep response under 120 words.
- MANDATORY: Write your entire response strictly in {lang_name} (language code: {lang}).
"""
    return prompt.strip()
