# Quick Start Guide

Get your Financial News Aggregator up and running in under 10 minutes! 🚀

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Python 3.7 or higher installed
- [ ] MySQL 5.7 or higher installed and running
- [ ] Git installed
- [ ] Email account with SMTP access (Office365, Gmail, etc.)
- [ ] 5-10 minutes of your time

## Installation Methods

Choose your preferred installation method:

### Option 1: Quick Install (Recommended for Beginners)

```bash
# 1. Clone the repository
git clone https://github.com/Acash-bits/financial-news-aggregator.git
cd financial-news-aggregator

# 2. Run the automated setup
make setup
make db-setup

# 3. Edit configuration files
nano config.py  # Add your database and email credentials

# 4. Start scraping!
make run-scraper
```

### Option 2: Manual Install (Step-by-Step)

```bash
# 1. Clone repository
git clone https://github.com/Acash-bits/financial-news-aggregator.git
cd financial-news-aggregator

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup configuration
cp config.example.py config.py
cp .env.example .env

# Edit config.py and .env with your credentials
nano config.py
nano .env

# 5. Setup database
mysql -u root -p < database/setup.sql

# 6. Run the scraper
python Ipo_tracker.py
```

### Option 3: Docker Install (For Advanced Users)

```bash
# 1. Clone repository
git clone https://github.com/Acash-bits/financial-news-aggregator.git
cd financial-news-aggregator

# 2. Configure environment
cp .env.example .env
nano .env  # Add your credentials

# 3. Start everything with Docker
docker-compose up -d

# 4. View logs
docker-compose logs -f
```

## Configuration Guide

### Step 1: Database Configuration

Edit `config.py`:

```python
DB_CONFIG = {
    'host': 'localhost',           # Your MySQL host
    'user': 'root',                # Your MySQL username
    'password': 'YOUR_PASSWORD',   # ⚠️ Change this!
    'database': 'lks_company',
    'autocommit': False,
    'use_unicode': True,
    'charset': 'utf8mb4'
}
```

### Step 2: Email Configuration

Edit `config.py`:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.office365.com',
    'smtp_port': 587,
    'sender_email': 'your_email@company.com',      # ⚠️ Change this!
    'sender_password': 'YOUR_EMAIL_PASSWORD',      # ⚠️ Change this!
    'recipient_emails': [
        'recipient1@company.com',                   # ⚠️ Change this!
        'recipient2@company.com'
    ],
    'cc_emails': [
        'cc1@company.com'
    ]
}
```

### Step 3: Test Your Setup

```bash
# Test database connection
mysql -u root -p -e "USE lks_company; SELECT COUNT(*) FROM IPO_Scraped_Articles;"

# Test scraper (will run once and exit with Ctrl+C)
python Ipo_tracker.py

# Test email (sends email for any unsent articles)
python mail_sending_agent.py
```

## First Run

When you run the scraper for the first time:

1. **It will connect to all 7 news websites**
2. **Scrape hundreds of articles**
3. **Filter for relevant IPO/M&A/Demerger content**
4. **Insert new articles into database**
5. **Wait 90 minutes and repeat**

Expected output:
```
Database connection successful.
Loaded 0 existing articles from database.

--- Scraping MoneyControl ---
Found 45 raw articles from MoneyControl
MoneyControl: Processed=45, Relevant=3, Duplicates=0, Relevant_but_Excluded=1

--- Scraping ZeeBiz Economy ---
Found 38 raw articles from ZeeBiz Economy
...

--- Scraping Summary ---
Total processed: 342
Total relevant: 12
Total duplicates skipped: 0
Total relevant but excluded: 4
New articles to insert: 12

Insertion complete: 12 successful, 0 failed
```

## Scheduling (Production)

### Using Cron (Linux/Mac)

```bash
# Edit crontab
crontab -e

# Add these lines:

# Run scraper on system startup
@reboot cd /path/to/financial-news-aggregator && /path/to/venv/bin/python Ipo_tracker.py

# Run email agent every 2 hours
0 */2 * * * cd /path/to/financial-news-aggregator && /path/to/venv/bin/python mail_sending_agent.py
```

### Using Systemd (Linux)

Create `/etc/systemd/system/financial-scraper.service`:

```ini
[Unit]
Description=Financial News Scraper
After=network.target mysql.service

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/financial-news-aggregator
ExecStart=/path/to/venv/bin/python Ipo_tracker.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable financial-scraper
sudo systemctl start financial-scraper
sudo systemctl status financial-scraper
```

### Using Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger: "When the computer starts"
4. Action: Start a program
5. Program: `C:\path\to\python.exe`
6. Arguments: `C:\path\to\Ipo_tracker.py`
7. Start in: `C:\path\to\financial-news-aggregator`

## Verification

### Check if Everything is Working

```bash
# 1. Check database has articles
mysql -u root -p -e "USE lks_company; SELECT COUNT(*) as total_articles FROM IPO_Scraped_Articles;"

# 2. Check recent articles
mysql -u root -p -e "USE lks_company; SELECT * FROM IPO_Scraped_Articles ORDER BY id DESC LIMIT 5;"

# 3. Check logs
tail -f logs/scraper.log

# 4. Check for unsent emails
mysql -u root -p -e "USE lks_company; SELECT COUNT(*) as pending FROM IPO_Scraped_Articles WHERE sent_status = FALSE;"
```

### Expected Results

✅ **Successful Setup:**
- Database connection works
- Articles are being scraped (check database count)
- Logs show "Scraper run completed"
- No error messages in logs

❌ **Common Issues:**

| Problem | Solution |
|---------|----------|
| "Database connection error" | Check MySQL is running: `sudo systemctl status mysql` |
| "No articles found" | Websites might be down, check internet connection |
| "Email sending failed" | Verify SMTP credentials and firewall settings |
| "Permission denied" | Check file permissions: `chmod 755 Ipo_tracker.py` |
| "Module not found" | Install dependencies: `pip install -r requirements.txt` |

## Monitoring

### View Real-Time Logs

```bash
# Scraper logs
tail -f logs/scraper.log

# Docker logs
docker-compose logs -f scraper

# Systemd logs
sudo journalctl -u financial-scraper -f
```

### Check Statistics

```bash
# Using Makefile
make status

# Manual queries
mysql -u root -p lks_company -e "
SELECT 
    Website, 
    COUNT(*) as articles,
    SUM(CASE WHEN sent_status = TRUE THEN 1 ELSE 0 END) as sent
FROM IPO_Scraped_Articles
GROUP BY Website;
"
```

## Customization

### Change Scraping Interval

Edit `Ipo_tracker.py`:
```python
wait_minutes = 90  # Change to your desired interval (in minutes)
```

### Add/Remove Websites

Edit `Ipo_tracker.py`, modify the `self.urls` dictionary:
```python
self.urls = {
    'MoneyControl': 'https://www.moneycontrol.com/news',
    # Add your website here:
    'YourSite': 'https://example.com/news',
}
```

### Modify Keywords

Edit `Ipo_tracker.py`, update `self.keyword_mapping`:
```python
self.keyword_mapping = {
    "IPO": ["IPO", "Initial Public Offering"],
    "M&A": ["M&A", "Merger", "Acquisition"],
    # Add more categories:
    "Investment": ["Investment", "Funding", "Series A"],
}
```

### Change Email Recipients

Edit `config.py`:
```python
EMAIL_CONFIG = {
    'recipient_emails': [
        'new_recipient@company.com',  # Add/modify recipients
    ],
    'cc_emails': [
        'new_cc@company.com',
    ]
}
```

## Backup & Restore

### Create Backup

```bash
# Using Makefile
make backup

# Manual
mysqldump -u root -p lks_company > backup_$(date +%Y%m%d).sql
```

### Restore from Backup

```bash
# Using Makefile
make restore FILE=backups/backup_20251108.sql

# Manual
mysql -u root -p lks_company < backups/backup_20251108.sql
```

## Updating

### Update Code

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Restart services
sudo systemctl restart financial-scraper

# Or with Docker
docker-compose down
docker-compose up -d --build
```

## Performance Optimization

### For High Volume

If scraping many websites:

1. **Increase database connection pool:**
```python
db_config = {
    'pool_size': 10,
    'max_overflow': 20,
}
```

2. **Adjust rate limiting:**
```python
SCRAPER_CONFIG = {
    'batch_pause_seconds': 15,  # Reduce from 30
    'site_pause_seconds': 1,    # Reduce from 2
}
```

3. **Enable MySQL query cache:**
```sql
SET GLOBAL query_cache_size = 67108864;  -- 64MB
SET GLOBAL query_cache_type = ON;
```

## Security Best Practices

1. **Never commit credentials:**
   - Always use `.env` and `config.py`
   - Add them to `.gitignore`

2. **Use environment variables:**
   ```bash
   export DB_PASSWORD="your_password"
   export EMAIL_PASSWORD="your_email_password"
   ```

3. **Restrict file permissions:**
   ```bash
   chmod 600 config.py .env
   chmod 600 backups/*.sql
   ```

4. **Regular updates:**
   ```bash
   pip list --outdated
   pip install --upgrade package_name
   ```

## Getting Help

### Documentation
- 📖 [README.md](README.md) - Full documentation
- 🏗️ [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- 📝 [CHANGELOG.md](CHANGELOG.md) - Version history

### Support Channels
- 🐛 [GitHub Issues](https://github.com/Acash-bits/financial-news-aggregator/issues)
- 💬 Email: akash.saxena@lakshmisri.com

### Common Commands

```bash
make help          # Show all available commands
make status        # Check system status
make logs          # View logs
make backup        # Create database backup
make test          # Run tests
make clean         # Clean temporary files
```

## Next Steps

After successful setup:

1. ✅ Monitor logs for first few runs
2. ✅ Verify email notifications work
3. ✅ Set up automated backups
4. ✅ Configure monitoring/alerts
5. ✅ Customize keywords for your needs
6. ✅ Add more news sources if needed

---

**Congratulations! Your Financial News Aggregator is now running! 🎉**

For detailed information, refer to the [full README](README.md).