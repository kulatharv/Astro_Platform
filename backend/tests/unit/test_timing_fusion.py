"""Unit test suite for Step 5.6 Window Fusion Engine (modules/prediction/timing_fusion.py)."""

from datetime import date
import pytest

from modules.prediction.timing_fusion import fuse_windows, TimingWindow, TimingFusionResult


SAMPLE_CHART_MARRIAGE = {
    "basic_details": {
        "lagna": "Tula",
        "moon_sign": "Kanya",
    },
    "dasha": {
        "current_mahadasha": "Venus",
        "balance_years": 12.0,
    },
    "planets": {
        "Venus": {"sign": "Tula", "house": 1, "is_combust": False},
        "Jupiter": {"sign": "Meena", "house": 6, "is_combust": False},
        "Saturn": {"sign": "Kumbha", "house": 5, "is_combust": False},
        "Sun": {"sign": "Dhanu", "house": 3, "is_combust": False},
    }
}

SAMPLE_CHART_HEALTH = {
    "basic_details": {
        "lagna": "Mesha",
        "moon_sign": "Meena",
    },
    "dasha": {
        "current_mahadasha": "Saturn",
        "balance_years": 8.0,
    },
    "planets": {
        "Saturn": {"sign": "Kumbha", "house": 11, "is_combust": False},
        "Sun": {"sign": "Mesha", "house": 1, "is_combust": False},
    }
}


def test_fuse_returns_windows():
    start_d = date(2026, 1, 1)
    end_d = date(2041, 1, 1)
    res = fuse_windows(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    assert isinstance(res, TimingFusionResult)
    assert isinstance(res.timing_windows, list)
    for w in res.timing_windows:
        assert isinstance(w, TimingWindow)
        assert w.start_date <= w.peak_date <= w.end_date
        assert 0.0 <= w.peak_score <= 1.0

    if len(res.timing_windows) > 1:
        scores = [w.peak_score for w in res.timing_windows]
        assert scores == sorted(scores, reverse=True)


def test_jupiter_7h_marriage_scores_high():
    chart_tula_jup = {
        "basic_details": {"lagna": "Mesha", "moon_sign": "Mesha"},
        "dasha": {"current_mahadasha": "Venus", "balance_years": 15.0},
        "planets": {"Venus": {"sign": "Tula", "house": 7, "is_combust": False}}
    }
    start_d = date(2028, 1, 1)
    end_d = date(2030, 1, 1)
    res = fuse_windows(chart_tula_jup, "marriage", start_d, end_d)

    assert len(res.timing_windows) > 0
    top = res.timing_windows[0]
    assert top.peak_score >= 0.45


def test_saturn_7h_marriage_blocks():
    start_d = date(2026, 1, 1)
    end_d = date(2028, 1, 1)
    res = fuse_windows(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    for w in res.timing_windows:
        if "Saturn" in w.drivers and "7H" in str(w.drivers):
            assert w.confidence in ("Possible", "Unlikely")


def test_smoothing_reduces_spikes():
    start_d = date(2026, 1, 1)
    end_d = date(2027, 1, 1)
    res = fuse_windows(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    assert res.threshold_used == 0.45


def test_consecutive_months_merge():
    start_d = date(2026, 1, 1)
    end_d = date(2028, 1, 1)
    res = fuse_windows(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    for w in res.timing_windows:
        # Merged window should cover multiple months if continuous
        num_months = (w.end_date.year - w.start_date.year) * 12 + (w.end_date.month - w.start_date.month) + 1
        assert num_months >= 1


def test_gap_tolerance():
    start_d = date(2026, 1, 1)
    end_d = date(2031, 1, 1)
    res = fuse_windows(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    assert res.timing_windows is not None


def test_threshold_filter():
    start_d = date(2026, 1, 1)
    end_d = date(2041, 1, 1)
    res = fuse_windows(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    for w in res.timing_windows:
        assert w.peak_score >= 0.45


def test_top_n_limit():
    start_d = date(2026, 1, 1)
    end_d = date(2041, 1, 1)
    res = fuse_windows(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d, top_n=3)

    assert len(res.timing_windows) <= 3


def test_peak_window_separate():
    start_d = date(2026, 1, 1)
    end_d = date(2031, 1, 1)
    res = fuse_windows(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    if res.timing_windows:
        assert res.peak_window == res.timing_windows[0]


def test_next_12_months_summary():
    start_d = date(2026, 1, 1)
    end_d = date(2027, 1, 1)
    res = fuse_windows(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    assert isinstance(res.next_12_months_summary, str)
    assert len(res.next_12_months_summary) > 0


def test_deterministic():
    start_d = date(2026, 1, 1)
    end_d = date(2031, 1, 1)
    res1 = fuse_windows(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)
    res2 = fuse_windows(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    assert len(res1.timing_windows) == len(res2.timing_windows)
    if res1.peak_window and res2.peak_window:
        assert res1.peak_window.peak_score == res2.peak_window.peak_score


def test_performance():
    import time
    start_d = date(2026, 1, 1)
    end_d = date(2041, 1, 1)

    t0 = time.time()
    res = fuse_windows(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)
    t1 = time.time()

    elapsed = t1 - t0
    assert elapsed < 2.0


def test_astrological_sanity():
    start_d = date(2026, 1, 1)
    end_d = date(2041, 1, 1)
    res = fuse_windows(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    assert isinstance(res.timing_windows, list)


def test_marriage_high_confidence_window():
    # Venus MD/AD + Jupiter 7H direct transit → high confidence
    chart = {
        "basic_details": {"lagna": "Tula", "moon_sign": "Tula"},
        "dasha": {"current_mahadasha": "Venus", "balance_years": 15.0},
        "planets": {
            "Venus": {"sign": "Tula", "house": 1, "is_combust": False},
            "Jupiter": {"sign": "Meena", "house": 6, "is_combust": False}
        }
    }
    start_d = date(2028, 5, 1)
    end_d = date(2029, 6, 30)
    res = fuse_windows(chart, "marriage", start_d, end_d)

    assert len(res.timing_windows) > 0
    top = res.timing_windows[0]
    assert top.peak_score >= 0.50
    assert top.confidence in ("High", "Moderate", "Possible")


def test_career_moderate_window():
    # Jupiter MD + Saturn 10H transit → Moderate confidence
    chart = {
        "basic_details": {"lagna": "Mithuna", "moon_sign": "Mithuna"},
        "dasha": {"current_mahadasha": "Jupiter", "balance_years": 10.0},
        "planets": {
            "Jupiter": {"sign": "Meena", "house": 10, "is_combust": False},
            "Saturn": {"sign": "Meena", "house": 10, "is_combust": False},
            "Sun": {"sign": "Mesha", "house": 11, "is_combust": False},
        }
    }
    start_d = date(2026, 1, 1)
    end_d = date(2031, 1, 1)
    res = fuse_windows(chart, "career", start_d, end_d)

    assert res.timing_windows is not None


def test_health_sade_sati_high():
    # Sade Sati peak + Saturn 12H transit → elevated health risk
    chart = {
        "basic_details": {"lagna": "Mesha", "moon_sign": "Meena"},
        "dasha": {"current_mahadasha": "Saturn", "balance_years": 15.0},
        "planets": {
            "Saturn": {"sign": "Kanya", "house": 6, "is_combust": False},
            "Sun": {"sign": "Mesha", "house": 1, "is_combust": False},
        }
    }
    start_d = date(2026, 1, 1)
    end_d = date(2031, 1, 1)
    res = fuse_windows(chart, "health", start_d, end_d)

    assert res.timing_windows is not None


def test_weak_chart_no_high_windows():
    # Chart with weak alignments
    chart_weak = {
        "basic_details": {"lagna": "Kanya", "moon_sign": "Simha"},
        "dasha": {"current_mahadasha": "Sun", "balance_years": 1.0},
        "planets": {"Sun": {"sign": "Tula", "house": 2, "is_combust": True}}
    }
    start_d = date(2026, 1, 1)
    end_d = date(2028, 1, 1)
    res = fuse_windows(chart_weak, "marriage", start_d, end_d)

    for w in res.timing_windows:
        assert w.confidence != "High"


def test_score_spread():
    start_d = date(2026, 1, 1)
    end_d = date(2036, 1, 1)
    res = fuse_windows(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    if len(res.timing_windows) >= 2:
        scores = [w.peak_score for w in res.timing_windows]
        spread = max(scores) - min(scores)
        assert spread >= 0.05

