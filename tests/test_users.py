"""
Sample Django tests for demonstration.
"""
import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestUsers:
    """Test cases for the users app."""

    def test_create_user(self):
        """Test creating a regular user."""
        User = get_user_model()
        email = "test@example.com"
        username = "testuser"
        password = "testpass123"

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        assert user.username == username
        assert user.email == email
        assert user.check_password(password)
        assert not user.is_staff
        assert not user.is_superuser

    def test_create_superuser(self):
        """Test creating a superuser."""
        User = get_user_model()

        user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
        )

        assert user.username == "admin"
        assert user.email == "admin@example.com"
        assert user.is_staff
        assert user.is_superuser

    def test_email_normalized(self):
        """Test that email is normalized."""
        User = get_user_model()

        user = User.objects.create_user(
            username="testuser",
            email="Test@EXAMPLE.COM",
            password="testpass123",
        )

        assert user.email == "test@example.com"

    def test_create_user_without_username(self):
        """Test that creating user without username raises error."""
        User = get_user_model()

        with pytest.raises(ValueError):
            User.objects.create_user(
                username="",
                email="test@example.com",
                password="testpass123",
            )
