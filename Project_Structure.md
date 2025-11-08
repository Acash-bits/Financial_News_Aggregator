# Project Structure

Complete directory structure and file organization for the Financial News Aggregator project.

```
financial-news-aggregator/
│
├── .github/                          # GitHub specific files
│   └── workflows/
│       └── ci.yml                    # CI/CD pipeline configuration
│
├── database/                         # Database related files
│   ├── setup.sql                     # Initial database schema
│   └── migrations/                   # Database migration scripts (future)
│
├── docs/                             # Documentation
│   ├── API.md                        # API documentation (future)
│   ├── ARCHITECTURE.md               # Architecture details
│   └── DEPLOYMENT.md                 # Deployment guide
│
├── logs/                             # Application logs (gitignored)
│   ├── scraper.log
│   └── email.log
│
├── tests/                            # Test files
│   ├── __init__.py
│   ├── test_scraper.py              # Scraper unit tests
│   ├── test_email_agent.py          # Email agent tests
│   ├── test_integration.py          # Integration tests
│   └── fixtures/                     # Test data
│       ├── sample_html/
│       └── sample_data.json
│
├── backups/                          # Database backups (gitignored)
│   └── backup_YYYYMMDD_HHMMSS.sql
│
├── .gitignore                        # Git ignore rules
├── .env.example                      # Environment variables template
├── .env                              # Actual environment variables (gitignored)
│
├── requirements.txt                  # Python dependencies
├── requirements-dev.txt              # Development dependencies
│
├── config.example.py                 # Configuration template
├── config.py                         # Actual configuration (gitignored)
│
├── Dockerfile                        # Docker container definition
├── docker-compose.yml                # Docker Compose configuration
├── .dockerignore                     # Docker ignore rules
│
├── Makefile                          # Quick command shortcuts
│
├── Ipo_tracker.py                    # Main scraper script
├── mail_sending_agent.py             # Email notification script
│
├── README.md                         # Project documentation
├── CHANGELOG.md                      # Version history
├── CONTRIBUTING.md                   # Contribution guidelines
├── LICENSE                           # License information
├── PROJECT_STRUCTURE.md              # This file
│
└── .vscode/                          # VS Code settings (optional)
    ├── settings.json
    ├── launch.json
    └── extensions.json
```

## File Descriptions

### Root Level Files

| File | Purpose | Required |
|------|---------|----------|
| `Ipo_tracker.py` | Main scraper application | ✅ Yes |
| `mail_sending_agent.py` | Email notification sender | ✅ Yes |
| `requirements.txt` | Python package dependencies | ✅ Yes |
| `README.md` | Project documentation | ✅ Yes |
| `config.example.py` | Configuration template | ✅ Yes |
| `config.py` | Actual configuration (create from example) | ✅ Yes |
| `.env.example` | Environment variables template | ⚠️ Recommended |
| `.env` | Actual environment variables | ⚠️ Recommended |
| `Dockerfile` | Docker container definition | 🔵 Optional |
| `docker-compose.yml` | Multi-container orchestration | 🔵 Optional |
| `Makefile` | Command shortcuts | 🔵 Optional |
| `CHANGELOG.md` | Version history | 🔵 Optional |
| `CONTRIBUTING.md` | Contribution guidelines | 🔵 Optional |
| `LICENSE` | License information | 🔵 Optional |

### Directory Details

#### `.github/`
Contains GitHub-specific configurations:
- **workflows/ci.yml**: Automated testing and deployment pipeline
- Runs on every push and pull request
- Performs linting, testing, security scans

#### `database/`
Database-related files:
- **setup.sql**: Initial database schema and tables
- **migrations/**: Future database version updates
- Keep this separate from application code for clarity

#### `docs/` (Future)
Additional documentation:
- **API.md**: API endpoints documentation
- **ARCHITECTURE.md**: System architecture details
- **DEPLOYMENT.md**: Production deployment guide

#### `tests/`
Testing suite:
- **test_scraper.py**: Unit tests for scraping logic
- **test_email_agent.py**: Email functionality tests
- **test_integration.py**: End-to-end integration tests
- **fixtures/**: Sample HTML and test data

#### `logs/`
Application logs (auto-created):
- Rotated automatically when size limit reached
- Gitignored - not committed to repository
- Useful for debugging production issues

#### `backups/`
Database backups (auto-created):
- Created by `make backup` command
- Timestamped for easy identification
- Gitignored - stored separately or in cloud

## Setup Order

Follow this order for initial setup:

1. **Clone repository**
   ```bash
   git clone <repository-url>
   cd financial-news-aggregator
   ```

2. **Create configuration**
   ```bash
   cp config.example.py config.py
   cp .env.example .env
   # Edit both files with your credentials
   ```

3. **Setup database**
   ```bash
   mysql -u root -p < database/setup.sql
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run scraper**
   ```bash
   python Ipo_tracker.py
   ```

Or use the Makefile:
```bash
make setup
make db-setup
make run-scraper
```

## File Ownership & Permissions

Recommended permissions for production:

```bash
# Configuration files (sensitive)
chmod 600 config.py .env

# Scripts (executable)
chmod 755 Ipo_tracker.py mail_sending_agent.py

# Database files
chmod 600 database/setup.sql

# Logs directory
chmod 755 logs/
chmod 644 logs/*.log

# Backups directory
chmod 700 backups/
chmod 600 backups/*.sql
```

## Gitignore Highlights

These files are excluded from git:

```
# Sensitive
config.py
.env
*.key
*.pem

# Generated
__pycache__/
*.pyc
*.log
.coverage

# Local
venv/
logs/
backups/
```

## Docker Structure

When using Docker:

```
Container: financial_news_scraper
├── /app/                    # Working directory
│   ├── Ipo_tracker.py
│   ├── config.py           # Mounted from host
│   └── logs/               # Mounted volume
│
Container: financial_news_db
└── /var/lib/mysql/         # MySQL data directory
    └── lks_company/        # Database
```

## Development vs Production

### Development Structure
```
project/
├── venv/              # Local virtual environment
├── .env               # Local credentials
├── config.py          # Development config
└── logs/              # Local logs
```

### Production Structure
```
/opt/financial-news-aggregator/
├── .env                    # Production credentials
├── config.py               # Production config
├── logs/                   # Application logs
├── backups/               # Database backups
└── systemd/               # Service files
    ├── scraper.service
    └── email-agent.service
```

## Adding New Files

When adding new files, consider:

1. **Where does it belong?**
   - Core logic → Root directory
   - Tests → `tests/`
   - Documentation → `docs/`
   - Database → `database/`

2. **Should it be in git?**
   - Sensitive data → NO (add to .gitignore)
   - Configuration templates → YES
   - Generated files → NO

3. **Does it need special permissions?**
   - Executable scripts → `chmod +x`
   - Sensitive configs → `chmod 600`
   - Log files → `chmod 644`

## Quick Reference

| Task | File | Command |
|------|------|---------|
| Run scraper | `Ipo_tracker.py` | `python Ipo_tracker.py` |
| Send emails | `mail_sending_agent.py` | `python mail_sending_agent.py` |
| Setup DB | `database/setup.sql` | `mysql < database/setup.sql` |
| Configure | `config.py` | Edit manually |
| View logs | `logs/scraper.log` | `tail -f logs/scraper.log` |
| Backup DB | - | `make backup` |
| Run tests | `tests/` | `pytest` or `make test` |

---

**Note**: This structure may evolve as the project grows. Update this document when making significant structural changes.