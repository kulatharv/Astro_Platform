"""Health & Longevity Domain Evaluator."""

from modules.prediction.scoring import (
    _score_planets_in_houses, _score_house_lord, _dasha_activates,
    _dosha_present, _pct, _ordinal
)
from modules.prediction.remedies import _timing_windows, _build_remedies


def analyse_health(ctx: dict) -> dict:
    pm  = ctx["planet_map"]
    hl  = ctx["house_lords"]

    sun    = pm.get("Sun",{})
    moon   = pm.get("Moon",{})
    saturn = pm.get("Saturn",{})
    mars   = pm.get("Mars",{})

    lord_1 = hl[1]; l1d = pm.get(lord_1,{})
    lord_6 = hl[6]; l6d = pm.get(lord_6,{})
    lord_8 = hl[8]; l8d = pm.get(lord_8,{})

    h1_occ = [p for p,d in pm.items() if d["house"]==1]
    h6_occ = [p for p,d in pm.items() if d["house"]==6]
    h8_occ = [p for p,d in pm.items() if d["house"]==8]

    base  = _score_planets_in_houses(ctx, [1,6,8])
    l1s   = _score_house_lord(ctx, 1)
    sun_sc= sun.get("str_score",0)
    total = base + l1s + sun_sc

    dasha_active = _dasha_activates(ctx, [6,8,12])
    pct = _pct(70, -total, -8 if dasha_active else 0)

    sign6 = ctx["house_signs"][6]
    ORGAN_MAP = {
        "Mesha":"head, brain, eyes","Vrishabha":"throat, neck, thyroid",
        "Mithuna":"lungs, arms, shoulders","Karka":"chest, stomach, breast",
        "Simha":"heart, spine, upper back","Kanya":"intestines, digestion, skin",
        "Tula":"kidneys, lower back, ovaries","Vrischika":"reproductive organs, excretory",
        "Dhanu":"hips, thighs, liver","Makara":"knees, bones, joints, teeth",
        "Kumbha":"ankles, nervous system, circulation","Meena":"feet, lymphatic, immune",
    }
    lagna_sign = ctx["lagna"]
    weak_organs = ORGAN_MAP.get(sign6,"general constitution")
    lagna_organs = ORGAN_MAP.get(lagna_sign,"overall vitality")

    DOSHA_MAP = {
        "Mesha":"Pitta","Vrishabha":"Kapha","Mithuna":"Vata","Karka":"Kapha",
        "Simha":"Pitta","Kanya":"Vata","Tula":"Vata","Vrischika":"Pitta",
        "Dhanu":"Pitta","Makara":"Vata","Kumbha":"Vata","Meena":"Kapha",
    }
    ayurvedic_dosha = DOSHA_MAP.get(lagna_sign,"Tridoshic")

    arishta = _dosha_present(ctx, ["Arishta","Balarishta","Kaal Sarp"])
    mental_h = moon.get("house",1)
    mental_ok = moon.get("str_score",0) >= 0 and mental_h not in (6,8,12)

    surgery_risk = "Mars" in h8_occ or "Mars" in h6_occ or saturn.get("house")==8
    disease_periods = f"Periods to watch: {ctx['mahadasha']} dasha / {ctx['antardasha']} antardasha if Saturn or Mars transits 1st, 6th or 8th"

    timing   = _timing_windows(ctx, [6,8,1], "health")
    remedies = _build_remedies(ctx, ["Sun"] if sun.get("str_score",0)<0 else (["Mars"] if mars.get("str_score",0)<0 else ["Saturn"]), "health")

    return {
        "domain":"Health & Longevity","icon":"✚","score":pct,
        "weak_organs":weak_organs,"lagna_organs":lagna_organs,
        "ayurvedic_dosha":ayurvedic_dosha,"emotional_sensitivity":"elevated" if not mental_ok else "balanced",
        "wellness_focus":surgery_risk,
        "wellness_txt":"Classical Vedic texts highlight this placement as a reminder to prioritize preventive health care and routine medical checkups." if surgery_risk else "Planetary alignment supports steady physical vitality.",
        "arishta_doshas":arishta,"disease_periods":disease_periods,
        "first_lord":f"{lord_1} in {_ordinal(l1d.get('house',0))}H — {l1d.get('strength','')}",
        "dasha_active":dasha_active,"timing":timing,"remedies":remedies,
        "analysis":_health_narrative(ctx,pct,weak_organs,ayurvedic_dosha,mental_ok),
    }


def _health_narrative(ctx,pct,organs,dosha,mental_ok):
    lagna=ctx["lagna"]; sun=ctx["planet_map"].get("Sun",{}); moon=ctx["planet_map"].get("Moon",{})
    parts=[]
    parts.append(f"Your Lagna (Ascendant) in {lagna} gives a {dosha} constitution — focus on balancing this Ayurvedic dosha through diet, lifestyle and seasonal cleansing.")
    parts.append(f"Vulnerable areas include {organs} — preventive care for these systems is advised.")
    parts.append(f"Sun (vitality karaka) is in the {_ordinal(sun.get('house',1))} house — {sun.get('strength','Neutral')}.")
    parts.append(f"Mental health is {'stable and resilient' if mental_ok else 'sensitive — Moon afflicted; manage stress proactively'}.")
    return " ".join(parts)


_health = analyse_health
