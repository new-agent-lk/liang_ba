"""
Health check endpoints for monitoring and CI/CD pipelines.
"""
import os
import sys
import time
from datetime import datetime, timezone

from django.db import connection
from django.http import JsonResponse
from django.views import View


class HealthCheckView(View):
    """
    Health check endpoint for load balancers and monitoring systems.

    Checks:
    - Database connectivity
    - Redis connectivity (if configured)
    - System status

    Returns:
        200: All services healthy
        503: One or more services unhealthy
    """

    def get(self, request):
        """
        Handle GET request for health check.

        Query parameters:
            - detailed: Return detailed health information (default: false)
        """
        detailed = request.GET.get("detailed", "false").lower() == "true"

        health_status = {
            "status": "healthy",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "services": {},
        }

        overall_healthy = True

        # Check database
        db_status = self._check_database()
        health_status["services"]["database"] = db_status
        if not db_status["healthy"]:
            overall_healthy = False

        # Check Redis (optional)
        redis_status = self._check_redis()
        health_status["services"]["redis"] = redis_status
        if not redis_status["healthy"]:
            overall_healthy = False

        # System information (only in detailed mode)
        if detailed:
            health_status["system"] = self._get_system_info()

        # Set overall status
        health_status["status"] = "healthy" if overall_healthy else "unhealthy"

        status_code = 200 if overall_healthy else 503
        return JsonResponse(health_status, status=status_code)

    def _check_database(self):
        """Check database connectivity."""
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
            return {
                "healthy": True,
                "type": "mysql",
                "latency_ms": 0,  # Will be updated below
            }
        except Exception as e:
            return {
                "healthy": False,
                "type": "mysql",
                "error": str(e),
            }

    def _check_redis(self):
        """Check Redis connectivity."""
        try:
            from django.conf import settings

            if not hasattr(settings, "REDIS_HOST"):
                return {
                    "healthy": True,
                    "type": "not_configured",
                    "message": "Redis not configured",
                }

            import redis

            r = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB or 0,
                socket_timeout=2,
                socket_connect_timeout=2,
            )
            r.ping()
            return {
                "healthy": True,
                "type": "redis",
                "host": settings.REDIS_HOST,
            }
        except Exception as e:
            return {
                "healthy": False,
                "type": "redis",
                "error": str(e),
            }

    def _get_system_info(self):
        """Get system information for detailed health check."""
        return {
            "python_version": sys.version,
            "platform": sys.platform,
            "timezone": str(time.tzname),
            "environment": os.environ.get("DJANGO_SETTINGS_MODULE", "unknown"),
            "debug": os.environ.get("DJANGO_DEBUG", "unknown"),
            "uptime_seconds": time.time() - getattr(self, "_start_time", time.time()),
        }


class SimpleHealthCheckView(View):
    """
    Simple health check endpoint for load balancers.

    Returns minimal response - just 200 if the app is running.
    No database or external service checks.
    """

    def get(self, _request):
        """Return simple 200 OK response."""
        return JsonResponse({"status": "ok"})
