"""
Configuration for tests directory.
"""

# Test settings
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# Ensure Django settings module is set
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_settings")

# pytest-django configuration
import django

django.setup()
