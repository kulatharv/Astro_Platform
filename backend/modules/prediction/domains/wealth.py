"""Wealth & Finance Domain Evaluator."""

from modules.prediction.scoring import (
    _score_planets_in_houses, _score_house_lord, _dasha_activates,
    _yoga_present, _pct, _ordinal
)
from modules.prediction.remedies import _timing_windows, _build_remedies


def analyse_wealth(ctx: dict) -> dict:
    pm = ctx["planet_map"]
    hl = ctx["house_lords"]

    jupiter = pm.get("Jupiter",{})
    venus   = pm.get("Venus",{})
    moon    = pm.get("Moon",{})

    lord_2  = hl[2]; l2d = pm.get(lord_2,{})
    lord_11 = hl[11]; l11d = pm.get(lord_11,{})
    h2_occ  = [p for p,d in pm.items() if d["house"]==2]
    h11_occ = [p for p,d in pm.items() if d["house"]==11]

    base   = _score_planets_in_houses(ctx, [2,11,9,5])
    l2s    = _score_house_lord(ctx, 2)
    l11s   = _score_house_lord(ctx, 11)
    j_sc   = jupiter.get("str_score",0) + (2 if jupiter.get("house") in (2,11,5,9) else 0)
    total  = base + l2s + l11s + j_sc

    dasha_active = _dasha_activates(ctx, [2,11,5,9])
    pct = _pct(50, total, 10 if dasha_active else 0)

    dhana_yogas = _yoga_present(ctx, ["Dhana","Lakshmi","Kubera","Wealth"])

    sign11 = ctx["house_signs"][11]
    SOURCE_MAP = {
        "Mesha":"business, real estate, initiative-driven income",
        "Vrishabha":"banking, agriculture, luxury trade, accumulation",
        "Mithuna":"communication, media, commission, intellectual work",
        "Karka":"real estate, food industry, family business, water",
        "Simha":"government, leadership, speculation, creative work",
        "Kanya":"service industry, health, detailed analytical work",
        "Tula":"partnerships, trade, legal, design, negotiation",
        "Vrischika":"research, insurance, inheritance, occult",
        "Dhanu":"education, exports, foreign income, law",
        "Makara":"professional services, construction, government",
        "Kumbha":"technology, NGO, innovation, irregular but large gains",
        "Meena":"spiritual services, medicine, arts, sea trade",
    }
    income_sources = SOURCE_MAP.get(sign11,"varied income streams")

    h8_occ  = [p for p,d in pm.items() if d["house"]==8]
    sudden_gain = "Lottery/sudden gains potential" if "Rahu" in h8_occ or "Jupiter" in h8_occ \
                  else "Moderate unexpected income possible" if "Moon" in h8_occ \
                  else "Earned wealth more prominent than windfalls"

    h6_saturn = pm.get("Saturn",{}).get("house") == 6
    debt_risk  = "6th house alignment indicates prudent budget management. Maintain disciplined finances and structured investments." if h6_saturn \
                 else "No strong debt indicators in current planetary configuration."

    timing   = _timing_windows(ctx, [2,11,9], "wealth")
    remedies = _build_remedies(ctx, ["Jupiter","Venus"] if j_sc < 0 else (["Jupiter"] if j_sc==0 else []), "wealth")

    return {
        "domain":"Wealth & Finance","icon":"₹","score":pct,
        "dhana_yogas":dhana_yogas,"income_sources":income_sources,
        "sudden_gain":sudden_gain,"debt_risk":debt_risk,
        "second_lord":f"{lord_2} in {_ordinal(l2d.get('house',0))}H — {l2d.get('strength','')}",
        "eleventh_lord":f"{lord_11} in {_ordinal(l11d.get('house',0))}H — {l11d.get('strength','')}",
        "h2_planets":h2_occ,"h11_planets":h11_occ,
        "dasha_active":dasha_active,"timing":timing,"remedies":remedies,
        "analysis":_wealth_narrative(ctx,pct,dhana_yogas,income_sources,timing),
    }


def _wealth_narrative(ctx,pct,yogas,sources,timing):
    md=ctx["mahadasha"]; ad=ctx["antardasha"]
    j=ctx["planet_map"].get("Jupiter",{})
    parts=[]
    parts.append(f"Jupiter, the primary wealth karaka, is placed in the {_ordinal(j.get('house',1))} house in {j.get('sign','')} — {j.get('strength','')}.")
    parts.append(f"Primary income sources: {sources}.")
    if yogas:
        parts.append(f"Dhana Yogas present: {', '.join(yogas)} — strong wealth accumulation potential.")
    parts.append(f"{md}/{ad} dasha {'is actively triggering' if timing['dasha_active'] else 'does not directly trigger'} wealth houses. Best financial window: {timing['best_window']}.")
    return " ".join(parts)


_wealth = analyse_wealth
