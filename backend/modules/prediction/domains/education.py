"""Education & Skills Domain Evaluator."""

from modules.prediction.scoring import (
    _score_planets_in_houses, _score_house_lord, _dasha_activates,
    _yoga_present, _pct, _ordinal
)
from modules.prediction.remedies import _timing_windows, _build_remedies


def analyse_education(ctx: dict) -> dict:
    pm = ctx["planet_map"]
    hl = ctx["house_lords"]

    mercury = pm.get("Mercury",{}); jupiter = pm.get("Jupiter",{}); sun=pm.get("Sun",{})
    lord_4 = hl[4]; l4d = pm.get(lord_4,{})
    lord_5 = hl[5]; l5d = pm.get(lord_5,{})
    h4_occ = [p for p,d in pm.items() if d["house"]==4]
    h5_occ = [p for p,d in pm.items() if d["house"]==5]

    base  = _score_planets_in_houses(ctx, [4,5,9])
    l4s   = _score_house_lord(ctx, 4)
    l5s   = _score_house_lord(ctx, 5)
    m_sc  = mercury.get("str_score",0)+(1 if mercury.get("house") in (4,5,9) else 0)
    j_sc  = jupiter.get("str_score",0)+(1 if jupiter.get("house") in (4,5,9) else 0)
    total = base + l4s + l5s + m_sc + j_sc

    dasha_active = _dasha_activates(ctx, [4,5,9])
    pct = _pct(50, total, 8 if dasha_active else 0)

    sign4 = ctx["house_signs"][4]
    STUDY_FIELDS = {
        "Mesha":"engineering, sports science, defense, physical therapy",
        "Vrishabha":"commerce, arts, agriculture, banking, architecture",
        "Mithuna":"journalism, languages, IT, mass communication, mathematics",
        "Karka":"nursing, psychology, hospitality, history",
        "Simha":"medicine, management, drama, literature, leadership",
        "Kanya":"medicine, accounting, research, editing, pharmacy",
        "Tula":"law, design, diplomacy, social sciences, fine arts",
        "Vrischika":"research, forensics, psychology, occult sciences",
        "Dhanu":"philosophy, law, education, foreign languages, travel",
        "Makara":"administration, civil services, engineering, finance",
        "Kumbha":"computer science, electronics, astrology, innovation",
        "Meena":"spirituality, medicine, arts, marine, music",
    }
    study_fields = STUDY_FIELDS.get(sign4,"diverse academic fields")

    vidya_yoga = _yoga_present(ctx, ["Saraswati","Vidya","Budhaditya"])
    foreign_edu = "Rahu" in h5_occ or pm.get("Rahu",{}).get("house") in (4,5,9)

    timing = _timing_windows(ctx, [4,5,9], "education")
    remedies = _build_remedies(ctx, ["Mercury"] if m_sc<0 else [], "education")

    return {
        "domain":"Education & Skills","icon":"✦","score":pct,
        "study_fields":study_fields,"vidya_yoga":vidya_yoga,
        "foreign_education":foreign_edu,
        "competitive_success":"Good competitive exam success" if pct>65 else "Focused preparation needed for competitive exams",
        "mercury_position":f"Mercury in {_ordinal(mercury.get('house',1))}H — {mercury.get('strength','')}",
        "dasha_active":dasha_active,"timing":timing,"remedies":remedies,
        "analysis":f"4th/5th houses govern education. Mercury (intellect) in {_ordinal(mercury.get('house',1))} house — {mercury.get('strength','')}. Best study fields: {study_fields}. {('Vidya Yoga present: '+', '.join(vidya_yoga)+' — academic distinction likely.' if vidya_yoga else '')} Foreign education: {'indicated' if foreign_edu else 'less prominent'}.",
    }


_education = analyse_education
