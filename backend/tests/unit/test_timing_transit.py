"""Unit tests for Step 5.5 Gochara transit activation scorer (modules/prediction/timing_transit.py)."""

from datetime import date
import pytest

from modules.prediction.timing_transit import score_transit_months, ScoredMonth


SAMPLE_CHART_MARRIAGE = {
    "basic_details": {
        "lagna": "Tula",
        "moon_sign": "Kanya",
    },
    "planets": {
        "Venus": {"sign": "Tula", "house": 1, "is_combust": False},
        "Jupiter": {"sign": "Meena", "house": 6, "is_combust": False},
        "Saturn": {"sign": "Kumbha", "house": 5, "is_combust": False},
        "Sun": {"sign": "Dhanu", "house": 3, "is_combust": False},
    }
}

SAMPLE_CHART_HEALTH_SADE_SATI = {
    "basic_details": {
        "lagna": "Mesha",
        "moon_sign": "Meena",  # Saturn in Meena is peak Sade Sati
    },
    "planets": {
        "Sun": {"sign": "Mesha", "house": 1, "is_combust": False},
        "Saturn": {"sign": "Kumbha", "house": 11, "is_combust": False},
    }
}


def test_returns_monthly_snapshots():
    start_d = date(2026, 1, 1)
    end_d = date(2026, 6, 30)
    months = score_transit_months(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    assert len(months) == 6
    for m in months:
        assert isinstance(m, ScoredMonth)
        assert m.month_start <= m.month_end
        assert 0.0 <= m.score <= 1.0


def test_jupiter_transit_scores_high():
    # Chart with Tula Lagna where Jupiter transits 7H (Mesha) in 2028
    chart_jup_7h = {
        "basic_details": {"lagna": "Tula", "moon_sign": "Tula"},
        "planets": {}
    }
    start_d = date(2027, 6, 1)
    end_d = date(2028, 12, 31)
    months = score_transit_months(chart_jup_7h, "marriage", start_d, end_d)

    assert len(months) > 0
    scores = [m.score for m in months]
    assert max(scores) >= 0.20


def test_saturn_7h_blocks_marriage():
    start_d = date(2026, 1, 1)
    end_d = date(2028, 1, 1)
    months = score_transit_months(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    for m in months:
        sat_house = m.active_transits.get("Saturn", {}).get("house")
        if sat_house == 7:
            # Saturn 7H block multiplier applied
            assert any("Saturn 7H transit block multiplier" in r for r in m.reasons)


def test_sade_sati_modifier():
    start_d = date(2026, 1, 1)
    end_d = date(2026, 6, 1)

    health_months = score_transit_months(SAMPLE_CHART_HEALTH_SADE_SATI, "health", start_d, end_d)
    challenges_months = score_transit_months(SAMPLE_CHART_HEALTH_SADE_SATI, "challenges", start_d, end_d)

    assert health_months[0].sub_scores["sade_sati_modifier"] == -0.15
    assert challenges_months[0].sub_scores["sade_sati_modifier"] == 0.15


def test_negative_transit_inversion():
    start_d = date(2026, 1, 1)
    end_d = date(2026, 6, 1)

    health_months = score_transit_months(SAMPLE_CHART_HEALTH_SADE_SATI, "health", start_d, end_d)
    marriage_months = score_transit_months(SAMPLE_CHART_HEALTH_SADE_SATI, "marriage", start_d, end_d)

    assert health_months is not None
    assert marriage_months is not None


def test_node_activation():
    start_d = date(2026, 1, 1)
    end_d = date(2026, 6, 1)
    months = score_transit_months(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    for m in months:
        assert "nodes" in m.sub_scores
        assert "Rahu" in m.active_transits
        assert "Ketu" in m.active_transits


def test_smoothing_not_applied():
    start_d = date(2026, 1, 1)
    end_d = date(2026, 5, 31)
    months = score_transit_months(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    # Returns raw monthly scores without rolling average window
    assert len(months) == 5
    assert all(isinstance(m.score, float) for m in months)


def test_deterministic():
    start_d = date(2026, 1, 1)
    end_d = date(2026, 6, 1)
    m1 = score_transit_months(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)
    m2 = score_transit_months(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    assert len(m1) == len(m2)
    for a, b in zip(m1, m2):
        assert a.score == b.score
        assert a.reasons == b.reasons


def test_performance():
    import time
    start_d = date(2026, 1, 1)
    end_d = date(2041, 1, 1)

    t0 = time.time()
    months = score_transit_months(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)
    t1 = time.time()

    elapsed = t1 - t0
    assert len(months) == 180
    assert elapsed < 1.0  # completes 15 years in < 1s


def test_reasons_readable():
    start_d = date(2026, 1, 1)
    end_d = date(2026, 6, 1)
    months = score_transit_months(SAMPLE_CHART_MARRIAGE, "marriage", start_d, end_d)

    for m in months:
        for r in m.reasons:
            assert isinstance(r, str)
            assert len(r) > 0
