"""Database and Authentication tests."""

import pytest
from app.core.security import hash_password, verify_password
from app.db.database import Base, SessionLocal, engine, init_db
from app.models.blog import Blog
from app.models.user import User, UserProfile
from app.schemas.auth import UserLogin, UserRegister
from app.schemas.blog import BlogCreate
from app.services.auth_service import auth_service
from app.services.blog_service import blog_service


@pytest.fixture(scope="module")
def db():
    init_db()
    session = SessionLocal()
    yield session
    session.close()


def test_password_hashing():
    pwd = "SecureAstrologyPassword123"
    hashed = hash_password(pwd)
    assert hashed != pwd
    assert verify_password(pwd, hashed) is True
    assert verify_password("WrongPassword", hashed) is False


def test_user_registration_and_auth(db):
    test_email = "architect_tester@astrologic.ai"

    # Cleanup if exists
    existing = db.query(User).filter(User.email == test_email).first()
    if existing:
        db.delete(existing)
        db.commit()

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
