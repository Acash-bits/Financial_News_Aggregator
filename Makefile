# Financial News Aggregator - Makefile
# ======================================
# Quick commands for common tasks

.PHONY: help install setup run-scraper run-email test lint format clean docker-up docker-down backup

# Default target
.DEFAULT_GOAL := help

# Colors for output
COLOR_RESET = \033[0m
COLOR_BOLD = \033[1m
COLOR_GREEN = \033[32m
COLOR_YELLOW = \033[33m
COLOR_BLUE = \033[34m

# Variables
PYTHON := python3
PIP := pip3
VENV := venv
DB_NAME := lks_company

## help: Show this help message
help:
	@echo "$(COLOR_BOLD)Financial News Aggregator - Available Commands$(COLOR_RESET)"
	@echo ""
	@sed -n 's/^##//p' ${MAKEFILE_LIST} | column -t -s ':' | sed -e 's/^/ /'
	@echo ""

## install: Install Python dependencies
install:
	@echo "$(COLOR_GREEN)Installing dependencies...$(COLOR_RESET)"
	$(PIP) install -r requirements.txt
	@echo "$(COLOR_GREEN)✓ Dependencies installed$(COLOR_RESET)"

## setup: Complete setup (venv, dependencies, config, database)
setup:
	@echo "$(COLOR_GREEN)Setting up project...$(COLOR_RESET)"
	@if [ ! -d "$(VENV)" ]; then \
		echo "Creating virtual environment..."; \
		$(PYTHON) -m venv $(VENV); \
	fi
	@echo "Activating virtual environment and installing dependencies..."
	@. $(VENV)/bin/activate && $(PIP) install -r requirements.txt
	@if [ ! -f "config.py" ]; then \
		echo "Creating config.py from example..."; \
		cp config.example.py config.py; \
		echo "$(COLOR_YELLOW)⚠ Please edit config.py with your credentials$(COLOR_RESET)"; \
	fi
	@if [ ! -f ".env" ]; then \
		echo "Creating .env from example..."; \
		cp .env.example .env; \
		echo "$(COLOR_YELLOW)⚠ Please edit .env with your credentials$(COLOR_RESET)"; \
	fi
	@echo "$(COLOR_GREEN)✓ Setup complete$(COLOR_RESET)"

## db-setup: Initialize database
db-setup:
	@echo "$(COLOR_GREEN)Setting up database...$(COLOR_RESET)"
	mysql -u root -p < database/setup.sql
	@echo "$(COLOR_GREEN)✓ Database initialized$(COLOR_RESET)"

## run-scraper: Run the news scraper
run-scraper:
	@echo "$(COLOR_BLUE)Starting news scraper...$(COLOR_RESET)"
	$(PYTHON) Ipo_tracker.py

## run-email: Run the email agent
run-email:
	@echo "$(COLOR_BLUE)Running email agent...$(COLOR_RESET)"
	$(PYTHON) mail_sending_agent.py

## test: Run all tests
test:
	@echo "$(COLOR_GREEN)Running tests...$(COLOR_RESET)"
	pytest -v --cov=. --cov-report=html --cov-report=term
	@echo "$(COLOR_GREEN)✓ Tests complete. Coverage report: htmlcov/index.html$(COLOR_RESET)"

## lint: Run code linting
lint:
	@echo "$(COLOR_GREEN)Running linters...$(COLOR_RESET)"
	flake8 --max-line-length=100 *.py
	@echo "$(COLOR_GREEN)✓ Linting complete$(COLOR_RESET)"

## format: Format code with black
format:
	@echo "$(COLOR_GREEN)Formatting code...$(COLOR_RESET)"
	black --line-length=100 *.py
	@echo "$(COLOR_GREEN)✓ Code formatted$(COLOR_RESET)"

## check: Run all checks (lint, format-check, test)
check:
	@echo "$(COLOR_GREEN)Running all checks...$(COLOR_RESET)"
	@$(MAKE) lint
	@black --check --line-length=100 *.py
	@$(MAKE) test
	@echo "$(COLOR_GREEN)✓ All checks passed$(COLOR_RESET)"

## docker-up: Start Docker containers
docker-up:
	@echo "$(COLOR_BLUE)Starting Docker containers...$(COLOR_RESET)"
	docker-compose up -d
	@echo "$(COLOR_GREEN)✓ Containers started$(COLOR_RESET)"
	@docker-compose ps

## docker-down: Stop Docker containers
docker-down:
	@echo "$(COLOR_YELLOW)Stopping Docker containers...$(COLOR_RESET)"
	docker-compose down
	@echo "$(COLOR_GREEN)✓ Containers stopped$(COLOR_RESET)"

## docker-logs: View Docker logs
docker-logs:
	docker-compose logs -f

## docker-rebuild: Rebuild Docker images
docker-rebuild:
	@echo "$(COLOR_BLUE)Rebuilding Docker images...$(COLOR_RESET)"
	docker-compose build --no-cache
	@echo "$(COLOR_GREEN)✓ Images rebuilt$(COLOR_RESET)"

## backup: Backup database
backup:
	@echo "$(COLOR_GREEN)Creating database backup...$(COLOR_RESET)"
	@mkdir -p backups
	mysqldump -u root -p $(DB_NAME) > backups/backup_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(COLOR_GREEN)✓ Backup created in backups/$(COLOR_RESET)"

## restore: Restore database from backup (specify FILE=path/to/backup.sql)
restore:
	@if [ -z "$(FILE)" ]; then \
		echo "$(COLOR_YELLOW)Usage: make restore FILE=backups/backup_20251108.sql$(COLOR_RESET)"; \
		exit 1; \
	fi
	@echo "$(COLOR_YELLOW)Restoring database from $(FILE)...$(COLOR_RESET)"
	mysql -u root -p $(DB_NAME) < $(FILE)
	@echo "$(COLOR_GREEN)✓ Database restored$(COLOR_RESET)"

## logs: View application logs
logs:
	@if [ -f "scraper.log" ]; then \
		tail -f scraper.log; \
	else \
		echo "$(COLOR_YELLOW)No log file found$(COLOR_RESET)"; \
	fi

## clean: Clean up generated files
clean:
	@echo "$(COLOR_YELLOW)Cleaning up...$(COLOR_RESET)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf htmlcov/ .coverage .pytest_cache/ *.egg-info/ 2>/dev/null || true
	@echo "$(COLOR_GREEN)✓ Cleanup complete$(COLOR_RESET)"

## clean-all: Clean everything including venv and database
clean-all: clean
	@echo "$(COLOR_YELLOW)Performing deep clean...$(COLOR_RESET)"
	rm -rf $(VENV)/ 2>/dev/null || true
	@echo "$(COLOR_YELLOW)⚠ Note: Database not deleted. Use 'make db-drop' if needed$(COLOR_RESET)"
	@echo "$(COLOR_GREEN)✓ Deep clean complete$(COLOR_RESET)"

## db-drop: Drop database (WARNING: Destructive)
db-drop:
	@echo "$(COLOR_YELLOW)⚠ WARNING: This will delete all data!$(COLOR_RESET)"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		mysql -u root -p -e "DROP DATABASE IF EXISTS $(DB_NAME);"; \
		echo "$(COLOR_GREEN)✓ Database dropped$(COLOR_RESET)"; \
	else \
		echo "Cancelled"; \
	fi

## status: Check system status
status:
	@echo "$(COLOR_BOLD)System Status$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_BLUE)Python Version:$(COLOR_RESET)"
	@$(PYTHON) --version
	@echo ""
	@echo "$(COLOR_BLUE)MySQL Status:$(COLOR_RESET)"
	@systemctl is-active mysql 2>/dev/null || echo "Not running or not using systemd"
	@echo ""
	@echo "$(COLOR_BLUE)Virtual Environment:$(COLOR_RESET)"
	@if [ -d "$(VENV)" ]; then echo "✓ Exists"; else echo "✗ Not created"; fi
	@echo ""
	@echo "$(COLOR_BLUE)Configuration:$(COLOR_RESET)"
	@if [ -f "config.py" ]; then echo "✓ config.py exists"; else echo "✗ config.py missing"; fi
	@if [ -f ".env" ]; then echo "✓ .env exists"; else echo "✗ .env missing"; fi
	@echo ""
	@echo "$(COLOR_BLUE)Database Connection:$(COLOR_RESET)"
	@mysql -u root -p -e "SELECT 'Connected successfully' AS Status;" 2>/dev/null || echo "✗ Cannot connect"

## dev: Setup development environment
dev: setup install
	@echo "$(COLOR_GREEN)Installing development dependencies...$(COLOR_RESET)"
	$(PIP) install pytest pytest-cov black flake8 pylint bandit
	@echo "$(COLOR_GREEN)✓ Development environment ready$(COLOR_RESET)"

## update: Update dependencies
update:
	@echo "$(COLOR_GREEN)Updating dependencies...$(COLOR_RESET)"
	$(PIP) install --upgrade -r requirements.txt
	@echo "$(COLOR_GREEN)✓ Dependencies updated$(COLOR_RESET)"
	@echo "$(COLOR_YELLOW)Run 'pip list --outdated' to check for more updates$(COLOR_RESET)"