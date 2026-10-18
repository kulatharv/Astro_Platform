"""Travel & Foreign Domain Evaluator."""

from modules.prediction.scoring import (
    _score_planets_in_houses, _score_house_lord, _dasha_activates,
    _pct, _ordinal
)
from modules.prediction.remedies import _timing_windows, _build_remedies


def analyse_travel(ctx: dict) -> dict:
    pm = ctx["planet_map"]
    hl = ctx["house_lords"]

    rahu=pm.get("Rahu",{}); ketu=pm.get("Ketu",{}); moon=pm.get("Moon",{})
    lord_12=hl[12]; l12d=pm.get(lord_12,{})
    lord_9=hl[9]; l9d=pm.get(lord_9,{})
    h12_occ=[p for p,d in pm.items() if d["house"]==12]
    h9_occ=[p for p,d in pm.items() if d["house"]==9]

    base  = _score_planets_in_houses(ctx, [12,9,3])
    l12s  = _score_house_lord(ctx, 12)
    r_sc  = 2 if rahu.get("house") in (12,9,3) else 0
    total = base + l12s + r_sc

    dasha_active = _dasha_activates(ctx, [12,9,3])
    pct = _pct(50, total, 8 if dasha_active else 0)

    foreign_strong = rahu.get("house") in (12,9,7,1) or "Rahu" in h12_occ
    visa_ok = lord_9 == "Jupiter" or l9d.get("str_score",0)>=1 or "Jupiter" in h9_occ

    sign4=ctx["house_signs"][4]
    DIR_MAP={"Mesha":"East","Vrishabha":"South","Mithuna":"North","Karka":"North-West",
             "Simha":"East","Kanya":"South","Tula":"West","Vrischika":"North",
             "Dhanu":"North-East","Makara":"South","Kumbha":"West","Meena":"North-East"}
    direction = DIR_MAP.get(sign4,"Variable direction")

    timing  = _timing_windows(ctx, [12,9,3], "travel")
    remedies= _build_remedies(ctx, ["Rahu"] if not foreign_strong else [], "travel")

    return {
        "domain":"Travel & Foreign","icon":"✈","score":pct,
        "foreign_settlement":foreign_strong,"visa_success":visa_ok,
        "direction":direction,
        "overseas_career":"Strong overseas career potential" if rahu.get("house")==10 else "Domestic career more prominent",
        "twelfth_lord":f"{lord_12} in {_ordinal(l12d.get('house',0))}H — {l12d.get('strength','')}",
        "rahu_position":f"Rahu in {_ordinal(rahu.get('house',1))}H — key foreign indicator",
        "dasha_active":dasha_active,"timing":timing,"remedies":remedies,
        "analysis":f"12th house (foreign lands) ruled by {lord_12} in {_ordinal(l12d.get('house',1))} house. Rahu in {_ordinal(rahu.get('house',1))} house. Foreign settlement: {'strongly indicated' if foreign_strong else 'less prominent'}. Best direction: {direction}. Travel window: {timing['best_window']}.",
    }


_travel = analyse_travel
