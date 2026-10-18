"""Unit tests for modules/prediction/timing_dasha.py."""

import time
import pytest
from datetime import date
from modules.prediction.timing_dasha import score_dasha_periods, ScoredPeriod

SAMPLE_CHART_MARRIAGE = {
    "lagna": "Tula",
    "planets": [
        {"name": "Venus", "sign": "Tula", "house": 1, "degree": 12.5},
        {"name": "Jupiter", "sign": "Mesha", "house": 7, "degree": 15.0},
        {"name": "Sun", "sign": "Simha", "house": 11, "degree": 22.0},
        {"name": "Saturn", "sign": "Kumbha", "house": 5, "degree": 8.0},
    ],
    "dasha": {
        "current_mahadasha": "Venus",
        "balance_years": 15.0,
    }
}

SAMPLE_CHART_CAREER_COMBUST = {
    "lagna": "Mesha",
    "planets": [
        {"name": "Sun", "sign": "Tula", "house": 7, "degree": 10.0},  # Debilitated Sun in 7th
        {"name": "Saturn", "sign": "Karka", "house": 4, "degree": 5.0},
    ],
    "dasha": {
        "current_mahadasha": "Sun",
        "balance_years": 5.0,
    }
}


def test_score_returns_periods():
    start_d = date(2026, 1, 1)
    end_d = date(2031, 1, 1)
    periods = score_dasha_periods(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    assert isinstance(periods, list)
    assert len(periods) > 0

    for p in periods:
        assert isinstance(p, ScoredPeriod)
        assert p.start_date >= start_d
        assert p.end_date <= end_d
        assert 0.0 <= p.score <= 1.0
        assert "md" in p.sub_scores
        assert "ad" in p.sub_scores
        assert "pd" in p.sub_scores


def test_karaka_md_scores_high():
    # Venus MD for Tula Lagna in 1st house for marriage
    start_d = date(2026, 1, 1)
    end_d = date(2028, 1, 1)
    periods = score_dasha_periods(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    assert len(periods) > 0
    top_period = max(periods, key=lambda p: p.score)
    assert top_period.score >= 0.70
    assert top_period.mahadasha_lord == "Venus"


def test_combust_md_scores_low():
    # Debilitated Sun MD for career
    start_d = date(2026, 1, 1)
    end_d = date(2027, 1, 1)
    periods = score_dasha_periods(SAMPLE_CHART_CAREER_COMBUST, "career", start_d, end_d)

    assert len(periods) > 0
    top_period = max(periods, key=lambda p: p.score)
    assert top_period.score <= 0.50


def test_functional_benefic_boost():
    # Venus is functional benefic for Tula Lagna vs Sun for Mesha Lagna
    start_d = date(2026, 1, 1)
    end_d = date(2027, 1, 1)
    periods_tula = score_dasha_periods(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)
    assert periods_tula[0].sub_scores["md"] > 0.50


def test_reasons_are_readable():
    start_d = date(2026, 1, 1)
    end_d = date(2027, 1, 1)
    periods = score_dasha_periods(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    for p in periods:
        assert len(p.reasons) > 0
        for r in p.reasons:
            assert isinstance(r, str)
            assert len(r.strip()) > 0
            # Ensure readable prose
            assert "_" not in r or "7H" in r or "10H" in r


def test_saturn_7h_block_applies():
    chart_saturn = {
        "lagna": "Mesha",
        "planets": [{"name": "Saturn", "sign": "Tula", "house": 7, "degree": 10.0}],
        "dasha": {"current_mahadasha": "Saturn", "balance_years": 10.0},
    }
    start_d = date(2026, 1, 1)
    end_d = date(2027, 1, 1)
    periods = score_dasha_periods(chart_saturn, "marriage", start_d, end_d)

    assert len(periods) > 0
    has_block_reason = any("Saturn MD/AD applies 7H block multiplier" in r for r in periods[0].reasons)
    assert has_block_reason is True


def test_deterministic():
    start_d = date(2026, 1, 1)
    end_d = date(2031, 1, 1)
    res1 = score_dasha_periods(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)
    res2 = score_dasha_periods(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    assert len(res1) == len(res2)
    for p1, p2 in zip(res1, res2):
        assert p1.score == p2.score
        assert p1.start_date == p2.start_date
        assert p1.reasons == p2.reasons


def test_performance():
    start_d = date(2026, 1, 1)
    end_d = date(2041, 1, 1)  # 15-year horizon

    t0 = time.time()
    periods = score_dasha_periods(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)
    elapsed_ms = (time.time() - t0) * 1000

    assert len(periods) > 0
    assert elapsed_ms < 500  # Must complete in under 500ms
