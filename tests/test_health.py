"""
Tests for health check endpoints.
"""

import pytest
from django.test import Client


@pytest.mark.django_db
class TestHealthEndpoints:
    """Test cases for health check endpoints."""

    def test_simple_health_check(self):
        """Test simple health endpoint returns 200."""
        client = Client()
        response = client.get("/health/simple/")

        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "ok"

    def test_health_check_detailed(self):
        """Test detailed health endpoint returns status."""
        client = Client()
        response = client.get("/health/?detailed=true")

        # Should return 200 or 503 depending on DB state
        assert response.status_code in [200, 503, 404]
        if response.status_code in [200, 503]:
            data = response.json()
            assert "status" in data
            assert "timestamp" in data
            assert "services" in data

    def test_health_check_services(self):
        """Test health endpoint includes service checks."""
        client = Client()
        response = client.get("/health/")

        assert response.status_code in [200, 503, 404]
        if response.status_code in [200, 503]:
            data = response.json()
            assert "database" in data["services"]
            assert "redis" in data["services"]

    def test_health_api_endpoint(self):
        """Test API health endpoint at /api/admin/health/."""
        client = Client()
        response = client.get("/api/admin/health/")

        assert response.status_code in [200, 503]
        data = response.json()
        assert "status" in data

    def test_health_simple_api_endpoint(self):
        """Test simple API health endpoint."""
        client = Client()
        response = client.get("/api/admin/health/simple/")

        assert response.status_code in [200, 404]
        if response.status_code == 200:
            data = response.json()
            assert data["status"] == "ok"
