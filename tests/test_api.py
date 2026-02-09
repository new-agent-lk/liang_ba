"""
Sample API tests for the admin API.
"""
import pytest
from django.test import Client


@pytest.mark.django_db
class TestAuthEndpoints:
    """Test cases for authentication endpoints."""

    def test_login_view(self):
        """Test that login page loads."""
        client = Client()
        response = client.get("/api/auth/login/")

        # May redirect or return 200 depending on configuration
        assert response.status_code in [200, 301, 302]


@pytest.mark.django_db
class TestCompanyEndpoints:
    """Test cases for company API endpoints."""

    def test_company_list_requires_auth(self):
        """Test that company list requires authentication."""
        client = Client()
        response = client.get("/api/v1/companies/")

        # Should return 401 or 403 without auth
        assert response.status_code in [401, 403, 302]

    def test_company_detail_requires_auth(self):
        """Test that company detail requires authentication."""
        client = Client()
        response = client.get("/api/v1/companies/000001.SZ/")

        # Should return 401 or 403 without auth
        assert response.status_code in [401, 403, 302]
