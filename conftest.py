"""
Pytest configuration and fixtures for Django tests.
"""

import os
import sys
from pathlib import Path

import pytest

# Add the project root to the Python path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configure Django settings before loading
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_settings")


@pytest.fixture(scope="function")
def api_client():
    """Provide a Django REST Framework API client."""
    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture(scope="function")
def authenticated_client(api_client, test_user):
    """Provide an authenticated API client."""
    from rest_framework import status

    response = api_client.post(
        "/api/auth/login/",
        {
            "username": test_user["username"],
            "password": test_user["password"],
        },
        format="json",
    )
    if response.status_code == status.HTTP_200_OK:
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    return api_client


@pytest.fixture(scope="function")
def test_user(db):
    """Create and return a test user."""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass123",
    )
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "user": user,
    }


@pytest.fixture(scope="function")
def admin_user(db):
    """Create and return an admin user."""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user = User.objects.create_superuser(
        username="adminuser",
        email="admin@example.com",
        password="adminpass123",
    )
    return {
        "username": "adminuser",
        "email": "admin@example.com",
        "password": "adminpass123",
        "user": user,
    }


@pytest.fixture(scope="function")
def sample_company(db):
    """Create a sample company for testing."""
    from apps.companyinfo.models import Company

    company = Company.objects.create(
        ts_code="000001.SZ",
        name="Test Company",
        industry="Technology",
        market="Main Board",
        list_status="L",
    )
    return company


@pytest.fixture(scope="function")
def sample_market_data(db):
    """Create sample market data for testing."""
    from datetime import date, timedelta

    import pandas as pd

    from apps.factorhub.models import MarketData

    today = date.today()
    dates = [today - timedelta(days=i) for i in range(10)]

    data = {
        "trade_date": [d.strftime("%Y%m%d") for d in dates],
        "close": [100 + i for i in range(10)],
        "open": [99 + i for i in range(10)],
        "high": [102 + i for i in range(10)],
        "low": [98 + i for i in range(10)],
        "volume": [1000000 + i * 10000 for i in range(10)],
        "amount": [100000000 + i * 1000000 for i in range(10)],
    }

    df = pd.DataFrame(data)
    market_data = MarketData.objects.create(
        ts_code="000001.SZ",
        trade_date=today.strftime("%Y%m%d"),
        close=100.0,
        open=99.0,
        high=102.0,
        low=98.0,
        volume=1000000,
        amount=100000000,
    )
    return market_data


@pytest.fixture(scope="function")
def temp_media_file(tmp_path):
    """Create a temporary media file for testing."""
    from django.core.files.uploadedfile import SimpleUploadedFile

    content = b"test file content"
    file = SimpleUploadedFile(
        "test.txt",
        content,
        content_type="text/plain",
    )
    return file
