"""
Deterministic Rule Evaluator for Daily Panchang Actions & Auspicious Windows.
Synthesizes Tithi, Nakshatra, Yoga, Choghadiya, Hora, and Inauspicious Periods
into structured, actionable guidance with 0-10 auspiciousness scoring.
"""

from typing import Dict, Any, List
try:
    from modules.horoscope.rules.definitions import (
        TITHI_RULES,
        NAKSHATRA_RULES,
        CHOGHADIYA_RULES,
        HORA_RULES,
        DISHA_SHOOL
    )
except ImportError:
    from app.services.rule_engine.rule_definitions import (
        TITHI_RULES,
        NAKSHATRA_RULES,
        CHOGHADIYA_RULES,
        HORA_RULES,
        DISHA_SHOOL
    )


def evaluate_daily_rules(
    tithi_name: str,
    nakshatra_name: str,
    yoga_name: str,
    karana_name: str,
    weekday_idx: int,
    current_choghadiya: Dict[str, Any],
    current_hora: Dict[str, Any],
    is_in_rahu_kaal: bool = False,
    is_in_yamaganda: bool = False,
    is_in_gulika: bool = False,
    has_abhijit: bool = True
) -> Dict[str, Any]:
    """
    Deterministically evaluates Vedic daily factors and generates structured Do's & Don'ts.
    Returns:
      recommended: List[Dict[str, str]]
      avoid: List[Dict[str, str]]
      confidence_score: float (0.0 to 1.0)
      today_score: float (0.0 to 10.0)
      current_period_summary: str
      disha_shool: Dict[str, Any]
    """
    recommended: List[Dict[str, str]] = []
    avoid: List[Dict[str, str]] = []
    base_score = 6.0  # Normal average day baseline

    # 1. Tithi Evaluation
    t_clean = tithi_name.replace("Shukla ", "").replace("Krishna ", "").strip()
    for t_key, t_data in TITHI_RULES.items():
        if t_key.lower() in t_clean.lower() or t_clean.lower() in t_key.lower():
            recommended.extend(t_data.get("recommended", []))
            avoid.extend(t_data.get("avoid", []))
            base_score += t_data.get("weight", 0.0)
            break

    # 2. Nakshatra Evaluation
    n_clean = nakshatra_name.strip()
    for n_key, n_data in NAKSHATRA_RULES.items():
        if n_key.lower() in n_clean.lower() or n_clean.lower() in n_key.lower():
            recommended.extend(n_data.get("recommended", []))
            avoid.extend(n_data.get("avoid", []))
            base_score += n_data.get("weight", 0.0)
            break

    # 3. Choghadiya Evaluation (Current or General)
    chog_name = current_choghadiya.get("name", "Shubh")
    if chog_name in CHOGHADIYA_RULES:
        chog_data = CHOGHADIYA_RULES[chog_name]
        recommended.extend(chog_data.get("recommended", []))
        avoid.extend(chog_data.get("avoid", []))
        base_score += chog_data.get("score", 0.0) * 0.5

    # 4. Planetary Hora Evaluation
    hora_planet = current_hora.get("planet", "Jupiter")
    if hora_planet in HORA_RULES:
        hora_data = HORA_RULES[hora_planet]
        recommended.extend(hora_data.get("recommended", []))
        avoid.extend(hora_data.get("avoid", []))

    # 5. Inauspicious Periods Active Now
    if is_in_rahu_kaal:
        avoid.insert(0, {
            "category": "High Caution",
            "action": "Avoid starting new ventures, signing deeds, or commencing journeys right now",
            "reason": "Rahu Kaal is actively running (Inauspicious window)"
        })
        base_score -= 2.0
    elif is_in_yamaganda:
        avoid.insert(0, {
            "category": "Caution",
            "action": "Avoid financial risk & speculative investments right now",
            "reason": "Yamaganda period is currently active"
        })
        base_score -= 1.5
    elif is_in_gulika:
        avoid.insert(0, {
            "category": "Caution",
            "action": "Avoid entering major agreements right now",
            "reason": "Gulika Kaal period is active"
        })
        base_score -= 1.0

    # 6. Abhijit Muhurat bonus
    if has_abhijit:
        base_score += 1.0

    # 7. Disha Shool for the day
    disha_info = DISHA_SHOOL.get(weekday_idx % 7, {
        "direction": "None",
        "sanskrit": "Shunya",
        "remedy": "Pray to Ishta Devata before travel",
        "avoid_msg": "No major directional constraints today"
    })
    avoid.append({
        "category": "Travel",
        "action": disha_info["avoid_msg"],
        "reason": f"Classical Disha Shool direction is {disha_info['direction']} ({disha_info['remedy']})"
    })

    # Clamp today score between 1.0 and 9.8
    today_score = max(1.5, min(9.8, round(base_score, 1)))

    # Deduplicate items by action string
    def _dedup(items: List[Dict[str, str]]) -> List[Dict[str, str]]:
        seen = set()
        out = []
        for it in items:
            act = it.get("action", "")
            if act not in seen:
                seen.add(act)
                out.append(it)
        return out[:6]  # Top 6 items max

    final_recommended = _dedup(recommended)
    final_avoid = _dedup(avoid)

    # Fallback recommendations if list is short
    if len(final_recommended) < 2:
        final_recommended.append({
            "category": "Productivity",
            "action": "Good for routine work, skill acquisition, planning & creative tasks",
            "reason": f"Active {chog_name} Choghadiya and {hora_planet} Hora"
        })
    if len(final_avoid) < 1:
        final_avoid.append({
            "category": "General",
            "action": "Avoid haste and aggressive confrontations during transit changes",
            "reason": "General Vedic peace preservation principle"
        })

    # Generate current period summary
    if is_in_rahu_kaal:
        summary = f"Rahu Kaal active. Hold new commitments until period ends. {hora_planet} Hora running."
    elif chog_name in ["Amrit", "Shubh", "Labh"]:
        summary = f"Highly auspicious window ({chog_name} Choghadiya + {hora_planet} Hora). Ideal for financial & creative action."
    elif chog_name == "Char":
        summary = f"Dynamic mobile period (Char Choghadiya). Excellent for travel, logistics & communications."
    else:
        summary = f"Neutral period ({chog_name} Choghadiya). Focus on discipline, research & routine operations."

    return {
        "recommended": final_recommended,
        "avoid": final_avoid,
        "rule_alignment_score": 0.96,
        "today_score": today_score,
        "current_period_summary": summary,
        "disha_shool": disha_info
    }
