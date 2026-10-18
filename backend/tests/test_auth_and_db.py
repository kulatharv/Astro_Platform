"""Database and Authentication tests."""

import uuid
import pytest
from modules.auth.security import hash_password, verify_password
from shared.db.session import SessionLocal, init_db
from modules.blog.models import Blog
from modules.auth.models import User, UserProfile
from modules.auth.schemas import UserLogin, UserRegister
from modules.blog.schemas import BlogCreate
from modules.auth.api import AuthService
from modules.blog.api import BlogService

auth_service = AuthService()
blog_service = BlogService()



@pytest.fixture
def db():
    init_db()
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


def test_password_hashing():
    pwd = "SecureAstrologyPassword123"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_user_registration_and_auth(db):
    unique_suffix = uuid.uuid4().hex[:8]
    test_email = f"architect_{unique_suffix}@astrologic.ai"

    reg_data = UserRegister(
        name="Architect Tester",
        email=test_email,
        phone="+91-9876543210",
        password="TestPassword@123",
    )
    user, err = auth_service.register_user(db, reg_data)
    assert err is None
    assert user is not None
    assert user.email == test_email

    # Duplicate registration check
    dup_user, dup_err = auth_service.register_user(db, reg_data)
    assert dup_user is None
    assert "already registered" in dup_err

    # Authentication test
    login_data = UserLogin(email=test_email, password="TestPassword@123")
    auth_user = auth_service.authenticate_user(db, login_data)
    assert auth_user is not None
    assert auth_user.id == user.id

    # Bad auth test
    bad_login = UserLogin(email=test_email, password="WrongPassword")
    assert auth_service.authenticate_user(db, bad_login) is None


def test_blog_crud(db):
    blog_data = BlogCreate(
        title="Test Planetary Transits 2026",
        content="Jupiter transit through Cancer brings tremendous fortune and expansive spiritual energy.",
    )
    blog = blog_service.create_blog(db, blog_data)
    assert blog.id is not None
    assert blog.title == blog_data.title

    fetched = blog_service.get_blog_by_id(db, blog.id)
    assert fetched is not None
    assert fetched.content == blog_data.content

    # Cleanup
    blog_service.delete_blog(db, blog.id)
