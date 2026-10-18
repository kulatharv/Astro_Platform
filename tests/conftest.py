"""Pytest fixtures and database initialization."""

import pytest
from app.db.database import Base, engine, init_db


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Ensure all database tables are created before test run."""
    init_db()
    yield
