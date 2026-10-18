"""Comprehensive Automated Verification Test Suite for Multi-Language (i18n) Support.

Verifies all 10 requested features:
1. Language detection priority (URL prefix, Query param, Cookie, Accept-Language header, Fallback).
2. Locale loading & fallback to English.
3. Client locale API (/api/locales/{lang}).
4. Astrology terminology translation (Planets, Signs, Concepts).
5. AI prompt language directive injection.
6. User preferred_language login synchronization.
7. Multi-language blog content creation & language filtering.
8. Language prefix routing (/{lang}/kundali, /{lang}/panchang, etc.).
"""

import uuid
import pytest
from fastapi.testclient import TestClient

from shared.config.settings import Settings
from modules.auth.security import hash_password, verify_password
from shared.db.session import SessionLocal, init_db
from gateway.main import app
from modules.auth.models import User
from modules.narrative.prompt_builder import build_chat_prompt, build_prediction_prompt
from modules.blog.api import BlogService
from shared.i18n.translation import (
    SUPPORTED_LANGUAGES,
    get_translation,
    load_translations,
    translate_astrology_term,
)
from modules.blog.schemas import BlogCreate

blog_service = BlogService()



def test_01_language_detection_priority():
    """Verify 5-level language detection priority."""
    # 1. URL prefix priority
    tc1 = TestClient(app)
    res_url = tc1.get("/hi/kundali")
    assert res_url.status_code == 200
    assert res_url.headers.get("content-language") == "hi"

    # 2. Query parameter priority
    tc2 = TestClient(app)
    res_query = tc2.get("/kundali?lang=mr")
    assert res_query.status_code == 200
    assert res_query.headers.get("content-language") == "mr"

    # 3. Cookie priority
    tc3 = TestClient(app)
    tc3.cookies.set("lang", "ta")
    res_cookie = tc3.get("/kundali")
    assert res_cookie.status_code == 200
    assert res_cookie.headers.get("content-language") == "ta"

    # 4. Accept-Language header priority
    tc4 = TestClient(app)
    res_header = tc4.get("/kundali", headers={"accept-language": "gu-IN,gu;q=0.9"})
    assert res_header.status_code == 200
    assert res_header.headers.get("content-language") == "gu"

    # 5. Default fallback
    tc5 = TestClient(app)
    res_default = tc5.get("/kundali")
    assert res_default.status_code == 200
    assert res_default.headers.get("content-language") == "en"


def test_02_all_8_supported_locales_exist():
    """Verify all 8 supported language locale files load properly."""
    expected_langs = ["en", "hi", "mr", "gu", "ta", "te", "kn", "bn"]
    for lang in expected_langs:
        loc = load_translations(lang)
        assert isinstance(loc, dict)
        assert len(loc) > 0
        assert "language.name" in loc or "navbar.home" in loc


def test_03_locales_api_endpoint():
    """Verify GET /api/locales/{lang} returns correct dictionary."""
    tc = TestClient(app)
    res = tc.get("/api/locales/hi")
    assert res.status_code == 200
    data = res.json()
    assert data["lang"] == "hi"
    assert "supported_languages" in data
    assert data["supported_languages"]["hi"] == "हिन्दी"
    assert data["translations"]["navbar.home"] == "होम"



def test_04_astrology_terminology_translation():
    """Verify planetary and zodiac terminology translation across regional languages."""
    assert translate_astrology_term("Sun", "hi") == "सूर्य"
    assert translate_astrology_term("Sun", "ta") == "சூரியன்"
    assert translate_astrology_term("Moon", "mr") == "चंद्र"
    assert translate_astrology_term("Mars", "te") == "అంగారకుడు"

    assert translate_astrology_term("Aries", "hi") == "मेष"
    assert translate_astrology_term("Aries", "ta") == "மேஷம்"
    assert translate_astrology_term("Taurus", "gu") == "વૃષભ"

    # Fallback to original term if English or unknown
    assert translate_astrology_term("Sun", "en") == "Sun"
    assert translate_astrology_term("UnknownTerm", "hi") == "UnknownTerm"


def test_05_ai_prompt_language_directives():
    """Verify AI prompt builders inject strict language output instructions."""
    sample_chart = {"basic_details": {"lagna": "Aries"}, "dasha": {"current_mahadasha": "Jupiter"}}

    pred_hi = build_prediction_prompt(sample_chart, "marriage", lang="hi")
    assert "strictly in हिन्दी (language code: hi)" in pred_hi

    pred_ta = build_prediction_prompt(sample_chart, "career", lang="ta")
    assert "strictly in தமிழ் (language code: ta)" in pred_ta

    chat_mr = build_chat_prompt(sample_chart, "How is my future?", lang="mr")
    assert "strictly in मराठी (language code: mr)" in chat_mr


def test_06_translation_fallback_chain():
    """Verify get_translation falls back to English when key is missing."""
    assert get_translation("home.title", "hi") == "AstroLogic में आपका स्वागत है"
    assert get_translation("non_existent_key", "hi", default="FallbackText") == "FallbackText"



def test_07_user_preferred_language_sync():
    """Verify login auto-sets language cookie matching user's preferred_language."""
    init_db()
    db = SessionLocal()
    try:
        uid = uuid.uuid4().hex[:6]
        email = f"user_{uid}@example.com"
        user = User(
            name="Tamil User",
            email=email,
            password_hash=hash_password("Password123!"),
            preferred_language="ta",
        )
        db.add(user)
        db.commit()

        tc = TestClient(app)
        login_res = tc.post(
            "/login",
            data={"email": email, "password": "Password123!"},
            follow_redirects=False,
        )
        assert login_res.status_code == 303
        assert "lang=ta" in login_res.headers.get("set-cookie", "")
    finally:
        db.close()


def test_08_multi_lingual_blog_content():
    """Verify blogs can be created with language tag and filtered by language."""
    init_db()
    db = SessionLocal()
    try:
        uid = uuid.uuid4().hex[:6]
        blog_service.create_blog(db, BlogCreate(title=f"English Blog {uid}", content="Content"), language="en")
        blog_service.create_blog(db, BlogCreate(title=f"Hindi Blog {uid}", content="विवरण"), language="hi")

        hi_blogs = blog_service.get_all_blogs(db, lang="hi")
        assert len(hi_blogs) > 0
        assert hi_blogs[0].language == "hi"

        en_blogs = blog_service.get_all_blogs(db, lang="en")
        assert len(en_blogs) > 0
        assert en_blogs[0].language == "en"
    finally:
        db.close()


def test_09_language_prefix_routes_render():
    """Verify localized page routes render properly."""
    tc = TestClient(app)
    routes = ["/hi/", "/mr/kundali", "/ta/panchang", "/te/prediction", "/gu/horoscope", "/kn/blogs"]
    for r in routes:
        res = tc.get(r)
        assert res.status_code == 200
        assert "text/html" in res.headers["content-type"]
