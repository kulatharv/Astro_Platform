"""Phase 0 Security Verification Test Suite.

Verifies:
1. Fail-fast startup configuration validation.
2. No hardcoded secrets or fallback admin credentials in source code.
3. Admin DB model and PBKDF2 password hashing.
4. Protected blog API routes (no public POST /api/blogs).
5. Isolated session chart state & in-memory PDF streaming (no cross-user data leak).
6. Default-deny authentication middleware on /api/* routes.
"""

import uuid
import pytest
from fastapi.testclient import TestClient

from shared.config.settings import Settings, validate_settings
from modules.auth.security import verify_password
from shared.db.session import SessionLocal, init_db
from gateway.main import app
from modules.auth.models import AdminUser


client = TestClient(app)


def test_01_fail_fast_config_validation():
    """Verify app crashes with RuntimeError when required env vars are missing."""
    invalid_settings = Settings(
        secret_key="",
        session_secret_key="some-key",
        jwt_secret_key="some-key",
        database_url="sqlite:///./test.db",
    )
    with pytest.raises(RuntimeError) as exc_info:
        validate_settings(invalid_settings)
    assert "Missing required environment variable: SECRET_KEY" in str(exc_info.value)


def test_02_no_hardcoded_secrets_or_astro123():
    """Verify config contains no default string secrets and no plaintext fallback credentials exist."""
    settings_obj = Settings()
    # Required keys must come from environment, not hardcoded defaults
    assert settings_obj.secret_key != "astrologic-secret-key-production-change-me"
    assert not hasattr(settings_obj, "admin_username")
    assert not hasattr(settings_obj, "admin_password")


def test_03_admin_user_db_pbkdf2_auth():
    """Verify admin user exists in DB and authenticates via PBKDF2 hashing."""
    init_db()
    db = SessionLocal()
    try:
        admin = db.query(AdminUser).filter(AdminUser.username == "admin").first()
        assert admin is not None
        assert "$" in admin.password_hash
        assert verify_password("AdminSecurePassword2026!", admin.password_hash)
        assert not verify_password("wrongpassword", admin.password_hash)
    finally:
        db.close()


def test_04_admin_login_flow():
    """Test web admin login via database credentials."""
    test_client = TestClient(app)
    # Invalid credentials -> fail
    res_bad = test_client.post("/admin/login", data={"username": "admin", "password": "wrong"})
    assert res_bad.status_code == 200
    assert "Invalid administrator credentials" in res_bad.text

    # Valid credentials -> success redirect
    res_good = test_client.post(
        "/admin/login",
        data={"username": "admin", "password": "AdminSecurePassword2026!"},
        follow_redirects=False,
    )
    assert res_good.status_code == 303
    assert res_good.headers["location"] == "/admin/blogs"


def test_05_blog_api_security():
    """Verify public POST /api/blogs does not exist or requires authentication."""
    test_client = TestClient(app)
    res_post_public = test_client.post("/api/blogs", data={"title": "Hack", "content": "Hacked"})
    # Must be blocked by Default-Deny (401) or 405 Method Not Allowed
    assert res_post_public.status_code in (401, 405, 404)

    # GET /api/blogs remains public
    res_get = test_client.get("/api/blogs")
    assert res_get.status_code == 200


def test_06_global_state_isolation_kundali_and_pdf():
    """Verify user sessions do not leak Kundali chart data across sessions."""
    client_a = TestClient(app)
    client_b = TestClient(app)

    uid_a = uuid.uuid4().hex[:6]
    uid_b = uuid.uuid4().hex[:6]

    # Authenticate Client A and Client B sessions
    client_a.post("/signup", data={"name": "User A", "email": f"usera_{uid_a}@example.com", "password": "Password123!"})
    client_b.post("/signup", data={"name": "User B", "email": f"userb_{uid_b}@example.com", "password": "Password123!"})

    # Client B requests download without calculating -> 400 (No chart in session)
    res_b_empty = client_b.get("/api/download-kundali")
    assert res_b_empty.status_code == 400

    # Client A posts kundali payload
    res_a_calc = client_a.post(
        "/api/kundali",
        json={"year": 1990, "month": 1, "day": 1, "hour": 12, "minute": 0, "city": "Pune"},
    )
    assert res_a_calc.status_code == 200

    # Client A can download PDF (in-memory streaming buffer)
    res_a_pdf = client_a.get("/api/download-kundali")
    assert res_a_pdf.status_code == 200
    assert res_a_pdf.headers["content-type"] == "application/pdf"
    assert len(res_a_pdf.content) > 0

    # Client B still has no access to Client A's chart
    res_b_isolated = client_b.get("/api/download-kundali")
    assert res_b_isolated.status_code == 400


def test_07_default_deny_middleware_routes():
    """Verify default-deny middleware blocks unauthenticated requests to protected endpoints."""
    fresh_client = TestClient(app)
    # Public routes allowed
    assert fresh_client.get("/health").status_code == 200
    assert fresh_client.post("/api/panchang", json={"city": "Delhi"}).status_code == 200
    assert fresh_client.get("/api/cities").status_code == 200

    # Protected routes blocked for unauthenticated users
    assert fresh_client.post("/api/prediction", json={"year": 1990, "month": 1, "day": 1, "hour": 12}).status_code == 401
    assert fresh_client.post("/api/chat", json={"message": "Hello"}).status_code == 401
    assert fresh_client.post("/api/domains", json={"year": 1990, "month": 1, "day": 1, "hour": 12, "minute": 0, "city": "Pune"}).status_code == 401
    assert fresh_client.get("/api/admin/blogs").status_code == 401
