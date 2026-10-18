"""Window fusion engine combining Dasha (60%) + Gochara (40%) into ranked, smoothed timing windows."""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Dict, Any, List, Optional

from modules.prediction.timing_config import get_domain_timing_config
from modules.prediction.timing_dasha import score_dasha_periods, ScoredPeriod
from modules.prediction.timing_transit import score_transit_months, ScoredMonth


@dataclass
class TimingWindow:
    start_date: date
    end_date: date
    peak_date: date
    peak_score: float
    confidence: str
    mahadasha: str
    antardasha: str
    pratyantardasha: str
    reasons: List[str]
    drivers: List[str]
    sub_scores: Dict[str, float]


@dataclass
class TimingFusionResult:
    timing_windows: List[TimingWindow]
    peak_window: Optional[TimingWindow]
    next_12_months_summary: str
    methodology: str
    threshold_used: float
    engine_version: str


def get_confidence_tier(score: float) -> str:
    """Return confidence tier based on peak fused score."""
    if score >= 0.75:
        return "High"
    elif score >= 0.55:
        return "Moderate"
    elif score >= 0.35:
        return "Possible"
    return "Unlikely"


def fuse_windows(
    chart: dict,
    domain: str,
    start_date: date,
    end_date: date,
    top_n: int = 5,
) -> TimingFusionResult:
    """
    Combine Dasha periods (60%) + Transit months (40%) into ranked, smoothed timing windows.
    """
    config = get_domain_timing_config(domain)
    dasha_w = config.get("dasha_weight", 0.60)
    transit_w = config.get("transit_weight", 0.40)
    special_rules = config.get("special_rules", [])

    # 1. Fetch raw Dasha and Transit scores
    dasha_periods = score_dasha_periods(chart, domain, start_date, end_date)
    transit_months = score_transit_months(chart, domain, start_date, end_date)

    if not transit_months:
        return TimingFusionResult(
            timing_windows=[],
            peak_window=None,
            next_12_months_summary=f"No timing windows generated for {domain}.",
            methodology="Dasha 60% + Gochara 40%, 15-year horizon",
            threshold_used=0.45,
            engine_version="1.0.0",
        )

    # 2. STEP A — Align time axes per monthly snapshot
    monthly_snapshots = []
    for m in transit_months:
        # Find matching dasha period covering month_start
        matching_dasha = None
        for dp in dasha_periods:
            if dp.start_date <= m.month_start <= dp.end_date or dp.start_date <= m.month_end <= dp.end_date or m.month_start <= dp.start_date <= m.month_end:
                matching_dasha = dp
                break

        d_score = matching_dasha.score if matching_dasha else 0.30
        t_score = m.score

        combined = (dasha_w * d_score) + (transit_w * t_score)

        monthly_snapshots.append({
            "month_start": m.month_start,
            "month_end": m.month_end,
            "dasha_score": d_score,
            "transit_score": t_score,
            "combined_score": round(combined, 3),
            "dasha_period": matching_dasha,
            "transit_month": m,
        })

    # 3. STEP B — 3-month rolling average smoothing
    num_months = len(monthly_snapshots)
    smoothed_scores = []
    for i in range(num_months):
        prev_s = monthly_snapshots[i - 1]["combined_score"] if i > 0 else monthly_snapshots[i]["combined_score"]
        curr_s = monthly_snapshots[i]["combined_score"]
        next_s = monthly_snapshots[i + 1]["combined_score"] if i < num_months - 1 else monthly_snapshots[i]["combined_score"]

        smooth_val = round((prev_s + curr_s + next_s) / 3.0, 3)
        smoothed_scores.append(smooth_val)
        monthly_snapshots[i]["smoothed_score"] = smooth_val

    # 4. STEP C & D — Threshold & Merge consecutive months (with 1-month gap tolerance)
    threshold = 0.45
    qualifying_indices = [i for i, snap in enumerate(monthly_snapshots) if snap["smoothed_score"] >= threshold]

    raw_groups = []
    if qualifying_indices:
        current_group = [qualifying_indices[0]]
        for idx in qualifying_indices[1:]:
            # Allow up to 1-month gap between qualifying months (diff <= 2)
            if idx - current_group[-1] <= 2:
                current_group.append(idx)
            else:
                raw_groups.append(current_group)
                current_group = [idx]
        if current_group:
            raw_groups.append(current_group)

    # 5. Build raw TimingWindow objects from groups
    built_windows = []
    for grp in raw_groups:
        grp_months = [monthly_snapshots[i] for i in grp]
        peak_snap = max(grp_months, key=lambda x: x["smoothed_score"])

        w_start = grp_months[0]["month_start"]
        w_end = grp_months[-1]["month_end"]
        peak_dt = peak_snap["month_start"]
        peak_score = peak_snap["smoothed_score"]

        d_period = peak_snap["dasha_period"]
        t_month = peak_snap["transit_month"]

        md_l = d_period.mahadasha_lord if d_period else "Jupiter"
        ad_l = d_period.antardasha_lord if d_period else "Venus"
        pd_l = d_period.pratyantardasha_lord if d_period else "Saturn"

        d_reasons = d_period.reasons if d_period else []
        t_reasons = t_month.reasons if t_month else []
        merged_reasons = list(dict.fromkeys(d_reasons + t_reasons))

        top_drivers = merged_reasons[:4]
        conf = get_confidence_tier(peak_score)

        # 6. STEP H — Special rule enforcement
        sat_house = t_month.active_transits.get("Saturn", {}).get("house") if t_month else None
        if "saturn_7h_block" in special_rules and sat_house == 7 and domain == "marriage":
            conf = "Possible"

        if "jupiter_return_7h" in special_rules and peak_score >= 0.60:
            jup_h = t_month.active_transits.get("Jupiter", {}).get("house") if t_month else None
            if jup_h == 7:
                conf = "High"

        built_windows.append(
            TimingWindow(
                start_date=w_start,
                end_date=w_end,
                peak_date=peak_dt,
                peak_score=peak_score,
                confidence=conf,
                mahadasha=md_l,
                antardasha=ad_l,
                pratyantardasha=pd_l,
                reasons=merged_reasons,
                drivers=top_drivers,
                sub_scores={
                    "dasha_score": peak_snap["dasha_score"],
                    "transit_score": peak_snap["transit_score"],
                },
            )
        )

    # 7. STEP G — Deduplicate overlapping windows (>50% overlap)
    deduped_windows: List[TimingWindow] = []
    for w in built_windows:
        if not deduped_windows:
            deduped_windows.append(w)
        else:
            prev_w = deduped_windows[-1]
            overlap_start = max(prev_w.start_date, w.start_date)
            overlap_end = min(prev_w.end_date, w.end_date)
            if overlap_start <= overlap_end:
                overlap_days = (overlap_end - overlap_start).days + 1
                len1 = (prev_w.end_date - prev_w.start_date).days + 1
                len2 = (w.end_date - w.start_date).days + 1
                min_len = min(len1, len2)

                if min_len > 0 and (overlap_days / min_len) >= 0.50:
                    # Merge into stronger window
                    if w.peak_score > prev_w.peak_score:
                        deduped_windows[-1] = w
                    continue
            deduped_windows.append(w)

    # 8. STEP F — Rank and limit
    deduped_windows.sort(key=lambda x: x.peak_score, reverse=True)
    top_windows = deduped_windows[:top_n]
    peak_win = top_windows[0] if top_windows else None

    # Next 12 months summary
    if peak_win:
        summary_msg = f"Peak activation window for {domain} occurs around {peak_win.peak_date.strftime('%B %Y')} with {peak_win.confidence} confidence during {peak_win.mahadasha}-{peak_win.antardasha} Dasha."
    else:
        summary_msg = f"No major timing activation window identified for {domain} in the next 12 months."

    return TimingFusionResult(
        timing_windows=top_windows,
        peak_window=peak_win,
        next_12_months_summary=summary_msg,
        methodology="Dasha 60% + Gochara 40%, 15-year horizon",
        threshold_used=threshold,
        engine_version="1.0.0",
    )
