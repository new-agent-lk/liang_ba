# Makefile for liang-ba project

.PHONY: help install dev-install test test-coverage lint lint-fix format check-format \
	docker-build docker-up docker-down docker-logs docker-logs-web docker-logs-db \
	deploy-staging deploy-production backup migrate rollbacks \
	install-pre-commit run-pre-commit clean clean-py clean-node clean-docker

# Colors
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[0;33m
NC = \033[0m # No Color

# Default target
help:
	@echo "Available commands:"
	@echo ""
	@echo "Installation:"
	@echo "  install           Install all dependencies"
	@echo "  dev-install       Install development dependencies"
	@echo ""
	@echo "Testing:"
	@echo "  test              Run Python tests"
	@echo "  test-coverage     Run tests with coverage report"
	@echo "  test-frontend     Run frontend tests"
	@echo ""
	@echo "Code Quality:"
	@echo "  lint              Run all linters"
	@echo "  lint-fix          Run linters with auto-fix"
	@echo "  format            Format code"
	@echo "  check-format      Check code formatting"
	@echo ""
	@echo "Docker:"
	@echo "  docker-build      Build Docker images"
	@echo "  docker-up         Start Docker containers"
	@echo "  docker-down       Stop Docker containers"
	@echo "  docker-logs       Show all container logs"
	@echo "  docker-logs-web   Show web container logs"
	@echo "  docker-logs-db    Show database logs"
	@echo "  docker-restart    Restart containers"
	@echo ""
	@echo "Database:"
	@echo "  migrate           Run database migrations"
	@echo "  backup            Create database backup"
	@echo ""
	@echo "Deployment:"
	@echo "  deploy-staging    Deploy to staging (requires SSH config)"
	@echo "  deploy-production Deploy to production (requires SSH config)"
	@echo ""
	@echo "Pre-commit:"
	@echo "  install-pre-commit Install pre-commit hooks"
	@echo "  run-pre-commit    Run pre-commit on all files"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean             Clean all temporary files"
	@echo "  clean-py          Clean Python cache files"
	@echo "  clean-node        Clean node_modules and build files"
	@echo "  clean-docker      Clean Docker resources"
	@echo ""

# Installation
install:
	@echo "$(GREEN)Installing Python dependencies...$(NC)"
	pip install -r requirements.txt

dev-install:
	@echo "$(GREEN)Installing development dependencies...$(NC)"
	pip install -r requirements-dev.txt

# Testing
test:
	@echo "$(GREEN)Running Python tests...$(NC)"
	pytest -v --tb=short

test-coverage:
	@echo "$(GREEN)Running tests with coverage...$(NC)"
	pytest --cov=apps --cov-report=term-missing --cov-report=html
	@echo "$(GREEN)Coverage report generated in htmlcov/$(*).html$(NC)"

test-frontend:
	@echo "$(GREEN)Running frontend tests...$(NC)"
	cd admin && npm run test:run

# Code Quality
lint:
	@echo "$(GREEN)Running linters...$(NC)"
	@echo "Python linting..."
	ruff check .
	@echo "Type checking..."
	mypy apps liang_ba --ignore-missing-imports
	@echo "Frontend linting..."
	cd admin && npm run lint

lint-fix:
	@echo "$(GREEN)Running linters with auto-fix...$(NC)"
	ruff check --fix .
	ruff format .
	black .
	isort --profile black .
	cd admin && npm run lint:fix

format:
	@echo "$(GREEN)Formatting code...$(NC)"
	ruff format .
	black .
	isort --profile black .
	cd admin && npm run lint:fix

check-format:
	@echo "$(GREEN)Checking code formatting...$(NC)"
	@echo "Ruff format..."
	ruff format --check .
	@echo "Black format..."
	black --check .
	@echo "isort..."
	isort --check-only --profile black .
	cd admin && npm run lint

# Docker
docker-build:
	@echo "$(GREEN)Building Docker images...$(NC)"
	docker build -t liang-ba:latest -f Dockerfile .
	docker build -t liang-ba:prod -f Dockerfile.prod .

docker-up:
	@echo "$(GREEN)Starting Docker containers...$(NC)"
	docker compose up -d

docker-down:
	@echo "$(GREEN)Stopping Docker containers...$(NC)"
	docker compose down

docker-restart:
	@echo "$(GREEN)Restarting Docker containers...$(NC)"
	docker compose restart

docker-logs:
	@echo "$(GREEN)Showing container logs...$(NC)"
	docker compose logs -f

docker-logs-web:
	@echo "$(GREEN)Showing web container logs...$(NC)"
	docker compose logs -f web

docker-logs-db:
	@echo "$(GREEN)Showing database logs...$(NC)"
	docker compose logs -f db

# Database
migrate:
	@echo "$(GREEN)Running database migrations...$(NC)"
	python manage.py migrate

backup:
	@echo "$(GREEN)Creating database backup...$(NC)"
	@read -p "Enter backup filename: " filename; \
	docker compose exec -T db mysqldump -u root -prootpass liang_ba > backups/$$filename.sql

# Deployment
deploy-staging:
	@echo "$(GREEN)Deploying to staging...$(NC)"
	@echo "This requires SSH access to staging server"
	@read -p "Continue? (y/n) " -n 1 -r; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		scp -r docker-compose.prod.yml .env $$(whoami)@staging:/data/wwwroot/liang_ba/; \
		ssh $$(whoami)@staging "cd /data/wwwroot/liang_ba && docker compose pull && docker compose up -d"; \
	fi

deploy-production:
	@echo "$(RED)Deploying to production...$(NC)"
	@echo "This requires SSH access to production server"
	@read -p "Enter version tag (e.g., v1.0.0): " version; \
	if [[ ! $$version =~ ^v[0-9]+\.[0-9]+\.[0-9]+$$ ]]; then \
		echo "$(RED)Invalid version format. Use vX.Y.Z$(NC)"; \
		exit 1; \
	fi; \
	scp -r docker-compose.prod.yml .env $$(whoami)@production:/data/wwwroot/liang_ba/; \
	ssh $$(whoami)@production "cd /data/wwwroot/liang_ba && \
		docker tag liang-ba:latest liang-ba:$$version && \
		docker push liang-ba:$$version && \
		docker compose pull && \
		docker compose up -d"

# Pre-commit
install-pre-commit:
	@echo "$(GREEN)Installing pre-commit hooks...$(NC)"
	pre-commit install

run-pre-commit:
	@echo "$(GREEN)Running pre-commit on all files...$(NC)"
	pre-commit run --all-files

# Cleanup
clean:
	@echo "$(GREEN)Cleaning all temporary files...$(NC)"
	make clean-py
	make clean-node
	rm -rf htmlcov .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true

clean-py:
	@echo "$(GREEN)Cleaning Python cache...$(NC)"
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	rm -rf .coverage htmlcov

clean-node:
	@echo "$(GREEN)Cleaning node modules and builds...$(NC)"
	rm -rf admin/node_modules admin/dist admin/coverage

clean-docker:
	@echo "$(GREEN)Cleaning Docker resources...$(NC)"
	docker system prune -af
	docker volume prune -f
