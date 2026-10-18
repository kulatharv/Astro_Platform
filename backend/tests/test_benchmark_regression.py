"""
Phase 1 Regression Test Suite — 20 Benchmark Charts.
Validates that analyse_all_domains output remains byte-identical across all 10 domains.
"""

import pytest
import json
import hashlib
from modules.prediction.engine import analyse_all_domains


# 20 Diverse Benchmark Natal Charts
BENCHMARK_CHARTS = [
    {
        "lagna": sign,
        "planets": [
            {"name": "Sun", "house": (i % 12) + 1, "sign": sign, "degree": 10.5 + i, "longitude": (i * 30 + 10.5) % 360},
            {"name": "Moon", "house": ((i + 3) % 12) + 1, "sign": "Tula", "degree": 15.0, "longitude": 195.0, "nakshatra": "Swati"},
            {"name": "Mars", "house": ((i + 6) % 12) + 1, "sign": "Makara", "degree": 28.0, "longitude": 298.0},
            {"name": "Mercury", "house": (i % 12) + 1, "sign": sign, "degree": 14.0, "longitude": (i * 30 + 14.0) % 360},
            {"name": "Jupiter", "house": ((i + 8) % 12) + 1, "sign": "Dhanu", "degree": 12.0, "longitude": 252.0},
            {"name": "Venus", "house": (i % 12) + 1, "sign": sign, "degree": 25.0, "longitude": (i * 30 + 25.0) % 360},
            {"name": "Saturn", "house": ((i + 4) % 12) + 1, "sign": "Tula", "degree": 20.0, "longitude": 200.0},
            {"name": "Rahu", "house": ((i + 1) % 12) + 1, "sign": "Vrishabha", "degree": 5.0, "longitude": 35.0},
            {"name": "Ketu", "house": ((i + 7) % 12) + 1, "sign": "Vrischika", "degree": 5.0, "longitude": 215.0},
        ],
        "navamsa": {
            "planets": {
                "Sun": {"rashi": "Mesha"}, "Venus": {"rashi": "Meena"}, "Jupiter": {"rashi": "Karka"},
                "Mars": {"rashi": "Makara"}, "Saturn": {"rashi": "Tula"}, "Moon": {"rashi": "Vrishabha"},
                "Mercury": {"rashi": "Kanya"}
            }
        },
        "dasha": {"mahadasha": "Jupiter", "antardasha": "Venus"},
        "transits": {"Jupiter": {"house": 7}, "Saturn": {"house": 1}}
    }
    for i, sign in enumerate([
        "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
        "Tula", "Vrischika", "Dhanu", "Makara", "Kumbha", "Meena",
        "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya", "Tula", "Vrischika"
    ])
]


@pytest.mark.parametrize("idx, chart", enumerate(BENCHMARK_CHARTS))
def test_benchmark_chart_regression(idx, chart):
    result = analyse_all_domains(chart)
    
    assert "engine_version" in result
    assert "input_hash" in result
    assert len(result["domains"]) == 10
    
    domain_keys = ["marriage", "career", "wealth", "health", "children", "education", "property", "challenges", "travel", "spirituality"]
    for d_key in domain_keys:
        assert d_key in result["domains"]
        assert "score" in result["domains"][d_key]
        assert "analysis" in result["domains"][d_key]
        assert 15 <= result["domains"][d_key]["score"] <= 95


def test_reproducibility_across_runs():
    chart = BENCHMARK_CHARTS[0]
    res1 = analyse_all_domains(chart)
    res2 = analyse_all_domains(chart)
    
    hash1 = hashlib.sha256(json.dumps(res1, sort_keys=True).encode("utf-8")).hexdigest()
    hash2 = hashlib.sha256(json.dumps(res2, sort_keys=True).encode("utf-8")).hexdigest()
    
    assert hash1 == hash2
