"""Translation and Localization Utility Engine."""

import os
import json
import logging
from typing import Dict, Any, Optional, Union

logger = logging.getLogger("app.services.translation")

LOCALES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "app", "static", "locales")
DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES: Dict[str, str] = {
    "en": "English",
    "hi": "हिन्दी",
    "mr": "मराठी",
    "bn": "বাংলা",
    "gu": "गुजराती",
    "kn": "कन्नड",
    "ta": "தமிழ்",
    "te": "तेलुगु",
}

ASTROLOGY_TERMS: Dict[str, Dict[str, str]] = {
    "hi": {
        "Sun": "सूर्य", "Moon": "चंद्र", "Mars": "मंगल", "Mercury": "बुध",
        "Jupiter": "गुरु", "Venus": "शुक्र", "Saturn": "शनि", "Rahu": "राहु", "Ketu": "केतु",
        "Aries": "मेष", "Taurus": "वृषभ", "Gemini": "मिथुन", "Cancer": "कर्क",
        "Leo": "सिंह", "Virgo": "कन्या", "Libra": "तुला", "Scorpio": "वृश्चिक",
        "Sagittarius": "धनु", "Capricorn": "मकर", "Aquarius": "कुंभ", "Pisces": "मीन"
    },
    "mr": {
        "Sun": "सूर्य", "Moon": "चंद्र", "Mars": "मंगल", "Mercury": "बुध",
        "Jupiter": "गुरु", "Venus": "शुक्र", "Saturn": "शनि", "Rahu": "राहु", "Ketu": "केतु",
        "Aries": "मेष", "Taurus": "वृषभ"
    },
    "ta": {
        "Sun": "சூரியன்", "Moon": "சந்திரன்", "Mars": "செவ்வாய்", "Mercury": "புதன்",
        "Jupiter": "குரு", "Venus": "சுக்கிரன்", "Saturn": "சனி", "Rahu": "ராகு", "Ketu": "கேது",
        "Aries": "மேஷம்"
    },
    "te": {
        "Sun": "సూర్యుడు", "Moon": "చంద్రుడు", "Mars": "అంగారకుడు", "Mercury": "బుధుడు",
        "Jupiter": "గురుడు", "Venus": "శుక్రుడు", "Saturn": "శని", "Rahu": "రాహువు", "Ketu": "కేతువు"
    },
    "gu": {
        "Sun": "સૂર્ય", "Moon": "ચંદ્ર", "Aries": "મેષ", "Taurus": "વૃષભ"
    }
}


_translations_cache: Dict[str, Dict[str, Any]] = {}


def load_translations(lang: str) -> Dict[str, Any]:
    if lang in _translations_cache:
        return _translations_cache[lang]

    filepath = os.path.join(LOCALES_DIR, f"{lang}.json")
    if not os.path.exists(filepath):
        logger.warning(f"Locale file for '{lang}' not found at {filepath}, falling back to '{DEFAULT_LANGUAGE}'.")
        filepath = os.path.join(LOCALES_DIR, f"{DEFAULT_LANGUAGE}.json")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            _translations_cache[lang] = data
            return data
    except Exception as e:
        logger.error(f"Error loading translations for '{lang}': {e}")
        return {}


def translate(
    key: str,
    lang: str = DEFAULT_LANGUAGE,
    default_text: Optional[str] = None,
    default: Optional[str] = None
) -> str:
    fallback_text = default_text if default_text is not None else default
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE

    data = load_translations(lang)
    if key in data:
        return str(data[key])

    keys = key.split(".")
    val = data
    found = True
    for k in keys:
        if isinstance(val, dict) and k in val:
            val = val[k]
        else:
            found = False
            break

    if found and not isinstance(val, (dict, list)):
        return str(val)

    if lang != DEFAULT_LANGUAGE:
        return translate(key, lang=DEFAULT_LANGUAGE, default_text=fallback_text)

    return fallback_text if fallback_text is not None else key



get_translation = translate


def translate_astrology_term(term: str, lang: str = DEFAULT_LANGUAGE) -> str:
    if lang in ASTROLOGY_TERMS and term in ASTROLOGY_TERMS[lang]:
        return ASTROLOGY_TERMS[lang][term]
    return translate(f"astrology.{term}", lang=lang, default_text=term)

