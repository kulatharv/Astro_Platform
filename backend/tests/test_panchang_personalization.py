"""
Test Suite for Personalized Vedic Decision Engine.
Tests:
- Tara Bala calculation across all 9 categories.
- Chandra Bala house distance computation.
- Category scores generation.
- Decision Assistant rule evaluation.
- Natal Moon derivation from birth parameters.
- API endpoints for personalization, profile resolution, and decision.
- Backward compatibility (General mode works without profile).
"""

import pytest
from datetime import date
from fastapi.testclient import TestClient

from gateway.main import app
from modules.panchang.personalization import (
    calculate_tara_bala,
    calculate_chandra_bala,
    calculate_category_scores,
    evaluate_decision,
    derive_natal_moon
)
from modules.panchang.engine import get_full_panchang



@pytest.fixture
def client():
    return TestClient(app)


# ── Tara Bala Tests ──────────────────────────────────────────

def test_tara_bala_sampat():
    """Ashwini(0) -> Bharani(1): count=2, tara=2 => Sampat."""
    res = calculate_tara_bala("Ashwini", "Bharani")
    assert res["tara_number"] == 2
    assert res["tara_name"] == "Sampat"
    assert res["is_auspicious"] is True
    assert res["score_mod"] > 0


def test_tara_bala_vipat():
    """Ashwini(0) -> Krittika(2): count=3, tara=3 => Vipat."""
    res = calculate_tara_bala("Ashwini", "Krittika")
    assert res["tara_number"] == 3
    assert res["tara_name"] == "Vipat"
    assert res["is_auspicious"] is False


def test_tara_bala_janma():
    """Same nakshatra: count=1, tara=1 => Janma."""
    res = calculate_tara_bala("Pushya", "Pushya")
    assert res["tara_number"] == 1
    assert res["tara_name"] == "Janma"


def test_tara_bala_wraps_around_27():
    """Revati(26) -> Ashwini(0): count=2, tara=2 => Sampat."""
    res = calculate_tara_bala("Revati", "Ashwini")
    assert res["tara_number"] == 2
    assert res["tara_name"] == "Sampat"


def test_tara_bala_invalid_nakshatra():
    """Invalid nakshatra should return a safe fallback."""
    res = calculate_tara_bala("InvalidNak", "AlsoInvalid")
    assert "tara_name" in res
    assert res["is_auspicious"] is True  # Safe fallback


# ── Chandra Bala Tests ───────────────────────────────────────

def test_chandra_bala_same_sign():
    """Same sign => 1st house => Auspicious."""
    res = calculate_chandra_bala("Mesha", "Mesha")
    assert res["house_distance"] == 1
    assert res["is_auspicious"] is True


def test_chandra_bala_8th_house():
    """8th house transit => Ashtama Chandra => Inauspicious."""
    # Mesha(0) -> Vrischika(7): distance = 8
    res = calculate_chandra_bala("Mesha", "Vrischika")
    assert res["house_distance"] == 8
    assert res["is_auspicious"] is False
    assert "Ashtama" in res["status"]


def test_chandra_bala_11th_house():
    """11th house transit => Labha => Auspicious."""
    # Mesha(0) -> Kumbha(10): distance = 11
    res = calculate_chandra_bala("Mesha", "Kumbha")
    assert res["house_distance"] == 11
    assert res["is_auspicious"] is True


# ── Category Scores Tests ────────────────────────────────────

def test_category_scores_range():
    """All scores should be between 1.0 and 10.0."""
    tara = {"score_mod": 1.5, "tara_name": "Sampat"}
    chandra = {"score_mod": 1.0, "house_distance": 11}
    scores = calculate_category_scores(tara, chandra, 7.0, "Jupiter", True)

    for key in ("career", "finance", "relationships", "health", "spiritual"):
        assert key in scores
        assert 1.0 <= scores[key] <= 10.0


# ── Decision Assistant Tests ─────────────────────────────────

def test_decision_investment():
    """Test investment decision with favorable conditions."""
    panchang = get_full_panchang("Pune")
    res = evaluate_decision("investment", "Vrishabha", "Rohini", panchang)

    assert "recommendation" in res
    assert res["recommendation"] in ("FAVORABLE", "MIXED SIGNALS", "REFLECT")
    assert "reasons" in res
    assert "cautions" in res
    assert 0 < (res.get("alignment_strength") or res.get("confidence", 0.9)) <= 1.0
    assert "next_best_time" in res


def test_decision_travel():
    """Test travel decision evaluation."""
    panchang = get_full_panchang("Pune")
    res = evaluate_decision("travel", "Simha", "Magha", panchang)
    assert res["activity"] == "Travel & Journeys"
    assert res["recommendation"] in ("FAVORABLE", "MIXED SIGNALS", "REFLECT")


def test_decision_spiritual():
    """Spiritual activities should return a valid recommendation."""
    panchang = get_full_panchang("Pune")
    res = evaluate_decision("spiritual puja", "Mesha", "Ashwini", panchang)
    assert res["activity"] == "Spiritual Puja & Sacred Rituals"
    assert res["recommendation"] in ("FAVORABLE", "MIXED SIGNALS", "REFLECT")


def test_decision_without_profile():
    """Decision should work even without user profile (general mode)."""
    panchang = get_full_panchang("Pune")
    res = evaluate_decision("meeting", None, None, panchang)
    assert res["recommendation"] in ("FAVORABLE", "MIXED SIGNALS", "REFLECT")
    assert res["alignment_strength"] < 0.9  # Lower alignment strength without profile


# ── Natal Moon Derivation Tests ──────────────────────────────

def test_derive_natal_moon():
    """Test natal Moon derivation for a known birth date."""
    result = derive_natal_moon(birth_date=date(1995, 5, 15), city_name="Pune")
    assert "rashi" in result
    assert "nakshatra" in result
    assert "nakshatra_pada" in result
    assert 1 <= result["nakshatra_pada"] <= 4
    assert result["birth_date"] == "1995-05-15"
    assert result["is_estimated_time"] is True
    assert "boundary_warning" in result
    assert "time_sensitivity_note" in result


def test_derive_natal_moon_with_exact_time():
    """Test natal Moon derivation with explicit birth time."""
    from datetime import time
    result = derive_natal_moon(birth_date=date(1995, 5, 15), birth_time=time(14, 30), city_name="Pune")
    assert result["is_estimated_time"] is False
    assert "time_sensitivity_note" in result
    assert "boundary_warning" in result


# ── API Endpoint Tests ───────────────────────────────────────

def test_api_general_mode_backward_compat(client):
    """General mode (no profile) should return standard response without personalization."""
    resp = client.post("/api/panchang", json={"city": "Pune"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["mode"] == "general"
    assert data.get("personalization") is None
    assert "today_score" in data
    assert "dos_and_donts" in data


def test_api_personalized_mode(client):
    """Personalized mode should include tara_bala, chandra_bala, category_scores."""
    resp = client.post("/api/panchang", json={
        "city": "Pune",
        "user_rashi": "Vrishabha",
        "user_nakshatra": "Rohini"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["mode"] == "personalized"
    assert data["personalization"] is not None

    p = data["personalization"]
    assert "tara_bala" in p
    assert "chandra_bala" in p
    assert "category_scores" in p
    assert "personalized_score" in p
    assert "personalized_advice" in p

    scores = p["category_scores"]
    for key in ("career", "finance", "relationships", "health", "spiritual"):
        assert 1.0 <= scores[key] <= 10.0


def test_api_resolve_profile(client):
    """Test profile resolution from birth parameters."""
    resp = client.post("/api/panchang/resolve-profile", json={
        "name": "Test User",
        "birth_date": "1995-05-15",
        "birth_time": "14:30",
        "birth_place": "Pune"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "rashi" in data
    assert "nakshatra" in data
    assert data["name"] == "Test User"


def test_api_decision_endpoint(client):
    """Test the interactive Decision Assistant endpoint."""
    resp = client.post("/api/panchang/decision", json={
        "activity": "investment",
        "city": "Pune",
        "user_rashi": "Vrishabha",
        "user_nakshatra": "Rohini"
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["recommendation"] in ("FAVORABLE", "MIXED SIGNALS", "REFLECT")
    assert "reasons" in data
    assert "next_best_time" in data
    assert 0 < data["alignment_strength"] <= 1.0


def test_worst_case_simultaneous_afflictions_clamped_to_min_score():
    """
    Worst-case stress test: Naidhana Tara (-2.5) + Ashtama Chandra (-2.0) +
    Rog/Kaal Choghadiya + Rahu Kaal simultaneously active.
    Asserts:
    1. Pre-clamp category scores plunge below 1.0 and are strictly clamped to 1.0.
    2. Decision recommendation evaluates strictly to 'REFLECT'.
    """
    # Natal: Ashwini (Nakshatra #1), Mesha (Rashi #1)
    # Transit: Punarvasu (Nakshatra #7 -> Naidhana Tara #7), Vrishchika (Rashi #8 -> 8th House Ashtama Chandra)
    tara = calculate_tara_bala(natal_nakshatra="Ashwini", transit_nakshatra="Punarvasu")
    assert tara["tara_number"] == 7
    assert tara["score_mod"] == -2.5

    chandra = calculate_chandra_bala(natal_rashi="Mesha", transit_rashi="Vrischika")
    assert chandra["house_distance"] == 8
    assert chandra["score_mod"] == -2.0

    # Low base score with simultaneous afflictions
    scores = calculate_category_scores(
        tara_bala=tara,
        chandra_bala=chandra,
        today_base_score=3.0,
        active_hora_planet="Saturn",
        active_chog_auspicious=False
    )
    # Check that health and other heavily hit categories are clamped to 1.0 minimum
    for cat, val in scores.items():
        assert 1.0 <= val <= 10.0
    assert scores["health"] == 1.0  # (3.0 - 1.6 - 1.0 - 1.0 - 1.2 = -2.8 -> clamped to 1.0)

    # Decision Assistant under worst-case scenario
    mock_panchang = {
        "nakshatra": "Punarvasu",
        "today_score": 3.0,
        "current_choghadiya": {"name": "Kaal", "is_auspicious": False, "score_mod": -1.5},
        "rahu_kaal": "04:30 PM - 06:00 PM",
        "planets": [{"name": "Chandra (Moon)", "sign": "Vrischika"}]
    }
    decision = evaluate_decision(
        activity_type="investment",
        user_rashi="Mesha",
        user_nakshatra="Ashwini",
        current_panchang=mock_panchang
    )
    assert decision["recommendation"] == "REFLECT"
    assert any("Naidhana" in c or "Obstacle" in c or "Ashtama" in c for c in decision.get("cautions", []))

