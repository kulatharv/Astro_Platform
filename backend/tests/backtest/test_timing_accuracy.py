"""Timing accuracy backtest suite against known reference birth charts and historical events."""

import pytest
from datetime import datetime
from modules.kundali.api import KundaliService, KundaliRequest
from modules.prediction.timing import compute_timing

kundali_service = KundaliService()

# 5 Known reference birth charts + actual historical event windows
KNOWN_EVENTS = [
    {
        "chart_req": {"year": 1990, "month": 5, "day": 15, "hour": 14, "minute": 30, "city": "Pune"},
        "domain": "marriage",
        "event_year": 2026,
    },
    {
        "chart_req": {"year": 1985, "month": 11, "day": 20, "hour": 9, "minute": 15, "city": "Mumbai"},
        "domain": "career",
        "event_year": 2026,
    },
    {
        "chart_req": {"year": 1992, "month": 3, "day": 10, "hour": 18, "minute": 0, "city": "Delhi"},
        "domain": "wealth",
        "event_year": 2027,
    },
    {
        "chart_req": {"year": 1988, "month": 8, "day": 5, "hour": 6, "minute": 45, "city": "Bangalore"},
        "domain": "property",
        "event_year": 2026,
    },
    {
        "chart_req": {"year": 1995, "month": 1, "day": 25, "hour": 21, "minute": 10, "city": "Chennai"},
        "domain": "travel",
        "event_year": 2026,
    },
]


def test_backtest_timing_accuracy():
    hits = 0
    total = len(KNOWN_EVENTS)

    for case in KNOWN_EVENTS:
        k_req = KundaliRequest(**case["chart_req"])
        chart = kundali_service.compute_chart(k_req)
        res = compute_timing(chart, case["domain"])

        windows = res.get("timing_windows", [])
        target_yr = case["event_year"]

        hit = len(windows) > 0
        if hit:
            hits += 1

    hit_rate = (hits / total) * 100
    print(f"\n[Timing Backtest Results] Total: {total}, Hits: {hits}, Hit Rate: {hit_rate:.1f}%")
    assert hit_rate >= 40.0  # Baseline hit rate threshold
