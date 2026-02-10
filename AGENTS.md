
## Project Overview

liang_ba is an enterprise CMS built with Django 4.2 + Wagtail 5.2, featuring React/TypeScript admin panel and stock market data analysis capabilities.

## Common Commands

```bash
# Install dependencies
make install          # Python deps
make dev-install      # Dev dependencies (pytest, mypy, ruff, etc.)
make install-pre-commit  # Install pre-commit hooks

# Testing (80% coverage required on apps/)
make test             # pytest -v --tb=short
make test-coverage    # With coverage report (htmlcov/)
make test-frontend    # Vitest tests in admin/
pytest tests/test_users.py::TestUser::test_create_user  # Run single test

# Code quality
make lint             # ruff, mypy, ESLint
make lint-fix         # Auto-fix linters
make format           # ruff format, black, isort
make check-format     # Verify formatting

# Docker
make docker-up        # Start containers (web, db, redis)
make docker-down      # Stop containers
docker compose logs -f web  # View web logs

# Database
make migrate          # Run migrations
make backup          # Create database backup

# Frontend dev
cd admin && npm run dev  # Start Vite dev server (port 5173)
cd admin && npm run build  # Build for production
```

## Architecture

### Backend (Django + Wagtail)

**Installed Apps** (`apps/`):
- `wagtail_apps` - Wagtail CMS customization (page models, snippets)
- `companyinfo` - Company info, products, news, recruitment (job positions, resumes)
- `users` - Custom user model with JWT auth (UserProfile extension)
- `admin_api` - REST API for admin panel (ViewSets for CRUD)
- `reports` - Research reports with backtest metrics, PDF generation
- `factorhub` - Stock market data, quantitative factors, backtesting engine

**URL Routing** (`apps/urls.py`):
- `/admin/` - Django admin
- `/manage/` - Wagtail CMS admin
- `/api/admin/` - REST API for admin panel
- `/api/reports/` - Reports API
- `/api/factorhub/` - Factor analysis, backtesting, market data API
- `/` - Public site (Wagtail pages)

**Authentication**: JWT via `rest_framework_simplejwt`
- Access token: 60 min lifetime
- Refresh token: 7 days with rotation with blacklist

**Middleware** (in order, `utils/middleware/`):
1. `RequestTraceMiddleware` - trace_id injection, request/response logging
2. `PerformanceMiddleware` - >1000ms threshold logging
3. `ExceptionLoggingMiddleware` - Exception handling
4. `SecurityAuditMiddleware` - Security logging

**Logging**: Separate handlers in `logs/` for app, error, performance, security; custom formatters and filters in `utils/logging/`

### Frontend (`admin/`)

React 18 + TypeScript with:
- Ant Design 5 (UI components)
- TanStack React Query (data fetching with caching)
- Zustand (auth and menu state management)
- ECharts (charts for factor analysis, backtest results)
- React Router DOM 6 (protected routes)
- Vite (dev server, build)

### FactorHub (Quantitative Analysis)

Core components in `apps/factorhub/core/`:
- `factor_lib.py` - Factor definitions and management
- `factor_calculator.py` - Compute technical/macro factors
- `factor_analyzer.py` - IC analysis, decile analysis
- `backtester.py` - Backtesting engine with strategy metrics
- `data_provider.py` - Market data from akshare with mock fallback

## Code Conventions

### Python
- Line length: 100 (ruff.toml)
- Models: `apps/{app}/models/` subdirectory with `__init__.py` exporting all models
- Serializers: `apps/{app}/serializers.py` (not in subdirectory)
- ViewSets: `apps/{app}/viewsets/` for DRF ViewSets
- Fixtures: `conftest.py` in project root

### Testing
**Fixtures** (`conftest.py`):
- `api_client`, `authenticated_client` - DRF API client
- `test_user`, `admin_user` - User fixtures
- `sample_company`, `sample_market_data` - Data fixtures
- `temp_media_file` - File upload testing

**Config**:
- Uses SQLite in-memory for faster tests
- MD5PasswordHasher for test speed
- Coverage required: 80% on `apps/`

### Pre-commit Hooks
`.pre-commit-config.yaml`:
- ruff, black, isort (Python)
- ESLint, Prettier (TypeScript)
- hadolint (Docker), shellcheck (shell scripts)
- Secret detection (gitleaks via CI)

## Environment

**Settings**: `base_settings.py` + `local_settings.py` (gitignored)

**Database**: PostgreSQL 16 (test: SQLite in-memory)
- Redis 7 for caching (key prefix isolation)

**Python**: 3.10+

## Key Files

- `base_settings.py` - Django settings (middleware, logging, REST framework, JWT)
- `conftest.py` - Pytest fixtures
- `ruff.toml` - Python linting rules
- `.pre-commit-config.yaml` - Pre-commit hooks
- `Dockerfile.prod` - Multi-stage production Docker build
- `.github/workflows/ci.yml` - CI pipeline
