# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

liang_ba is an enterprise CMS built with Django 4.2 + Wagtail 5.2, featuring React/TypeScript admin panel and stock market data analysis capabilities.

## Common Commands

```bash
# Install dependencies
make install          # Python deps
make dev-install      # Dev dependencies (pytest, mypy, etc.)
make install-pre-commit  # Install pre-commit hooks

# Testing (80% coverage required on apps/)
make test             # pytest -v --tb=short
make test-coverage    # With coverage report (htmlcov/)
make test-frontend    # Vitest tests in admin/

# Code quality
make lint             # ruff, mypy, ESLint
make lint-fix         # Auto-fix linters
make format           # ruff format, black, isort
make check-format     # Verify formatting

# Docker
make docker-up        # Start containers (web, db, redis)
make docker-down      # Stop containers
make docker-logs      # View logs

# Database
make migrate          # Run migrations
make backup           # Create database backup
```

## Architecture

### Backend (Django + Wagtail)

**Installed Apps** (`apps/`):
- `wagtail_apps` - Wagtail CMS customization
- `companyinfo` - Company, products, news, recruitment
- `users` - Custom user model with JWT auth
- `admin_api` - REST API for admin panel
- `reports` - Research reports, PDF generation
- `factorhub` - Stock market data, quantitative factors

**URL Routing** (`apps/urls.py`):
- `/admin/` - Django admin
- `/manage/` - Wagtail CMS
- `/api/admin/` - REST API
- `/api/reports/` - Reports API
- `/api/factorhub/` - Factor analysis API
- `/` - Public site (Wagtail pages)

**Authentication**: JWT via `rest_framework_simplejwt`
- Access token: 60 min lifetime
- Refresh token: 7 days with rotation

**Middleware** (`utils/middleware/`):
- `RequestTraceMiddleware` - trace_id injection
- `PerformanceMiddleware` - >1000ms threshold logging
- `ExceptionLoggingMiddleware` - Exception handling
- `SecurityAuditMiddleware` - Security logging

**Logging**: Separate handlers for app, error, performance, security logs in `logs/`

### Frontend (`admin/`)

React 18 + TypeScript with:
- Ant Design 5 (UI components)
- TanStack React Query (data fetching)
- Zustand (state management)
- ECharts (data visualization)
- React Router DOM 6

### Database

- MySQL 8.0 for persistent data
- Redis for caching (key prefix isolation)
- Test database: SQLite in-memory (faster tests)

## Code Conventions

### Python
- Follow `ruff.toml` (line-length: 100)
- Use Django REST Framework ViewSets for APIs
- Define models in `apps/{app}/models/` subdirectory
- Create serializers in `apps/{app}/serializers.py`

### Testing
- Fixtures in `conftest.py`: `api_client`, `authenticated_client`, `test_user`, `admin_user`, `sample_company`
- Test files: `tests/test_*.py`
- Password hasher: MD5 for faster tests

### Pre-commit Hooks
Configured in `.pre-commit-config.yaml`:
- ruff, black, isort (Python)
- ESLint, Prettier (TypeScript)
- Docker (hadolint), shell scripts (shellcheck)
- Secret detection (gitleaks)

## Environment

- **Settings**: `base_settings.py` + `local_settings.py` (gitignored)
- **Database**: MySQL at 172.18.4.63:3306, Redis at 172.18.4.63:6379/2
- **Python**: 3.10+

## Key Files

- `base_settings.py` - Django settings (middleware, logging, REST framework)
- `conftest.py` - Pytest fixtures
- `ruff.toml` - Python linting rules
- `.pre-commit-config.yaml` - Pre-commit hooks
- `Dockerfile.prod` - Multi-stage production Docker build
- `.github/workflows/ci.yml` - CI pipeline
