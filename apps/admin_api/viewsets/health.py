"""
Health check endpoints for monitoring.
"""

import sys
import time
from datetime import datetime, timezone

from django.db import connection
from django.http import JsonResponse
from django.views import View


class HealthCheckView(View):
    """Health check endpoint with database and Redis connectivity checks."""

    def get(self, request):
        """Handle health check request."""
        detailed = request.GET.get("detailed", "false").lower() == "true"

        status = {"status": "healthy", "timestamp": datetime.now(timezone.utc).isoformat()}
        overall_healthy = True

        # Check database
        db_status = self._check_database()
        status["database"] = db_status
        if not db_status["healthy"]:
            overall_healthy = False

        # Check Redis
        redis_status = self._check_redis()
        status["redis"] = redis_status
        if not redis_status["healthy"]:
            overall_healthy = False

        # Detailed system info
        if detailed:
            status["system"] = {
                "python_version": sys.version.split()[0],
                "platform": sys.platform,
                "timezone": str(time.tzname),
            }

        status["status"] = "healthy" if overall_healthy else "unhealthy"
        return JsonResponse(status, status=200 if overall_healthy else 503)

    def _check_database(self):
        """Check PostgreSQL connectivity."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            return {"healthy": True, "type": "postgresql"}
        except Exception as e:
            return {"healthy": False, "type": "postgresql", "error": str(e)}

    def _check_redis(self):
        """Check Redis connectivity."""
        try:
            import redis
            from django.conf import settings

            r = redis.Redis(
                host=getattr(settings, "REDIS_HOST", "localhost"),
                port=getattr(settings, "REDIS_PORT", 6379),
                socket_timeout=2,
                socket_connect_timeout=2,
            )
            r.ping()
            return {"healthy": True, "type": "redis"}
        except Exception as e:
            return {"healthy": False, "type": "redis", "error": str(e)}


class SimpleHealthCheckView(View):
    """Simple health check for load balancers."""

    def get(self, _request):
        """Return minimal health status."""
        return JsonResponse({"status": "ok"})
