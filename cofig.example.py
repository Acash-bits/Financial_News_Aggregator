"""
Configuration Template for Financial News Aggregator
Copy this file to config.py and fill in your actual credentials
"""

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'your_mysql_username',
    'password': 'your_mysql_password',
    'database': 'lks_company',
    'autocommit': False,
    'use_unicode': True,
    'charset': 'utf8mb4'
}

# Email Configuration
EMAIL_CONFIG = {
    'smtp_server': 'smtp.office365.com',
    'smtp_port': 587,
    'sender_email': 'your_email@company.com',
    'sender_password': 'your_email_password',
    'recipient_emails': [
        'recipient1@company.com',
        'recipient2@company.com'
    ],
    'cc_emails': [
        'cc1@company.com',
        'cc2@company.com'
    ],
    'subject': 'IPO & M&A News Alert'
}

# Scraper Configuration
SCRAPER_CONFIG = {
    'scrape_interval_minutes': 90,  # Time between scraping cycles
    'request_timeout': 15,  # Timeout for HTTP requests (seconds)
    'batch_pause_seconds': 30,  # Pause after every 10 articles
    'site_pause_seconds': 2,  # Pause between different websites
}

# Logging Configuration
LOGGING_CONFIG = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    'log_file': 'scraper.log',
    'max_log_size_mb': 10,
    'backup_count': 5
}

# Advanced Options (Optional)
ADVANCED_CONFIG = {
    'enable_proxy': False,
    'proxy_url': 'http://proxy.company.com:8080',
    'max_retries': 3,
    'enable_notifications': True
}