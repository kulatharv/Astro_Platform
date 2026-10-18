"""Children & Next Generation Domain Evaluator."""

from modules.prediction.scoring import (
    _score_planets_in_houses, _score_house_lord, _dasha_activates,
    _dosha_present, _yoga_present, _pct, _ordinal
)
from modules.prediction.remedies import _timing_windows, _build_remedies


def analyse_children(ctx: dict) -> dict:
    pm = ctx["planet_map"]
    hl = ctx["house_lords"]

    jupiter = pm.get("Jupiter",{}); sun=pm.get("Sun",{}); moon=pm.get("Moon",{})
    lord_5 = hl[5]; l5d = pm.get(lord_5,{})
    h5_occ = [p for p,d in pm.items() if d["house"]==5]
    h9_occ = [p for p,d in pm.items() if d["house"]==9]

    base   = _score_planets_in_houses(ctx, [5,9,1])
    l5s    = _score_house_lord(ctx, 5)
    j_sc   = jupiter.get("str_score",0) + (2 if jupiter.get("house") in (5,9,1) else 0)
    total  = base + l5s + j_sc

    dasha_active = _dasha_activates(ctx, [5,9])
    pct = _pct(50, total, 10 if dasha_active else 0)

    putra_dosh = _dosha_present(ctx, ["Putra","Santana"])
    santana_yoga = _yoga_present(ctx, ["Santana","Putra"])

    j_h = jupiter.get("house",5)
    count = "Multiple children possible" if j_h in (5,11) and jupiter.get("str_score",0)>=0 \
            else "1-2 children indicated" if jupiter.get("str_score",0)>=0 \
            else "Challenges in childbearing — seek remedies"

    sign5 = ctx["house_signs"][5]
    MALE_SIGNS = ["Mesha","Mithuna","Simha","Dhanu","Kumbha"]
    gender_txt = "Male child indicated" if sign5 in MALE_SIGNS else "Female child indicated"

    child_nature = f"Child likely to be {'creative and intelligent' if 'Jupiter' in h5_occ or 'Mercury' in h5_occ else 'energetic and ambitious' if 'Mars' in h5_occ else 'artistic and sensitive' if 'Venus' in h5_occ or 'Moon' in h5_occ else 'disciplined and serious' if 'Saturn' in h5_occ else 'independent and bright'}"

    timing   = _timing_windows(ctx, [5,9], "children")
    remedies = _build_remedies(ctx, ["Jupiter"] if j_sc<0 else [], "children")

    return {
        "domain":"Children & Next Generation","icon":"❋","score":pct,
        "count_indicator":count,"gender_indicator":gender_txt,
        "child_nature":child_nature,"putra_dosh":putra_dosh,"santana_yoga":santana_yoga,
        "fifth_lord":f"{lord_5} in {_ordinal(l5d.get('house',0))}H — {l5d.get('strength','')}",
        "h5_planets":h5_occ,"jupiter_position":f"Jupiter in {_ordinal(jupiter.get('house',1))}H — {jupiter.get('strength','')}",
        "dasha_active":dasha_active,"timing":timing,"remedies":remedies,
        "analysis":f"Jupiter (putra karaka) in {_ordinal(jupiter.get('house',1))} house ({jupiter.get('strength','')}). 5th lord {lord_5} in {_ordinal(l5d.get('house',1))} house. {count}. {child_nature}. Timing: {timing['best_window']}.",
    }


_children = analyse_children
