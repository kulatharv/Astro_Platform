"""Challenges & Dosha Domain Evaluator."""

from shared.veda import evaluate_mangal_dosha, evaluate_pitru_dosha
from modules.prediction.scoring import RASHI, _ordinal
from modules.prediction.remedies import _build_remedies


def analyse_challenges(ctx: dict) -> dict:
    pm  = ctx["planet_map"]
    hl  = ctx["house_lords"]

    rahu = pm.get("Rahu",{}); ketu=pm.get("Ketu",{})
    saturn=pm.get("Saturn",{}); mars=pm.get("Mars",{})

    rahu_h = rahu.get("house",1); ketu_h = ketu.get("house",1)
    all_others = [p for p in pm if p not in ("Rahu","Ketu")]
    ks_range = list(range(min(rahu_h,ketu_h), max(rahu_h,ketu_h)+1))
    kaal_sarp = all(pm[p]["house"] in ks_range for p in all_others if p in pm)

    eval_m = evaluate_mangal_dosha(pm)
    mangal = eval_m["present"] and not eval_m.get("cancelled", False)

    moon_sign_idx = RASHI.index(pm.get("Moon",{}).get("sign","Mesha")) if pm.get("Moon",{}).get("sign") in RASHI else 0
    sat_sign_idx  = RASHI.index(saturn.get("sign","Mesha")) if saturn.get("sign") in RASHI else 0
    sade_sati = abs(sat_sign_idx - moon_sign_idx) in (0,1,11)

    eval_p = evaluate_pitru_dosha(pm)
    pitru = eval_p["present"]

    grahan_planets = []
    for lum in ["Sun","Moon"]:
        lum_h = pm.get(lum,{}).get("house",0)
        if lum_h in (rahu.get("house",0), ketu.get("house",0)):
            grahan_planets.append(lum)
    grahan = len(grahan_planets) > 0

    doshas_found = []
    if kaal_sarp: doshas_found.append({"name":"Kaal Sarp Dosh","severity":"High","desc":"All planets hemmed between Rahu and Ketu — intense karmic patterns, obstacles followed by sudden rises."})
    if mangal:    doshas_found.append({"name":"Mangal Dosh","severity":"Moderate","desc":f"Mars in {_ordinal(mars.get('house',1))} house — relationship friction, energy imbalance. Match with similar chart."})
    if sade_sati: doshas_found.append({"name":"Shani Sade Sati","severity":"Moderate","desc":"Saturn transiting near Moon sign — 7.5-year karmic cleansing phase."})
    if pitru:     doshas_found.append({"name":"Pitru Dosh","severity":"Moderate","desc":"Ancestral karmic debt — offer tarpan on Amavasya and Pitru Paksha."})
    if grahan:    doshas_found.append({"name":"Grahan Dosh","severity":"Moderate" if len(grahan_planets)==1 else "High","desc":f"Rahu/Ketu eclipsing {', '.join(grahan_planets)} — emotional or identity challenges."})

    h6_malefics = [p for p in ["Saturn","Mars","Rahu"] if pm.get(p,{}).get("house")==6]
    legal_risk = len(h6_malefics)>0

    total_severity = len(doshas_found)
    pct = max(10, min(90, 80 - total_severity*15))

    remedies = _build_remedies(ctx,
        (["Rahu","Ketu"] if kaal_sarp else []) +
        (["Mars"] if mangal else []) +
        (["Saturn"] if sade_sati else []) +
        (["Sun"] if pitru else []),
        "challenges")

    return {
        "domain":"Challenges & Doshas","icon":"⚡","score":pct,
        "kaal_sarp":kaal_sarp,"mangal_dosh":mangal,"sade_sati":sade_sati,
        "pitru_dosh":pitru,"grahan_dosh":grahan,
        "doshas_found":doshas_found,"dosha_count":total_severity,
        "legal_risk":legal_risk,
        "legal_txt":"6th house affliction — highlights the importance of clear agreements, documentation, and diplomacy in professional matters." if legal_risk else "No strong legal trouble indicators.",
        "remedies":remedies,
        "analysis":_challenges_narrative(doshas_found),
    }


def _challenges_narrative(doshas_found):
    if not doshas_found:
        return "No major doshas detected — chart is relatively clean and free from major planetary afflictions."
    names = ", ".join([d["name"] for d in doshas_found])
    return f"{len(doshas_found)} dosha(s) detected: {names}. Appropriate remedies can significantly mitigate these effects. Consult an experienced Vedic astrologer for personalised rituals."


_challenges = analyse_challenges
