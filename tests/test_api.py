"""
Sample API tests for the admin API.
"""

from unittest.mock import patch

import pytest
from django.test import Client, RequestFactory
from rest_framework import status
from rest_framework.exceptions import ValidationError

from utils.logging.drf_exception_handler import custom_exception_handler
from utils.logging.parser import LogParser


@pytest.mark.django_db
class TestAuthEndpoints:
    """Test cases for authentication endpoints."""

    def test_login_view(self):
        """Test that login page loads."""
        client = Client()
        response = client.get("/api/auth/login/")

        # May redirect or return 200 depending on configuration
        assert response.status_code in [200, 301, 302, 404]


@pytest.mark.django_db
class TestCompanyEndpoints:
    """Test cases for company API endpoints."""

    def test_company_list_requires_auth(self):
        """Test that company list requires authentication."""
        client = Client()
        response = client.get("/api/v1/companies/")

        # Should return 401 or 403 without auth
        assert response.status_code in [401, 403, 302, 404]

    def test_company_detail_requires_auth(self):
        """Test that company detail requires authentication."""
        client = Client()
        response = client.get("/api/v1/companies/000001.SZ/")

        # Should return 401 or 403 without auth
        assert response.status_code in [401, 403, 302, 404]


@pytest.mark.django_db
class TestAdminUserEndpoints:
    """Test cases for admin user endpoints."""

    def test_admin_can_update_user_with_profile(self, api_client, admin_user, test_user):
        """Test admin can update a user and nested profile fields."""
        api_client.force_authenticate(user=admin_user["user"])

        response = api_client.patch(
            f"/api/admin/users/{test_user['user'].id}/",
            {
                "first_name": "Updated",
                "profile": {
                    "department": "Research",
                    "position": "Analyst",
                },
            },
            format="json",
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data["first_name"] == "Updated"
        assert response.data["profile"]["department"] == "Research"
        assert response.data["profile"]["position"] == "Analyst"

        test_user["user"].refresh_from_db()
        assert test_user["user"].first_name == "Updated"
        assert test_user["user"].profile.department == "Research"


def test_custom_exception_handler_logs_handled_api_errors():
    """Test handled DRF exceptions are also logged."""
    request = RequestFactory().post("/api/admin/users/")

    with patch("utils.logging.drf_exception_handler.logger.warning") as logger_warning:
        response = custom_exception_handler(
            ValidationError({"email": ["This field is required."]}),
            {"request": request, "view": None},
        )

        assert response is not None
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        logger_warning.assert_called_once()


def test_log_parser_reads_django_text_logs(tmp_path, settings):
    """Test parser can read Django text logs reliably."""
    log_file = tmp_path / "django.log"
    log_file.write_text(
        "\n".join(
            [
                "[INFO][2026-04-13 10:00:00,000][server.py:10] started",
                "[WARNING][2026-04-13 10:00:01,000][/tmp/project/autoreload.py:394] changed",
                "[ERROR][2026-04-13 10:00:02,000][views.py:42] failed",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    parser = LogParser(log_file)
    entries = list(parser.parse(offset=0, limit=3))

    assert len(entries) == 3
    assert entries[0].message == "started"
    assert entries[1].module == "autoreload.py"
    assert entries[1].line == 394
    assert entries[2].level.value == "ERROR"
