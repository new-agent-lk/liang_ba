# CI/CD Pipeline Setup Guide

This document describes the complete CI/CD pipeline configuration for the liang-ba project.

## Overview

The project uses GitHub Actions for both Continuous Integration (CI) and Continuous Deployment (CD):

- **CI Pipeline** (`.github/workflows/ci.yml`): Runs on every push and PR
- **CD Pipeline** (`.github/workflows/cd.yml`): Runs on merge to main and releases
- **Security Scan** (`.github/workflows/security.yml`): Runs weekly and on demand

## Pipeline Stages

### CI Pipeline Jobs

| Job | Purpose | Triggers |
|-----|---------|----------|
| `quality` | Python linting (ruff, black, isort, mypy) | PR, Push |
| `frontend-quality` | TypeScript linting (ESLint, type-check) | PR, Push |
| `python-test` | Django tests with MySQL and Redis | PR, Push |
| `frontend-test` | React/Vitest tests | PR, Push |
| `docker` | Build & push Docker image, Trivy scan | Push to main |
| `security` | Bandit, Safety, Gitleaks scans | PR, Push |
| `summary` | Build summary report | Always |

### CD Pipeline Jobs

| Job | Purpose | Triggers |
|-----|---------|----------|
| `deploy-staging` | Deploy to staging environment | Push to main |
| `deploy-production` | Deploy to production (requires approval) | Release tags |
| `rollback` | Rollback to previous version | Manual |
| `smoke-tests` | Verify deployment health | After production deploy |
| `backup` | Create database backup | After production deploy |

## Setup Instructions

### 1. Repository Secrets

Add the following secrets to your GitHub repository:

#### Docker Hub
- `DOCKERHUB_USERNAME`: Your Docker Hub username
- `DOCKERHUB_TOKEN`: Docker Hub access token (not password)

#### Staging Server
- `STAGING_HOST`: Staging server IP or hostname
- `STAGING_USER`: SSH user for staging server
- `STAGING_SSH_KEY`: Private SSH key for staging server

#### Production Server
- `PRODUCTION_HOST`: Production server IP or hostname
- `PRODUCTION_USER`: SSH user for production server
- `PRODUCTION_SSH_KEY`: Private SSH key for production server

#### Notifications (Optional)
- `SLACK_WEBHOOK_URL`: Slack webhook URL for deployment notifications

### 2. GitHub Environments

Create the following environments in GitHub:

#### Staging
- **Protection rules**: None (optional)
- **Environment variables**: Add `DJANGO_SETTINGS_MODULE=local_settings`

#### Production
- **Protection rules**: Require approval from selected reviewers
- **Environment variables**: Add `DJANGO_SETTINGS_MODULE=local_settings`

### 3. Server Setup

On your staging/production servers:

```bash
# Create project directory
mkdir -p /data/wwwroot/liang_ba
cd /data/wwwroot/liang_ba

# Clone repository (or pull latest)
git clone <repository-url> .

# Create .env file
cp .env.prod.example .env
# Edit .env with your values

# Create required directories
mkdir -p logs static media backups

# Start services
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

### 4. Database Setup

```bash
# Run initial migrations
docker compose -f docker-compose.prod.yml exec -T web python manage.py migrate

# Create superuser
docker compose -f docker-compose.prod.yml exec -T web python manage.py createsuperuser

# Collect static files
docker compose -f docker-compose.prod.yml exec -T web python manage.py collectstatic --noinput
```

## Local Development

### Pre-commit Hooks

Install and configure pre-commit:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Update hooks
pre-commit autoupdate
```

### Running Tests Locally

#### Python Tests
```bash
# Install test dependencies
pip install pytest pytest-django pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=apps --cov-report=html
```

#### Frontend Tests
```bash
cd admin

# Install dependencies
npm ci

# Run tests
npm run test

# Run with coverage
npm run test:coverage
```

### Docker Build

```bash
# Build production image
docker build -t liang-ba:latest -f Dockerfile.prod .

# Run locally
docker compose -f docker-compose.prod.yml up -d
```

## Pipeline Configuration

### CI Workflow

The CI pipeline runs:
1. **Quality checks** (Python & Frontend)
2. **Tests** (Python & Frontend)
3. **Docker build** (on main branch push)
4. **Security scans** (Trivy, Bandit, Safety, Gitleaks)

### CD Workflow

The CD pipeline:
1. **Deploys to staging** automatically on push to main
2. **Waits for approval** for production deployment
3. **Deploys to production** on release tags
4. **Runs smoke tests** after deployment
5. **Creates database backup** after successful deployment

## Troubleshooting

### CI Pipeline Fails

1. **Check logs**: View GitHub Actions logs for detailed error messages
2. **Database issues**: Ensure MySQL and Redis services are running
3. **Docker build fails**: Check Dockerfile.prod syntax

### Deployment Fails

1. **SSH connection**: Verify SSH key and server access
2. **Docker images**: Ensure Docker Hub credentials are correct
3. **Health check fails**: Check application logs on server:
   ```bash
   docker compose -f docker-compose.prod.yml logs --tail=100 web
   ```

### Rollback

To rollback to a previous version:

```bash
# Via GitHub Actions
# 1. Go to Actions > CD Pipeline
# 2. Click "Run workflow"
# 3. Select "rollback: true"
# 4. Click "Run workflow"

# Manual rollback
ssh user@server
cd /data/wwwroot/liang_ba
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d
```

## Security Considerations

- **Secrets**: Never commit secrets to the repository
- **Docker**: Use Trivy to scan images for vulnerabilities
- **Dependencies**: Run `safety check` and `pip-audit` regularly
- **Code Review**: Require PR reviews before merging

## Monitoring

### Health Check Endpoints
- `/health`: Application health check (returns 200 if healthy)

### Logs
- **Application**: `/data/wwwroot/liang_ba/logs/`
- **Docker**: `docker compose -f docker-compose.prod.yml logs`

### Monitoring Tools
- Set up monitoring (e.g., Prometheus, Grafana)
- Configure alerts for deployment failures
- Monitor Docker container health
