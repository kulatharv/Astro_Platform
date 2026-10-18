"""Integration tests for FastAPI endpoints."""

import uuid
import pytest
from fastapi.testclient import TestClient
from gateway.main import app


client = TestClient(app)


def get_auth_client():
    c = TestClient(app)
    uid = uuid.uuid4().hex[:8]
    c.post(
        "/signup",
        data={"name": f"Test User {uid}", "email": f"tester_{uid}@example.com", "password": "Password123!"},
    )
    return c


def test_get_cities():
    response = client.get("/api/cities")
    assert response.status_code == 200
    cities = response.json()
    assert isinstance(cities, list)
    assert "Pune" in cities
    assert "Mumbai" in cities


def test_generate_chart_endpoint():
    auth_client = get_auth_client()
    payload = {
        "name": "Test Seeker",
        "year": 1995,
        "month": 5,
        "day": 15,
        "hour": 14.5,
        "place": "Pune",
    }
    response = auth_client.post("/api/generate-chart", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "basic_details" in data
    assert "planets" in data


def test_kundali_endpoint():
    auth_client = get_auth_client()
    payload = {
        "year": 1990,
        "month": 7,
        "day": 22,
        "hour": 18,
        "minute": 30,
        "city": "Mumbai",
    }
    response = auth_client.post("/api/kundali", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "lagna" in data
    assert "planets" in data
    assert "scores" in data
    assert "yogas" in data
    assert "doshas" in data


def test_panchang_endpoint():
    response = client.post("/api/panchang", json={"city": "Delhi"})
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Delhi"
    assert "tithi" in data
    assert "nakshatra" in data


def test_daily_horoscope_endpoint():
    response = client.get("/api/daily-horoscope/aries")
    assert response.status_code == 200
    data = response.json()
    assert data["sign"] == "Aries"
    assert "horoscope" in data

    # Test invalid sign
    bad_resp = client.get("/api/daily-horoscope/unknownsign")
    assert bad_resp.status_code == 400


def test_horoscope_by_index():
    response = client.get("/api/horoscope/0")
    assert response.status_code == 200
    data = response.json()
    assert data["sign"] == "Aries"


def test_festivals_endpoints():
    today_resp = client.get("/api/festivals/today")
    assert today_resp.status_code == 200
    assert "festivals" in today_resp.json()

    upcoming_resp = client.get("/api/festivals/upcoming")
    assert upcoming_resp.status_code == 200
    assert "festivals" in upcoming_resp.json()


def test_prediction_and_chat():
    auth_client = get_auth_client()
    payload = {
        "year": 1995,
        "month": 5,
        "day": 15,
        "hour": 14.5,
        "city": "Pune",
    }
    pred_resp = auth_client.post("/api/prediction?sync=true", json=payload)
    assert pred_resp.status_code == 200
    data = pred_resp.json()
    assert "marriage_prediction" in data
    assert "career_prediction" in data

    # Test chat
    chat_resp = auth_client.post("/api/chat", json={"message": "How is my career progression?"})
    assert chat_resp.status_code == 200
    assert "reply" in chat_resp.json()


def test_kundali_chat_endpoint():
    auth_client = get_auth_client()
    k_payload = {
        "year": 1990,
        "month": 7,
        "day": 22,
        "hour": 18,
        "minute": 30,
        "city": "Mumbai",
    }
    k_resp = auth_client.post("/api/kundali", json=k_payload)
    chart = k_resp.json()

    chat_payload = {
        "message": "When will I get married and how is my spouse?",
        "chart": chart,
    }
    chat_resp = auth_client.post("/api/kundali-chat", json=chat_payload)
    assert chat_resp.status_code == 200
    assert "reply" in chat_resp.json()
    assert chat_resp.json()["topic"] == "marriage"


def test_domains_endpoint():
    auth_client = get_auth_client()
    payload = {
        "year": 1993,
        "month": 3,
        "day": 10,
        "hour": 9,
        "minute": 15,
        "city": "Pune",
    }
    resp = auth_client.post("/api/domains", json=payload)
    assert resp.status_code == 200
    assert "domains" in resp.json()


def test_blogs_public_endpoints():
    resp = client.get("/api/blogs")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_web_pages_render():
    routes = ["/", "/prediction", "/panchang.html", "/blogs", "/about", "/horoscope", "/kundali", "/login", "/signup"]
    for route in routes:
        resp = client.get(route)
        assert resp.status_code == 200
        assert "text/html" in resp.headers["content-type"]
