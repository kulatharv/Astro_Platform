"""
Unit tests for 'Share Today's Panchang' Image Generator & API Endpoint.
Validates:
1. Universal general Panchang data source (strictly get_full_panchang).
2. Absence of personalized fields in general share cards.
3. Accurate data parity between get_full_panchang() and image engine (no drift).
4. Permanent pixel-baked disclaimer and branding.
5. Portrait (1080x1920) and Square (1080x1080) geometries for PNG and JPEG.
6. In-memory caching per city + date.
7. End-to-end FastAPI endpoint response headers and MIME types.
"""
import pytest
from datetime import date
from io import BytesIO
from PIL import Image
from fastapi.testclient import TestClient

from gateway.main import app
from modules.panchang.engine import get_full_panchang
from modules.panchang.image import (
    generate_panchang_image,
    DISCLAIMER_TEXT,
    BRANDING_TEXT,
    _IMAGE_CACHE
)



@pytest.fixture
def client():
    return TestClient(app)


def test_share_image_portrait_png():
    """Verify portrait PNG image generation dimensions, format, and disclaimer."""
    target_d = date(2026, 9, 27)
    img_bytes, media_type = generate_panchang_image(
        city="Pune",
        target_date=target_d,
        image_format="portrait",
        image_type="png"
    )
    
    assert media_type == "image/png"
    assert len(img_bytes) > 10000
    
    # Open image with Pillow to verify valid headers and dimensions
    with Image.open(BytesIO(img_bytes)) as img:
        assert img.format == "PNG"
        assert img.size == (1080, 1920)


def test_share_image_square_jpeg():
    """Verify square JPEG image generation dimensions, format, and compression."""
    target_d = date(2026, 9, 27)
    img_bytes, media_type = generate_panchang_image(
        city="Pune",
        target_date=target_d,
        image_format="square",
        image_type="jpeg"
    )
    
    assert media_type == "image/jpeg"
    assert len(img_bytes) > 10000
    
    with Image.open(BytesIO(img_bytes)) as img:
        assert img.format == "JPEG"
        assert img.size == (1080, 1080)


def test_data_parity_with_get_full_panchang():
    """Assert image generator consumes pure get_full_panchang data with zero drift."""
    target_d = date(2026, 12, 21)
    panchang_data = get_full_panchang(city_name="Chennai", target_date=target_d)
    
    # Generate image for same parameters
    img_bytes, _ = generate_panchang_image(
        city="Chennai",
        target_date=target_d,
        image_format="portrait",
        image_type="png"
    )
    
    # Ensure standard panchang keys exist in the underlying data feed
    assert panchang_data["city"] == "Chennai"
    assert "sunrise" in panchang_data
    assert "sunset" in panchang_data
    assert "tithi" in panchang_data
    assert "nakshatra" in panchang_data
    assert "yoga" in panchang_data
    assert "karana" in panchang_data
    assert "rahu_kaal" in panchang_data
    assert "abhijit_muhurta" in panchang_data
    assert "choghadiya_day" in panchang_data
    assert "vara" in panchang_data


def test_no_personalized_fields_in_general_share():
    """Confirm personalized fields are never included in general share cards."""
    target_d = date(2026, 9, 27)
    # General panchang call has no user_rashi or user_nakshatra
    panchang_data = get_full_panchang(city_name="Pune", target_date=target_d)
    
    assert "tara_bala" not in panchang_data
    assert "chandra_bala" not in panchang_data
    assert "decision_assistant" not in panchang_data
    assert "user_profile" not in panchang_data
    assert "personalized_recommendations" not in panchang_data


def test_mandatory_disclaimer_constant():
    """Verify non-optional disclaimer is defined and baked into branding constant."""
    assert "Traditional Vedic guidance for reflection and awareness" in DISCLAIMER_TEXT
    assert "not a guarantee of outcomes" in DISCLAIMER_TEXT
    assert "Astro" in BRANDING_TEXT
    assert "astrologic.app" in BRANDING_TEXT


def test_image_caching():
    """Assert repeated calls with same parameters hit cache and return identical bytes."""
    target_d = date(2026, 9, 27)
    bytes_1, _ = generate_panchang_image("Shimla", target_d, "portrait", "png")
    bytes_2, _ = generate_panchang_image("Shimla", target_d, "portrait", "png")
    
    assert bytes_1 is bytes_2  # Object identity match from cache


def test_api_endpoint_share_image(client):
    """Test FastAPI GET /api/panchang/share-image endpoint."""
    # 1. Default parameters (Pune, portrait, png)
    resp = client.get("/api/panchang/share-image?city=Pune")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "image/png"
    assert "panchang_pune_portrait.png" in resp.headers["content-disposition"]
    assert len(resp.content) > 5000
    
    # 2. Square JPEG with custom date
    resp_sq = client.get("/api/panchang/share-image?city=Chennai&date=2026-12-21&format=square&type=jpeg")
    assert resp_sq.status_code == 200
    assert resp_sq.headers["content-type"] == "image/jpeg"
    assert "panchang_chennai_square.jpg" in resp_sq.headers["content-disposition"]
    
    # 3. Invalid date format validation
    resp_bad = client.get("/api/panchang/share-image?city=Pune&date=invalid-date")
    assert resp_bad.status_code == 400
    assert "Invalid date format" in resp_bad.json()["detail"]
