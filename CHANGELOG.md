# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Add more news sources (Business Standard, Financial Express)
- Implement machine learning for better categorization
- Create web dashboard for article management
- Add Telegram/Slack notifications
- Implement full-text article extraction

---

## [1.0.0] - 2025-11-08

### Added
- Initial release of Financial News Aggregator
- Multi-source web scraping for 7 news websites
- Intelligent keyword matching with exact word boundaries
- Duplicate detection using normalized titles and URLs
- Category classification (IPO, M&A, Demerger)
- Exclusion filter for irrelevant content
- MySQL database integration for article storage
- Automated email notifications via SMTP
- HTML-formatted email digests
- Continuous scraping with 90-minute intervals
- Comprehensive error handling and auto-reconnection
- Rate limiting to respect server resources
- Batch processing for database efficiency

### Supported Websites
- MoneyControl
- ZeeBiz (Economy & General)
- Economic Times
- MNA Critique
- Entrackr
- Livemint

### Features
- **Scraper (`Ipo_tracker.py`)**
  - Real-time article discovery
  - Multi-selector fallback strategy
  - Normalization for consistent comparison
  - Relevant-but-excluded article tracking
  - Detailed logging and statistics

- **Email Agent (`mail_sending_agent.py`)**
  - HTML table formatting
  - Multiple recipients (To + CC)
  - Automatic status tracking
  - Office365 SMTP integration

---

## [0.5.0] - 2025-10-15 (Beta)

### Added
- Basic scraping functionality for 3 websites
- Simple keyword matching
- Database storage
- Email notifications

### Known Issues
- Duplicate articles not properly filtered
- No exclusion keywords implemented
- Limited error handling

---

## [0.1.0] - 2025-09-01 (Alpha)

### Added
- Proof of concept
- Single website scraping (MoneyControl)
- Basic MySQL integration
- Manual email sending

---

## Version History Summary

| Version | Date | Key Features |
|---------|------|--------------|
| 1.0.0 | 2025-11-08 | Full production release with 7 websites |
| 0.5.0 | 2025-10-15 | Beta with 3 websites |
| 0.1.0 | 2025-09-01 | Initial alpha prototype |

---

## Migration Guide

### Upgrading from 0.5.0 to 1.0.0

**Database Changes:**
```sql
-- Add new index for performance
ALTER TABLE IPO_Scraped_Articles 
ADD INDEX idx_keyword (Keyword);

-- Add inserted_at column if not exists
ALTER TABLE IPO_Scraped_Articles 
ADD COLUMN inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
```

**Configuration Changes:**
- Update `db_config` to include `charset: 'utf8mb4'`
- Review and update exclusion keywords list
- Add new website URLs to configuration

**Code Changes:**
- Replace old keyword matching with new exact word boundary matching
- Update email formatting to HTML table format
- Implement new error handling patterns

---

## Contributors

- Akash Saxena - Initial development and maintenance
- Lakshmikumaran & Sridharan Attorneys - Project sponsorship

---

## Support

For issues or questions about specific versions, please check:
- [GitHub Issues](https://github.com/Acash-bits/financial-news-aggregator/issues)
- [Documentation](https://github.com/Acash-bits/financial-news-aggregator/wiki)

---

[Unreleased]: https://github.com/Acash-bits/financial-news-aggregator/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Acash-bits/financial-news-aggregator/releases/tag/v1.0.0
[0.5.0]: https://github.com/Acash-bits/financial-news-aggregator/releases/tag/v0.5.0
[0.1.0]: https://github.com/Acash-bits/financial-news-aggregator/releases/tag/v0.1.0