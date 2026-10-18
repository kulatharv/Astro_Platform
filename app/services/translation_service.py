"""Localization and astrology terminology translation service."""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SUPPORTED_LANGUAGES = {
    "en": "English",
    "hi": "हिन्दी",
    "mr": "मराठी",
    "gu": "ગુજરાતી",
    "ta": "தமிழ்",
    "te": "తెలుగు",
    "kn": "ಕನ್ನಡ",
    "bn": "বাংলা",
}

ASTROLOGY_TERMS: dict[str, dict[str, str]] = {
    # Planets
    "Sun": {"hi": "सूर्य", "mr": "सूर्य", "gu": "સૂર્ય", "ta": "சூரியன்", "te": "సూర్యుడు", "kn": "ಸೂರ್ಯ", "bn": "সূর্য"},
    "Moon": {"hi": "चन्द्र", "mr": "चंद्र", "gu": "ચંદ્ર", "ta": "சந்திரன்", "te": "చంద్రుడు", "kn": "ಚಂದ್ರ", "bn": "চন্দ্র"},
    "Mars": {"hi": "मंगल", "mr": "मंगल", "gu": "મંગળ", "ta": "செவ்வாய்", "te": "అంగారకుడు", "kn": "ಮಂಗಳ", "bn": "মঙ্গল"},
    "Mercury": {"hi": "बुध", "mr": "बुध", "gu": "બુધ", "ta": "புதன்", "te": "బుధుడు", "kn": "ಬುಧ", "bn": "বুধ"},
    "Jupiter": {"hi": "गुरु", "mr": "गुरु", "gu": "ગુરુ", "ta": "குரு", "te": "గురుడు", "kn": "ಗುರು", "bn": "বৃহস্পতি"},
    "Venus": {"hi": "शुक्र", "mr": "शुक्र", "gu": "શુક્ર", "ta": "சுக்கிரன்", "te": "శుక్రుడు", "kn": "శుక్ర", "bn": "শুক্রবার"},
    "Saturn": {"hi": "शनि", "mr": "शनि", "gu": "શનિ", "ta": "சனி", "te": "శని", "kn": "ಶನಿ", "bn": "শনি"},
    "Rahu": {"hi": "राहु", "mr": "राहु", "gu": "રાહુ", "ta": "ராகு", "te": "రాహువు", "kn": "ರಾಹು", "bn": "রাহু"},
    "Ketu": {"hi": "केतु", "mr": "કેતુ", "gu": "કેતુ", "ta": "கேது", "te": "కేతువు", "kn": "కేతు", "bn": "কেতু"},
    "Lagna": {"hi": "लग्न", "mr": "लग्न", "gu": "લગ્ન", "ta": "லக்னம்", "te": "లగ్నం", "kn": "ಲಗ್ನ", "bn": "লগ্ন"},

    # Zodiac Signs
    "Aries": {"hi": "मेष", "mr": "मेष", "gu": "મેષ", "ta": "மேஷம்", "te": "మేషం", "kn": "ಮೇಷ", "bn": "মেষ"},
    "Taurus": {"hi": "वृषभ", "mr": "वृषभ", "gu": "વૃષભ", "ta": "ரிஷபம்", "te": "వృషభం", "kn": "ವೃಷಭ", "bn": "বৃষ"},
    "Gemini": {"hi": "मिथुन", "mr": "मिथुन", "gu": "મિથુન", "ta": "மிதுனம்", "te": "మిథునం", "kn": "ಮಿಥುನ", "bn": "মিথুন"},
    "Cancer": {"hi": "कर्क", "mr": "कर्क", "gu": "કર્ક", "ta": "கடகம்", "te": "కర్కాటకం", "kn": "ಕರ್ಕಾಟಕ", "bn": "কর্কট"},
    "Leo": {"hi": "सिंह", "mr": "सिंह", "gu": "સિંહ", "ta": "சிம்மம்", "te": "సింహం", "kn": "ಸಿಂಹ", "bn": "সিংহ"},
    "Virgo": {"hi": "कन्या", "mr": "कन्या", "gu": "કન્યા", "ta": "கன்னி", "te": "కన్య", "kn": "ಕನ್ಯಾ", "bn": "কন্যা"},
    "Libra": {"hi": "तुला", "mr": "तुला", "gu": "તુલા", "ta": "துலாம்", "te": "తులా", "kn": "ತುಲಾ", "bn": "তুলা"},
    "Scorpio": {"hi": "वृश्चिक", "mr": "वृश्चिक", "gu": "વૃશ્ચિક", "ta": "விருச்சிகம்", "te": "వృశ్చિકం", "kn": "ವೃಶ್ಚಿಕ", "bn": "বৃশ্চিক"},
    "Sagittarius": {"hi": "धनु", "mr": "धनु", "gu": "ધનુ", "ta": "தனுசு", "te": "ధనుస్సు", "kn": "ಧನುಸ್ಸು", "bn": "ধনু"},
    "Capricorn": {"hi": "मकर", "mr": "मकर", "gu": "મકર", "ta": "மகரம்", "te": "మకరం", "kn": "ಮಕರ", "bn": "মকর"},
    "Aquarius": {"hi": "कुंभ", "mr": "कुंभ", "gu": "કુંભ", "ta": "கும்பம்", "te": "కుంభం", "kn": "ಕುಂಭ", "bn": "কুম্ভ"},
    "Pisces": {"hi": "मीन", "mr": "मीन", "gu": "મીન", "ta": "மீனம்", "te": "మీనం", "kn": "ಮೀನ", "bn": "মীন"},

    # Core Concepts
    "Tithi": {"hi": "तिथि", "mr": "तिथी", "gu": "તિથિ", "ta": "திதி", "te": "తిథి", "kn": "ತಿಥಿ", "bn": "তিথি"},
    "Nakshatra": {"hi": "नक्षत्र", "mr": "नक्षत्र", "gu": "નક્ષત્ર", "ta": "நட்சத்திரம்", "te": "నక్షత్రం", "kn": "ನಕ್ಷತ್ರ", "bn": "নক্ষত্র"},
    "Yoga": {"hi": "योग", "mr": "योग", "gu": "યોગ", "ta": "யோகம்", "te": "యోగం", "kn": "ಯೋಗ", "bn": "যোগ"},
    "Karana": {"hi": "करण", "mr": "करण", "gu": "કરણ", "ta": "கரணம்", "te": "కరణం", "kn": "ಕರಣ", "bn": "করণ"},
}


def load_translations(lang: str = "en") -> dict:
    """Load JSON translation locale file with fallback chain to English."""
    lang_code = lang.lower().split("-")[0] if lang else "en"
    if lang_code not in SUPPORTED_LANGUAGES:
        lang_code = "en"

    file_path = BASE_DIR / "static" / "locales" / f"{lang_code}.json"

    if file_path.exists():
        try:
            with open(file_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    # Fallback to English
    fallback_path = BASE_DIR / "static" / "locales" / "en.json"
    if fallback_path.exists():
        try:
            with open(fallback_path, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass

    return {}


def get_translation(key: str, lang: str = "en", default: str | None = None) -> str:
    """Retrieve translated string by key with strict fallback chain."""
    translations = load_translations(lang)
    if key in translations:
        return translations[key]

    en_translations = load_translations("en")
    if key in en_translations:
        return en_translations[key]

    return default if default is not None else key


def translate_astrology_term(term: str, lang: str = "en") -> str:
    """Translate planet, sign, or astrology concept into target language."""
    lang_code = lang.lower().split("-")[0] if lang else "en"
    if lang_code == "en" or lang_code not in SUPPORTED_LANGUAGES:
        return term

    mapping = ASTROLOGY_TERMS.get(term)
    if mapping and lang_code in mapping:
        return mapping[lang_code]

    return term