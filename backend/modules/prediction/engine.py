"""
Prediction Engine Orchestrator.
Imports all 10 domain evaluators and runs analyse_all_domains.
"""

import hashlib
from modules.prediction.scoring import _build_ctx
from modules.prediction.domains.marriage import analyse_marriage
from modules.prediction.domains.career import analyse_career
from modules.prediction.domains.wealth import analyse_wealth
from modules.prediction.domains.health import analyse_health
from modules.prediction.domains.children import analyse_children
from modules.prediction.domains.education import analyse_education
from modules.prediction.domains.property import analyse_property
from modules.prediction.domains.challenges import analyse_challenges
from modules.prediction.domains.travel import analyse_travel
from modules.prediction.domains.spirituality import analyse_spirituality


from modules.prediction.timing import compute_timing, build_timing_block


def analyse_all_domains(chart: dict) -> dict:
    chart_bytes = str(sorted((k, str(v)) for k, v in chart.items())).encode('utf-8')
    input_hash = hashlib.sha256(chart_bytes).hexdigest()[:12]
    ctx = _build_ctx(chart)

    domains = {
        "marriage":    analyse_marriage(ctx),
        "career":      analyse_career(ctx),
        "wealth":      analyse_wealth(ctx),
        "health":      analyse_health(ctx),
        "children":    analyse_children(ctx),
        "education":   analyse_education(ctx),
        "property":    analyse_property(ctx),
        "challenges":  analyse_challenges(ctx),
        "travel":      analyse_travel(ctx),
        "spirituality":analyse_spirituality(ctx),
    }

    # Attach concrete timing block per domain
    for d_name, d_val in domains.items():
        if isinstance(d_val, dict):
            legacy_t = d_val.get("timing")
            timing_block = build_timing_block(chart, d_name)
            d_val["timing"] = timing_block
            d_val["timing_legacy"] = legacy_t
            d_val["timing_windows"] = timing_block.get("timing_windows", [])
            d_val["peak_window"] = timing_block.get("peak_window")
            d_val["next_12_months_summary"] = timing_block.get("next_12_months_summary", "")
            d_val["timing_methodology"] = timing_block.get("methodology", "")
            d_val["timing_engine"] = timing_block.get("engine_version", "1.0.0")

    return {
        "engine_version": "2.0.0-modular",
        "input_hash":     input_hash,
        "lagna":          ctx["lagna"],
        "mahadasha":      ctx["mahadasha"],
        "antardasha":     ctx["antardasha"],
        "yogas_detected": ctx["yogas"],
        "domains":        domains,
    }
