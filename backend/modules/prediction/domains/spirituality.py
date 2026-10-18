"""Spirituality & Karma Domain Evaluator."""

from modules.prediction.scoring import _domain_score, _ordinal
from modules.prediction.remedies import _timing, _build_remedies, _house_lord_str


def analyse_spirituality(ctx: dict) -> dict:
    pm=ctx["planet_map"]; hl=ctx["house_lords"]; fn=ctx.get("fn",{}); ns=ctx.get("net_scores",{}); yogas=ctx.get("yogas",[])

    result=_domain_score(ctx,[9,12],karaka="Jupiter",secondary_houses=[1,5,8])
    sc=result["score"]

    ketu=pm.get("Ketu",{}); jupiter=pm.get("Jupiter",{})
    lord_9=hl[9]; lord_12=hl[12]

    ketu_h=ketu.get("house",1)
    spiritual_inc=(ketu_h in (1,5,9,12) and ns.get("Ketu",0)>=-1) or (ns.get("Jupiter",0)>=1 and jupiter.get("house") in (9,12))

    moksha=[y for y in yogas if any(k in (y if isinstance(y, str) else y.get("name","")) for k in ("Vipreet","Moksha","Kaal Sarp"))]

    moon_nak=pm.get("Moon",{}).get("nakshatra","Ashwini")
    DEITY={
        "Ashwini":"Ashwini Kumaras","Bharani":"Lord Yama","Krittika":"Lord Agni",
        "Rohini":"Lord Brahma / Krishna","Mrigashira":"Soma (Chandra)","Ardra":"Lord Shiva / Rudra",
        "Punarvasu":"Mother Aditi","Pushya":"Lord Brihaspati / Shiva","Ashlesha":"Naga Devatas",
        "Magha":"Pitrus (Ancestors)","Purva Phalguni":"Lord Bhaga","Uttara Phalguni":"Lord Aryaman",
        "Hasta":"Surya (Savitri)","Chitra":"Lord Vishwakarma","Swati":"Lord Vayu",
        "Vishakha":"Indra and Agni","Anuradha":"Lord Mitra","Jyeshtha":"Lord Indra",
        "Mula":"Nirrti (Kali)","Purva Ashadha":"Apas (Water deities)","Uttara Ashadha":"Vishwadevas",
        "Shravana":"Lord Vishnu","Dhanishta":"Ashta Vasus","Shatabhisha":"Lord Varuna",
        "Purva Bhadrapada":"Aja Ekapada","Uttara Bhadrapada":"Ahir Budhanya","Revati":"Pusha",
    }
    deity=DEITY.get(moon_nak,"Lord Vishnu")

    ketu_domain=["self-mastery","wealth and family","communication","home and comfort",
                 "creativity and past merit","service and karma","partnerships","occult and transformation",
                 "dharma and teacher","career and action","social connections","liberation and loss"][ketu_h-1]
    past_karma=f"Ketu in {_ordinal(ketu_h)} house — past-life mastery in {ketu_domain}. This life, the soul seeks to balance through the opposite {_ordinal(((ketu_h+5)%12)+1)} house themes."

    sign9=ctx["house_signs"][9]
    DHARMA={"Mesha":"courage and individual initiative","Vrishabha":"sensory service and material dharma",
            "Mithuna":"communication and mental dharma","Karka":"emotional service and family dharma",
            "Simha":"leadership and creative dharma","Kanya":"service, healing and perfection",
            "Tula":"justice, balance and relational dharma","Vrischika":"transformation and occult dharma",
            "Dhanu":"knowledge, teaching and philosophical dharma","Makara":"discipline and structural dharma",
            "Kumbha":"innovation, community and humanitarian dharma","Meena":"surrender, compassion and spiritual dharma"}
    dharma=DHARMA.get(sign9,"alignment with cosmic order")

    remedies=_build_remedies(ctx,["Jupiter","Ketu"],"spirituality")
    timing=_timing(ctx,[9,12,5],"spirituality")

    j_ns=round(ns.get("Jupiter",0),1); l9_ns=round(ns.get(lord_9,0),1)

    return {
        "domain":"Spirituality & Karma","icon":"☯","score":sc,
        "spiritual_inclination":spiritual_inc,"moksha_yoga":moksha,"deity":deity,"past_karma":past_karma,
        "dharma_path":f"9th house in {sign9} — dharma through {dharma}",
        "ninth_lord":_house_lord_str(ctx,9),
        "ketu_position":f"Ketu in {_ordinal(ketu_h)}H",
        "dasha_active":result["dasha_active"],
        "timing":timing,"remedies":remedies,
        "analysis":f"9th lord {lord_9} net {l9_ns:+.1f}. Jupiter net {j_ns:+.1f}. {'Strong spiritual inclination — Ketu in spiritual house.' if spiritual_inc else 'Spiritual growth through material experience first.'} {past_karma} Deity: {deity}. Dharma: {dharma}.",
        "_scoring":result,
    }


_spirituality = analyse_spirituality
