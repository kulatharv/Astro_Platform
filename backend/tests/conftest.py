"""Pytest fixtures and database initialization."""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from shared.db.session import Base, engine, init_db



@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """Ensure all database tables are created before test run."""
    init_db()
    yield
