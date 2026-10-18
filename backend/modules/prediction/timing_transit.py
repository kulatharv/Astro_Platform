"""Gochara Transit activation scoring engine for domain timing (Step 5.5)."""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Dict, Any, List, Optional
import functools

import swisseph as swe

from shared.veda.zodiac import degree_to_sign, SIGNS, SIGN_LORDS
from modules.kundali.houses import assign_house
from modules.prediction.timing_config import get_domain_timing_config
from modules.prediction.transit_forecast import is_sade_sati_active, compute_transit_aspects
from shared.cache.keys import compute_input_hash


@dataclass
class ScoredMonth:
    month_start: date
    month_end: date
    score: float           # 0.0 to 1.0
    reasons: List[str]
    active_transits: dict  # planet -> {sign, house, aspect_houses}
    sub_scores: dict       # {jupiter, saturn, nodes, sade_sati}


def _get_planet_sign_house_at_date(dt: date, planet: str, lagna: str) -> tuple[str, int, List[int]]:
    """Compute exact sidereal sign, house from Lagna, and aspected houses for a planet at a date."""
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL

    planet_codes = {
        "Jupiter": swe.JUPITER,
        "Saturn": swe.SATURN,
        "Rahu": swe.TRUE_NODE,
        "Ketu": swe.TRUE_NODE,
    }

    code = planet_codes.get(planet, swe.JUPITER)
    jd = swe.julday(dt.year, dt.month, dt.day, 12.0)

    raw_pos = swe.calc_ut(jd, code, flags)[0][0]
    if planet == "Ketu":
        raw_pos = (raw_pos + 180.0) % 360.0
    else:
        raw_pos = raw_pos % 360.0

    sign, _ = degree_to_sign(raw_pos)
    house = assign_house(sign, lagna)
    aspects = compute_transit_aspects(planet, house)

    return sign, house, aspects


def score_transit_months(
    chart: dict,
    domain: str,
    start_date: date,
    end_date: date,
) -> List[ScoredMonth]:
    """Score monthly Gochara transit snapshots for a domain over a date range."""
    config = get_domain_timing_config(domain)
    lagna = chart.get("basic_details", {}).get("lagna", "Mesha")
    lagna_idx = SIGNS.index(lagna) if lagna in SIGNS else 0
    natal_moon = chart.get("basic_details", {}).get("moon_sign", "Mesha")
    natal_moon_idx = SIGNS.index(natal_moon) if natal_moon in SIGNS else 0

    transit_houses = config.get("transit_houses", [1, 5, 9])
    karaka_sign_house = config.get("transit_karaka_sign_house")
    is_negative_domain = config.get("transit_aspect_negative", False)
    special_rules = config.get("special_rules", [])

    # Find natal sign of domain primary karaka / lord
    primary_k = config.get("primary_karaka")
    natal_karaka_sign = None
    if primary_k:
        planets = chart.get("planets", {})
        if primary_k in planets:
            natal_karaka_sign = planets[primary_k].get("sign")

    # Generate monthly dates (sample at 15th of each month)
    scored_months: List[ScoredMonth] = []

    curr_year = start_date.year
    curr_month = start_date.month

    max_months = 180  # cap at 15 years
    month_count = 0

    while month_count < max_months:
        m_start = date(curr_year, curr_month, 1)
        if curr_month == 12:
            next_start = date(curr_year + 1, 1, 1)
        else:
            next_start = date(curr_year, curr_month + 1, 1)

        m_end = next_start - date.resolution

        if m_start > end_date:
            break

        sample_dt = date(curr_year, curr_month, 15)
        month_count += 1

        active_transits = {}
        reasons = []

        # 1. Evaluate Jupiter
        jup_sign, jup_house, jup_aspects = _get_planet_sign_house_at_date(sample_dt, "Jupiter", lagna)
        active_transits["Jupiter"] = {"sign": jup_sign, "house": jup_house, "aspects": jup_aspects}

        jup_pts = 0
        if not is_negative_domain:
            if jup_house in transit_houses:
                jup_pts += 3
                reasons.append(f"Jupiter transits domain house {jup_house}")

            matched_jup_aspects = [h for h in jup_aspects if h in transit_houses]
            if matched_jup_aspects:
                jup_pts += 2 * len(matched_jup_aspects)
                reasons.append(f"Jupiter aspects domain house(s) {matched_jup_aspects}")

            if karaka_sign_house and jup_house == karaka_sign_house:
                jup_pts += 2
                reasons.append(f"Jupiter transits karaka house {karaka_sign_house}")

            if jup_sign in ("Karka", "Dhanu", "Meena"):
                jup_pts += 1
                reasons.append(f"Jupiter is exalted/own sign in {jup_sign}")

            # Jupiter in kendra from Moon
            jup_from_moon = (SIGNS.index(jup_sign) - natal_moon_idx) % 12 + 1
            if jup_from_moon in (1, 4, 7, 10):
                jup_pts += 1
        else:
            # Negative domain: Jupiter protection reduces severity
            if jup_house in transit_houses:
                jup_pts += 2
                reasons.append(f"Jupiter protection in domain house {jup_house}")

        # Max achievable Jupiter points = 9 for benefic domains, 4 for negative domains
        max_jup = 9.0 if not is_negative_domain else 4.0
        jup_subscore = max(0.0, min(1.0, jup_pts / max_jup))

        # 2. Evaluate Saturn
        sat_sign, sat_house, sat_aspects = _get_planet_sign_house_at_date(sample_dt, "Saturn", lagna)
        active_transits["Saturn"] = {"sign": sat_sign, "house": sat_house, "aspects": sat_aspects}

        sat_pts = 0
        saturn_penalty = 0.0

        if is_negative_domain:
            if sat_house in transit_houses:
                sat_pts += 3
                reasons.append(f"Saturn transits domain house {sat_house} (activates discipline/health)")

            matched_sat_aspects = [h for h in sat_aspects if h in transit_houses]
            if matched_sat_aspects:
                sat_pts += 2 * len(matched_sat_aspects)
                reasons.append(f"Saturn aspects domain house(s) {matched_sat_aspects}")

            if sat_sign in ("Tula", "Makara", "Kumbha"):
                sat_pts += 1
                reasons.append(f"Saturn is exalted/own sign in {sat_sign}")
            max_sat = 6.0
            sat_subscore = max(0.0, min(1.0, sat_pts / max_sat))
        else:
            # Benefic domain: Saturn direct transit or aspect applies penalty
            if sat_house in transit_houses:
                saturn_penalty = 1.0
                reasons.append(f"Saturn transits domain house {sat_house} (blocking influence)")
            elif any(h in transit_houses for h in sat_aspects):
                saturn_penalty = 0.5
                reasons.append(f"Saturn aspects domain house(s)")
            sat_subscore = 0.0

        # 3. Evaluate Rahu & Ketu
        rahu_sign, rahu_house, rahu_aspects = _get_planet_sign_house_at_date(sample_dt, "Rahu", lagna)
        ketu_sign, ketu_house, ketu_aspects = _get_planet_sign_house_at_date(sample_dt, "Ketu", lagna)

        active_transits["Rahu"] = {"sign": rahu_sign, "house": rahu_house, "aspects": rahu_aspects}
        active_transits["Ketu"] = {"sign": ketu_sign, "house": ketu_house, "aspects": ketu_aspects}

        node_pts = 0
        nodes_penalty = 0.0

        if is_negative_domain:
            if rahu_house in transit_houses:
                node_pts += 2
                reasons.append(f"Rahu transits domain house {rahu_house}")
            if ketu_house in transit_houses:
                node_pts += 2
                reasons.append(f"Ketu transits domain house {ketu_house}")
            if any(h in transit_houses for h in rahu_aspects + ketu_aspects):
                node_pts += 1
                reasons.append("Rahu/Ketu aspect domain house(s)")
            node_subscore = max(0.0, min(1.0, node_pts / 3.0))
        else:
            if rahu_house in transit_houses or ketu_house in transit_houses:
                nodes_penalty = 1.0
                reasons.append(f"Rahu/Ketu transit domain house (disruptive influence)")
            elif any(h in transit_houses for h in rahu_aspects + ketu_aspects):
                nodes_penalty = 0.5
                reasons.append("Rahu/Ketu aspect domain house(s)")
            node_subscore = 0.0

        if domain == "marriage" and (rahu_house in (1, 7) or ketu_house in (1, 7)):
            reasons.append("Rahu/Ketu on 1H/7H axis (unconventional partnerships)")

        # 4. Sade Sati Modifier
        sade_info = is_sade_sati_active(sat_sign, natal_moon)
        sade_sati_modifier = 0.0
        if sade_info["active"]:
            if domain in ("health", "marriage", "career"):
                sade_sati_modifier = -0.15
                reasons.append(f"Sade Sati active ({sade_info['phase']}) — caution for {domain}")
            elif domain in ("challenges", "spirituality", "education"):
                sade_sati_modifier = 0.15
                reasons.append(f"Sade Sati active ({sade_info['phase']}) — intensifies focus for {domain}")

        # Final Transit score formula
        if not is_negative_domain:
            raw_transit = (0.65 * jup_subscore) - (0.25 * saturn_penalty) - (0.10 * nodes_penalty) + sade_sati_modifier
        else:
            raw_transit = (0.65 * sat_subscore) + (0.20 * node_subscore) + (0.15 * jup_subscore) + sade_sati_modifier

        month_score = max(0.0, min(1.0, raw_transit))
        if month_score == 0.0 and not reasons:
            month_score = 0.20  # baseline if no specific transits active
            reasons.append("Baseline transit activity")

        # 5. Apply Special Rules
        if "jupiter_return_7h" in special_rules and jup_house == 7 and natal_karaka_sign and jup_sign == natal_karaka_sign:
            month_score += 0.20
            reasons.append("Jupiter return to 7H (marriage blessing)")

        if "saturn_7h_block" in special_rules and sat_house == 7 and domain == "marriage":
            month_score *= 0.60
            reasons.append("Saturn 7H transit block multiplier (0.6)")

        if "saturn_10h_activates" in special_rules and sat_house == 10 and domain == "career":
            month_score += 0.20
            reasons.append("Saturn 10H transit activates career responsibilities")

        final_score = round(max(0.0, min(1.0, month_score)), 2)

        scored_months.append(
            ScoredMonth(
                month_start=m_start,
                month_end=m_end,
                score=final_score,
                reasons=list(dict.fromkeys(reasons)),
                active_transits=active_transits,
                sub_scores={
                    "jupiter": round(jup_subscore, 2),
                    "saturn": round(sat_subscore, 2),
                    "nodes": round(node_subscore, 2),
                    "sade_sati_modifier": round(sade_sati_modifier, 2),
                },
            )
        )

        # Advance to next month
        if curr_month == 12:
            curr_year += 1
            curr_month = 1
        else:
            curr_month += 1

    return scored_months
