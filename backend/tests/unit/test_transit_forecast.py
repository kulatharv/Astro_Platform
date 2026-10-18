"""Unit tests for future transit forecasting and Dasha chain expansion."""

import pytest
from datetime import datetime
from shared.cache.redis_client import CacheService
from modules.kundali.dasha import generate_dasha_chain, compute_pratyantardasha
from modules.prediction.transit_forecast import (
    compute_transit_aspects,
    is_sade_sati_active,
    compute_ingress_windows,
    compute_transit_forecast,
)

SAMPLE_CHART = {
    "basic_details": {
        "lagna": "Mesha",
        "moon_sign": "Vrishabha",
    },
    "dasha": {
        "current_mahadasha": "Jupiter",
    }
}


def test_dasha_chain_pratyantardasha():
    ad_start = datetime(2025, 1, 1)
    ad_end = datetime(2027, 1, 1)
    pds = compute_pratyantardasha("Jupiter", "Saturn", ad_start, ad_end)

    assert len(pds) == 9
    assert pds[0]["md_lord"] == "Jupiter"
    assert pds[0]["ad_lord"] == "Saturn"
    assert pds[0]["pd_lord"] == "Saturn"  # Self PD first


def test_compute_transit_aspects():
    # Jupiter in 1st house aspects 5th, 7th, 9th
    jup_aspects = compute_transit_aspects("Jupiter", 1)
    assert jup_aspects == [5, 7, 9]

    # Saturn in 1st house aspects 3rd, 7th, 10th
    sat_aspects = compute_transit_aspects("Saturn", 1)
    assert sat_aspects == [3, 7, 10]


def test_sade_sati_detection():
    # Moon in Vrishabha (Taurus, idx 1)
    # Saturn in Mesha (Aries, idx 0) -> 12th from Moon -> Rising
    ss_rising = is_sade_sati_active("Mesha", "Vrishabha")
    assert ss_rising["active"] is True
    assert "Rising" in ss_rising["phase"]

    # Saturn in Vrishabha -> Peak
    ss_peak = is_sade_sati_active("Vrishabha", "Vrishabha")
    assert ss_peak["active"] is True
    assert "Peak" in ss_peak["phase"]

    # Saturn in Mithuna -> Setting
    ss_setting = is_sade_sati_active("Mithuna", "Vrishabha")
    assert ss_setting["active"] is True
    assert "Setting" in ss_setting["phase"]

    # Saturn in Karka -> Not active
    ss_none = is_sade_sati_active("Karka", "Vrishabha")
    assert ss_none["active"] is False


def test_compute_transit_forecast_and_caching():
    CacheService.clear()
    dt = datetime(2026, 1, 1)
    fc1 = compute_transit_forecast(SAMPLE_CHART, start_date=dt, num_years=5)

    assert fc1["num_years"] == 5
    assert len(fc1["jupiter_ingress"]) > 0
    assert len(fc1["saturn_ingress"]) > 0

    # Second call should be cache hit
    fc2 = compute_transit_forecast(SAMPLE_CHART, start_date=dt, num_years=5)
    assert fc1 == fc2
