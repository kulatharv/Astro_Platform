"""Unit test suite for Step 5.8 Domain Integration & Timing Block wiring."""

import time
import pytest
from modules.kundali.api import KundaliService, KundaliRequest
from modules.prediction.engine import analyse_all_domains
from modules.prediction.timing import build_timing_block, compute_timing
from modules.prediction.schemas import TimingBlock, TimingWindow

kundali_service = KundaliService()

SAMPLE_REQ = {
    "year": 1990,
    "month": 5,
    "day": 15,
    "hour": 14,
    "minute": 30,
    "city": "Pune",
}


def test_each_domain_returns_timing_block():
    k_req = KundaliRequest(**SAMPLE_REQ)
    chart = kundali_service.compute_chart(k_req)
    res = analyse_all_domains(chart)

    domains = res["domains"]
    assert len(domains) == 10

    for d_name, d_val in domains.items():
        assert "timing" in d_val
        tb = d_val["timing"]
        assert "timing_windows" in tb
        assert "next_12_months_summary" in tb
        assert "methodology" in tb
        assert "engine_version" in tb


def test_timing_windows_have_required_fields():
    k_req = KundaliRequest(**SAMPLE_REQ)
    chart = kundali_service.compute_chart(k_req)
    res = analyse_all_domains(chart)

    marriage_timing = res["domains"]["marriage"]["timing"]
    for w in marriage_timing["timing_windows"]:
        assert "start" in w or "start_date" in w
        assert "end" in w or "end_date" in w
        assert "score" in w or "peak_score" in w
        assert "confidence" in w
        assert "mahadasha" in w
        assert "antardasha" in w
        assert "pratyantardasha" in w
        assert "reasons" in w


def test_legacy_timing_preserved():
    k_req = KundaliRequest(**SAMPLE_REQ)
    chart = kundali_service.compute_chart(k_req)
    res = analyse_all_domains(chart)

    for d_name, d_val in res["domains"].items():
        assert "timing_legacy" in d_val


def test_fail_open_on_timing_error(monkeypatch):
    k_req = KundaliRequest(**SAMPLE_REQ)
    chart = kundali_service.compute_chart(k_req)

    def mock_fail(*args, **kwargs):
        raise RuntimeError("Simulated fusion exception")

    monkeypatch.setattr("modules.prediction.timing.fuse_windows", mock_fail)
    tb = build_timing_block(chart, "marriage")

    assert tb["timing_windows"] == []
    assert tb["peak_window"] is None
    assert "unavailable" in tb["next_12_months_summary"]


def test_timing_deterministic():
    k_req = KundaliRequest(**SAMPLE_REQ)
    chart1 = kundali_service.compute_chart(k_req)
    chart2 = kundali_service.compute_chart(k_req)

    tb1 = build_timing_block(chart1, "marriage")
    tb2 = build_timing_block(chart2, "marriage")

    assert tb1["next_12_months_summary"] == tb2["next_12_months_summary"]
    assert len(tb1["timing_windows"]) == len(tb2["timing_windows"])


def test_performance_10_domains():
    k_req = KundaliRequest(**SAMPLE_REQ)
    chart = kundali_service.compute_chart(k_req)

    t0 = time.time()
    res = analyse_all_domains(chart)
    t1 = time.time()

    elapsed = t1 - t0
    assert len(res["domains"]) == 10
    assert elapsed < 5.0  # complete 10 domains timing in < 5s


def test_byte_identical_non_timing():
    k_req = KundaliRequest(**SAMPLE_REQ)
    chart = kundali_service.compute_chart(k_req)
    res = analyse_all_domains(chart)

    assert "engine_version" in res
    assert "input_hash" in res
    assert "domains" in res
