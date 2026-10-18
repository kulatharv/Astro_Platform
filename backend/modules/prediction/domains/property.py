"""Property & Home Domain Evaluator."""

from modules.prediction.scoring import (
    _score_planets_in_houses, _score_house_lord, _dasha_activates,
    _pct, _ordinal
)
from modules.prediction.remedies import _timing_windows, _build_remedies


def analyse_property(ctx: dict) -> dict:
    pm = ctx["planet_map"]
    hl = ctx["house_lords"]

    mars = pm.get("Mars",{}); moon=pm.get("Moon",{}); saturn=pm.get("Saturn",{})
    lord_4 = hl[4]; l4d = pm.get(lord_4,{})
    h4_occ = [p for p,d in pm.items() if d["house"]==4]

    base  = _score_planets_in_houses(ctx, [4,2,12])
    l4s   = _score_house_lord(ctx, 4)
    m_sc  = mars.get("str_score",0)+(2 if mars.get("house") in (4,2) else 0)
    total = base + l4s + m_sc

    dasha_active = _dasha_activates(ctx, [4,12,2])
    pct = _pct(50, total, 8 if dasha_active else 0)

    sign4 = ctx["house_signs"][4]
    PROP_TYPE = {
        "Mesha":"independent house / active environment preferred",
        "Vrishabha":"fertile land, luxurious property, garden",
        "Mithuna":"apartment in busy area, multi-story building",
        "Karka":"near water body, ancestral property",
        "Simha":"large prestigious property, prominent location",
        "Kanya":"clean, hygienic, well-organized living space",
        "Tula":"beautiful, artistically designed home",
        "Vrischika":"old or hidden property, secretive location",
        "Dhanu":"property near temples, open land, hills",
        "Makara":"durable construction, traditional or stone buildings",
        "Kumbha":"modern housing society, tech-enabled home",
        "Meena":"near sea, spiritual property, irregular shape",
    }
    prop_type = PROP_TYPE.get(sign4,"varied property types")

    multiple_props = mars.get("str_score",0)>=2 or (mars.get("house")==4 and "Mars" in h4_occ)
    domestic_happiness = "Moon" in h4_occ or moon.get("house")==4 or moon.get("str_score",0)>=1

    timing = _timing_windows(ctx, [4,2,12], "property")
    remedies = _build_remedies(ctx, ["Mars"] if m_sc<0 else [], "property")

    return {
        "domain":"Property & Home","icon":"⌂","score":pct,
        "property_type":prop_type,"multiple_properties":multiple_props,
        "domestic_happiness":domestic_happiness,
        "vastu":"4th house in earthy signs — vastu compliance highly beneficial" if sign4 in ("Vrishabha","Kanya","Makara") else "Standard vastu principles apply",
        "fourth_lord":f"{lord_4} in {_ordinal(l4d.get('house',0))}H — {l4d.get('strength','')}",
        "mars_position":f"Mars in {_ordinal(mars.get('house',1))}H — {mars.get('strength','')}",
        "dasha_active":dasha_active,"timing":timing,"remedies":remedies,
        "analysis":f"4th house (property) ruled by {lord_4} in {_ordinal(l4d.get('house',1))} house — {l4d.get('strength','')}. Property type: {prop_type}. Mars (real estate karaka) in {_ordinal(mars.get('house',1))} house. {('Multiple properties possible.' if multiple_props else '')} Best purchase window: {timing['best_window']}.",
    }


_property = analyse_property
