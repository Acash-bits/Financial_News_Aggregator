# IPO & M&A News Tracker 📰

An automated news scraping and email notification system that monitors multiple financial news websites for IPO, M&A, and Demerger related articles. The system intelligently filters relevant content, prevents duplicates, and sends daily email digests to stakeholders.Having an interactive web-based dashboard with auto-refresh capabilities to get the visual analysis of data easily.

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [System Architecture](#️-system-architecture)
- [Analytics Dashboards](#-analytics-dashboards)
- [Technical Deep Dive](#-technical-deep-dive)
- [Installation](#-installation)
- [Configuration](#️-configuration)
- [Usage](#-usage)
- [Database Schema](#️-database-schema)
- [How It Works](#-how-it-works)
- [Website-Specific Scraping Strategies](#-website-specific-scraping-strategies)
- [Keyword Matching Logic](#-keyword-matching-logic)
- [Error Handling & Resilience](#-error-handling--resilience)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

This project consists of two main components:

1. **News Scraper** (`Ipo_tracker.py`) - Continuously monitors 7+ financial news websites for relevant articles
2. **Email Agent** (`mail_sending_agent.py`) - Sends formatted email digests of newly discovered articles
3. **Static Analytics Dashboard** (`News Scraper Analytics Dashboard.py`) - Generates comprehensive visualizations with matplotlib/seaborn
4. **Real-time Analytics Dashboard** (`Real_time_analytics_dashboard.py`) - Interactive web-based dashboard with auto-refresh capabilities

The system is designed to run 24/7, scraping news every 90 minutes and sending email notifications whenever new articles are found.

---

## ✨ Features

### Core Capabilities

- **Multi-Source Scraping**: Monitors 7 major financial news platforms
- **Intelligent Keyword Matching**: Uses exact word boundary matching to identify relevant articles
- **Advanced Filtering**: Excludes irrelevant content (sports, entertainment, advertisements, etc.)
- **Duplicate Prevention**: Tracks articles by both title and URL to avoid redundancy
- **Category Classification**: Automatically categorizes articles into IPO, M&A, or Demerger
- **Email Notifications**: Sends HTML-formatted email digests with article links
- **Database Persistence**: Stores all articles in MySQL for historical tracking
- **Auto-Reconnection**: Handles database disconnections gracefully
- **Rate Limiting**: Implements delays to respect website servers

### Analytics & Visualization Features 🆕

- **Dual Dashboard System**: Static and real-time analytics options
- **Multi-Timeframe Analysis**: Daily, weekly, monthly, and quarterly trends
- **Interactive Visualizations**: Dynamic charts with Plotly
- **Source Performance Tracking**: Monitor which sources provide the most articles
- **Keyword Distribution Analysis**: Understand topic coverage
- **Heatmap Visualizations**: Cross-analysis of sources vs keywords
- **Auto-Refresh Capability**: Real-time dashboard updates every 60 seconds
- **Export Functionality**: Save static charts as high-resolution images
- **Tabbed Interface**: Organized navigation for different analysis views


### Smart Features

- **Exclusion Tracking**: Reports relevant articles that were filtered out and why
- **Batch Processing**: Commits database records in batches for efficiency
- **Session Management**: Uses persistent HTTP sessions for better performance
- **Normalization**: Handles URL variations and text formatting inconsistencies

---

## 🗃️ System Architecture

```mermaid
graph TB
    subgraph "Data Collection Layer"
        A[News Scraper<br/>Ipo_tracker.py] --> B[MoneyControl]
        A --> C[ZeeBiz]
        A --> D[Economic Times]
        A --> E[MNA Critique]
        A --> F[Entrackr]
        A --> G[Livemint]
    end
    
    subgraph "Processing Layer"
        A --> H[Keyword Matcher]
        H --> I[Exclusion Filter]
        I --> J[Duplicate Checker]
        J --> K[Category Classifier]
    end
    
    subgraph "Storage Layer"
        K --> L[(MySQL Database<br/>IPO_Scraped_Articles)]
    end
    
    subgraph "Notification Layer"
        L --> M[Email Agent<br/>mail_sending_agent.py]
        M --> N[SMTP Server<br/>Office365]
        N --> O[Recipients]
    end
    
    subgraph "Analytics Layer 🆕"
        L --> P[Static Dashboard<br/>matplotlib/seaborn]
        L --> Q[Real-time Dashboard<br/>Dash/Plotly]
        P --> R[PNG Reports]
        Q --> S[Web Interface<br/>:8050]
    end
    
    style A fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    style M fill:#E24A4A,stroke:#8A2E2E,stroke-width:3px,color:#fff
    style L fill:#043015,stroke:#2E8A4F,stroke-width:3px,color:#fff
    style P fill:#9B59B6,stroke:#6C3483,stroke-width:3px,color:#fff
    style Q fill:#E67E22,stroke:#A04000,stroke-width:3px,color:#fff
```

---

## 📊 Analytics Dashboards

### 1. Static Analytics Dashboard (`News Scraper Analytics Dashboard.py`)

A comprehensive data visualization tool using **matplotlib** and **seaborn** for in-depth historical analysis.

#### Features:
- **Source Distribution**: Bar and pie charts showing article counts per source
- **Keyword Analysis**: Distribution of IPO, M&A, and Demerger articles
- **Daily Trends**: Line charts tracking article frequency over time
- **Weekly/Monthly/Quarterly Breakdown**: Grouped analysis by time periods
- **Comparison Dashboard**: 6-panel comprehensive view with multiple metrics
- **Heatmaps**: Cross-tabulation of sources vs keywords
- **Summary Statistics**: Automated reporting of key metrics
- **Image Export**: Save all charts as high-resolution PNG files (300 DPI)

#### Visualization Types:
```python
1. plot_source_distribution()      # Bar + Pie charts
2. plot_keyword_distribution()     # Bar + Pie charts  
3. plot_daily_trends()             # Line chart
4. plot_weekly_trends()            # Grouped bar charts
5. plot_monthly_trends()           # Grouped bar charts
6. plot_quarterly_trends()         # Grouped bar charts
7. plot_heatmap_source_keyword()   # Heatmap
8. plot_comparison_dashboard()     # 6-panel overview
```

#### Sample Output:
```
============================================================
SUMMARY STATISTICS
============================================================

Total Articles: 1,247
Date Range: 2025-01-01 to 2025-11-24
Total Days: 328

--- Top Sources ---
MoneyControl       423
Economic Times     312
ZeeBiz            189
Livemint          156
...

--- Keyword Distribution ---
M&A               687
IPO               412
Demerger          148

--- Average Articles per Day ---
3.80

--- Most Active Week ---
2025-W42: 67 articles

--- Most Active Month ---
2025-10: 198 articles
============================================================
```

---

### 2. Real-time Analytics Dashboard (`Real_time_analytics_dashboard.py`)

An **interactive web-based dashboard** built with **Dash** and **Plotly** for live monitoring.

#### Key Features:
- **Auto-Refresh**: Updates every 60 seconds automatically
- **Live Metrics**: Real-time summary cards with key statistics
- **Tabbed Navigation**: 6 organized tabs for different analyses
- **Interactive Charts**: Hover, zoom, and pan capabilities
- **Responsive Design**: Clean, modern UI with card-based layout
- **SQLAlchemy Integration**: Efficient database connection pooling

#### Dashboard Tabs:

**📈 Overview Tab**
- Source distribution (bar + donut charts)
- Keyword distribution (bar + donut charts)
- Side-by-side comparison views

**📅 Daily Analysis Tab**
- Daily article frequency trend line
- Average articles per day metric
- Interactive date-based exploration

**📊 Weekly Analysis Tab**
- Weekly trends by source (multi-line chart)
- Weekly trends by keyword (multi-line chart)
- Most active week highlight

**📆 Monthly Analysis Tab**
- Monthly articles by source (grouped bars)
- Monthly articles by keyword (grouped bars)
- Most active month metric

**📋 Quarterly Analysis Tab**
- Quarterly breakdown by source
- Quarterly breakdown by keyword
- Long-term trend visualization

**🔥 Heatmaps Tab**
- Keyword vs Source heatmap
- Source vs Keyword heatmap (reversed)
- Annotated cell values

#### Summary Cards:
```
┌─────────────┬──────────────┬─────────────┬─────────────┬─────────────┐
│ Total       │ Today's      │ This Week   │ This Month  │ Top Source  │
│ Articles    │ Articles     │             │             │             │
│ 1,247       │ 5            │ 23          │ 87          │ MoneyControl│
│ 2025-01-01  │              │             │             │             │
│ to          │              │             │             │             │
│ 2025-11-24  │              │             │             │             │
└─────────────┴──────────────┴─────────────┴─────────────┴─────────────┘
```

#### Access the Dashboard:
```bash
python Real_time_analytics_dashboard.py

# Dashboard available at:
# http://127.0.0.1:8050
# or
# http://localhost:8050
```

---


## 🔬 Technical Deep Dive

### Scraping Process Flow

```mermaid
flowchart TD
    Start([Start Scraper]) --> Init[Initialize Database Connection]
    Init --> Load[Load Existing Articles<br/>from Database]
    Load --> Loop{For Each<br/>Website}
    
    Loop -->|Next Site| Fetch[Fetch HTML Content]
    Fetch --> Parse[Parse with BeautifulSoup]
    Parse --> Extract[Extract Articles using<br/>Site-Specific Selectors]
    
    Extract --> Process{For Each<br/>Article}
    Process --> Valid{Valid Article?<br/>Title > 10 chars}
    Valid -->|No| Process
    Valid -->|Yes| Dup{Duplicate?<br/>Check Title & URL}
    
    Dup -->|Yes| Skip[Skip & Count]
    Dup -->|No| Match[Keyword Matching]
    
    Match --> Relevant{Has Relevant<br/>Keywords?}
    Relevant -->|No| Process
    Relevant -->|Yes| Exclude{Has Exclusion<br/>Keywords?}
    
    Exclude -->|Yes| Log[Log as<br/>Relevant-but-Excluded]
    Exclude -->|No| Category[Assign Category<br/>IPO/M&A/Demerger]
    
    Category --> Add[Add to Results]
    Add --> Batch{Batch Size<br/>= 10?}
    Batch -->|Yes| Pause[Pause 30 seconds]
    Batch -->|No| Process
    Pause --> Process
    Log --> Process
    Skip --> Process
    
    Process -->|More Articles| Process
    Process -->|Done| Wait[Wait 2 seconds]
    Wait --> Loop
    
    Loop -->|All Sites Done| Insert[Insert into Database]
    Insert --> Print[Print Summary Report]
    Print --> Sleep[Sleep 90 minutes]
    Sleep --> Load
    
    style Start fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
    style Insert fill:#043015,stroke:#2E8A4F,stroke-width:3px,color:#fff
    style Add fill:#043015,stroke:#2E8A4F,stroke-width:2px
    style Skip fill:#300404,stroke:#8A2E2E,stroke-width:2px
    style Log fill:#F5A623,stroke:#C17D11,stroke-width:2px
```

### Email Notification Flow

```mermaid
sequenceDiagram
    participant Timer as Scheduler
    participant Email as Email Agent
    participant DB as MySQL Database
    participant SMTP as Office365 SMTP
    participant Users as Recipients
    
    Timer->>Email: Trigger Email Check
    Email->>DB: Query unsent articles<br/>(sent_status = FALSE)
    
    alt Articles Found
        DB-->>Email: Return new articles
        Email->>Email: Format HTML Table
        Email->>SMTP: Connect & Authenticate
        SMTP-->>Email: Connection Established
        Email->>SMTP: Send Email<br/>(To + CC recipients)
        SMTP->>Users: Deliver Email
        SMTP-->>Email: Success Confirmation
        Email->>DB: UPDATE sent_status = TRUE
        DB-->>Email: Update Confirmed
    else No Articles
        DB-->>Email: Empty Result
        Email->>Email: Log "No new articles"
    end
    
    Email->>DB: Close Connection
```

---

## 📦 Installation

### Prerequisites

```bash
# Python 3.7+
python --version

# MySQL Server
mysql --version
```

### Install Dependencies

```bash
pip install requests beautifulsoup4 mysql-connector-python

# Analytics dependencies 🆕
pip install pandas matplotlib seaborn numpy

# Real-time dashboard dependencies 🆕
pip install dash plotly sqlalchemy
```

Or install all at once:
```bash
pip install -r requirements.txt
```

### Create `requirements.txt`:
```txt
requests>=2.28.0
beautifulsoup4>=4.11.0
mysql-connector-python>=8.0.0
python-dotenv>=1.0.0
pandas>=1.5.0
matplotlib>=3.6.0
seaborn>=0.12.0
numpy>=1.23.0
dash>=2.14.0
plotly>=5.18.0
sqlalchemy>=2.0.0
```

### Database Setup

```sql
CREATE DATABASE financial_news;

USE financial_news;

CREATE TABLE IPO_Scraped_Articles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Scraped_Date DATE NOT NULL,
    Website VARCHAR(100) NOT NULL,
    Keyword VARCHAR(50) NOT NULL,
    Title TEXT NOT NULL,
    Article_Link TEXT NOT NULL,
    sent_status BOOLEAN DEFAULT FALSE,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_sent_status (sent_status),
    INDEX idx_scraped_date (Scraped_Date),
    INDEX idx_keyword (Keyword)
);
```

---

## ⚙️ Configuration

### Database Configuration (`Ipo_tracker.py`)
Change the values in the .env file

```python
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('MYSQL_ROOT_PASSWORD'),  # or MYSQL_PASSWORD
    'database': os.getenv('DB_NAME'),
    'autocommit': False,
    'use_unicode': True,
    'charset': 'utf8mb4'
}
```

### Email Configuration (`mail_sending_agent.py`)
Change the values in .env file
```python
sender_email = os.getenv('SENDER_EMAIL')
recipient_emails = os.getenv('RECIPIENT_EMAILS') 
cc_emails = os.getenv('CC_EMAILS')

# SMTP Credentials
server.login(os.getenv('SENDER_EMAIL'),os.getenv('SENDER_PASSWORD'))
```

### Scraping Interval

Modify the wait time between scraping cycles:

```python
wait_minutes = os.getenv('SCRAPE_INTERVAL_MINUTES')  # Default: 90 minutes
```

---

## 🚀 Usage

### Running the Scraper

```bash
# Start continuous scraping
python Ipo_tracker.py

# The scraper will:
# 1. Connect to database
# 2. Load existing articles
# 3. Scrape all configured websites
# 4. Insert new articles
# 5. Wait 90 minutes
# 6. Repeat
```

### Running the Email Agent

```bash
# Send emails for unsent articles
python mail_sending_agent.py

# The agent will:
# 1. Connect to database
# 2. Fetch unsent articles
# 3. Format HTML email
# 4. Send via SMTP
# 5. Mark articles as sent
```

### Scheduling with Cron

```bash
# Edit crontab
crontab -e

# Run email agent every 2 hours
0 */2 * * * /usr/bin/python3 /path/to/mail_sending_agent.py

# Start scraper on system boot
@reboot /usr/bin/python3 /path/to/Ipo_tracker.py
```
### 3. Running Static Analytics Dashboard 🆕

```bash
python "News Scraper Analytics Dashboard.py"

# Output:
# 🎨 Generating all visualizations...
# ------------------------------------------------------------
# Database connection successful.
# Loaded 1247 articles from database.
# 
# ============================================================
# SUMMARY STATISTICS
# ============================================================
# ...
# 
# 📊 Creating charts...
# ✓ Source distribution chart saved
# ✓ Keyword distribution chart saved
# ✓ Daily trends chart saved
# ✓ Weekly trends chart saved
# ✓ Monthly trends chart saved
# ✓ Quarterly trends chart saved
# ✓ Source-Keyword heatmap saved
# ✓ Comparison dashboard saved
# 
# ✅ All visualizations generated successfully!
# 
# Do you want to save all the generated charts as images? (yes/no):
```

**Generated Charts:**
- `source_distribution.png`
- `keyword_distribution.png`
- `daily_trends.png`
- `weekly_trends.png`
- `monthly_trends.png`
- `quarterly_trends.png`
- `heatmap_source_keyword.png`
- `comparison_dashboard.png`

### 4. Running Real-time Dashboard 🆕

```bash
python Real_time_analytics_dashboard.py

# Output:
# 🚀 Starting Enhanced Real-time Dashboard...
# 📊 Dashboard will be available at: http://127.0.0.1:8050
# 🔗 Database: 127.0.0.1:3306/financial_news
# 🔄 Auto-refresh interval: 60 seconds
# ✨ All features from Analytics Dashboard included!
# Press Ctrl+C to stop
# 
# Dash is running on http://127.0.0.1:8050/
```

**Access in Browser:**
- Local: `http://127.0.0.1:8050`
- Network: `http://[your-ip]:8050`

**Features:**
- Auto-refreshes every 60 seconds
- Tabbed navigation
- Interactive charts
- Real-time metrics
- Responsive design

---

## 📊 Dashboard Comparison

| Feature | Static Dashboard | Real-time Dashboard |
|---------|-----------------|---------------------|
| **Technology** | matplotlib/seaborn | Dash/Plotly |
| **Update Method** | Manual run | Auto-refresh (60s) |
| **Interactivity** | Static images | Fully interactive |
| **Export** | PNG files | Screenshot only |
| **Performance** | One-time generation | Continuous updates |
| **Best For** | Reports, presentations | Monitoring, live analysis |
| **Resource Usage** | Low | Moderate |
| **Network Access** | Not required | Web browser required |
| **Customization** | Code changes | Tab selection |

---

---

## 🗄️ Database Schema

```mermaid
erDiagram
    IPO_Scraped_Articles {
        int id PK "Auto-increment primary key"
        date Scraped_Date "Date article was scraped"
        varchar Website "Source website name"
        varchar Keyword "Category: IPO/M&A/Demerger"
        text Title "Article headline"
        text Article_Link "Full URL to article"
        boolean sent_status "Email sent flag"
        timestamp inserted_at "Record creation time"
    }
```

### Key Fields Explained

| Field | Purpose | Example |
|-------|---------|---------|
| `id` | Unique identifier | 1, 2, 3... |
| `Scraped_Date` | When article was discovered | 2025-11-08 |
| `Website` | Source platform | MoneyControl, ZeeBiz |
| `Keyword` | Article category | IPO, M&A, Demerger |
| `Title` | Article headline | "Company XYZ files for IPO" |
| `Article_Link` | Direct URL | https://example.com/article |
| `sent_status` | Email notification status | 0 (pending), 1 (sent) |
| `inserted_at` | Database insertion timestamp | 2025-11-08 14:30:00 |

---

## 🔍 How It Works

### 1. Duplicate Prevention

```mermaid
graph LR
    A[New Article] --> B[Normalize Title]
    A --> C[Normalize URL]
    B --> D{Title Hash<br/>in Database?}
    C --> E{URL Hash<br/>in Database?}
    D -->|Yes| F[Skip - Duplicate]
    E -->|Yes| F
    D -->|No| G{Check URL}
    E -->|No| H[Accept Article]
    G --> E
    
    style F fill:#300404,stroke:#8A2E2E,stroke-width:2px
    style H fill:#043015,stroke:#2E8A4F,stroke-width:2px
```

**Normalization Process:**
- Convert to lowercase
- Remove extra whitespace
- Strip URL fragments (#anchors)
- Remove query parameters (optional)

### 2. Keyword Matching Engine

```mermaid
graph TD
    A[Article Title] --> B[Normalize Text<br/>lowercase, trim]
    B --> C{Check IPO<br/>Keywords}
    C -->|Match| D[Category: IPO]
    C -->|No Match| E{Check M&A<br/>Keywords}
    E -->|Match| F[Category: M&A]
    E -->|No Match| G{Check Demerger<br/>Keywords}
    G -->|Match| H[Category: Demerger]
    G -->|No Match| I[Category: Other]
    
    D --> J{Check Exclusion<br/>Keywords}
    F --> J
    H --> J
    
    J -->|Found| K[Mark as<br/>Relevant-but-Excluded]
    J -->|Not Found| L[Accept Article]
    I --> M[Reject Article]
    
    style D fill:#043015,stroke:#2E8A4F,stroke-width:2px
    style F fill:#043015,stroke:#2E8A4F,stroke-width:2px
    style H fill:#043015,stroke:#2E8A4F,stroke-width:2px
    style K fill:#696315,stroke:#C17D11,stroke-width:2px
    style M fill:#300404,stroke:#8A2E2E,stroke-width:2px
    style L fill:#4A90E2,stroke:#2E5C8A,stroke-width:3px,color:#fff
```

**Exact Word Matching:**
Uses regex word boundaries `\b` to ensure precision:
- ✅ "IPO filing" → Matches "IPO"
- ❌ "HIPOT test" → Does NOT match "IPO"
- ✅ "Company acquired stake" → Matches "Acquired"


### 3. Complete System Flow

```mermaid
graph TB
    A[News Scraper<br/>Every 90 min] --> B[(MySQL DB)]
    C[Email Agent<br/>Every 2 hours] --> B
    D[Static Dashboard<br/>On-demand] --> B
    E[Real-time Dashboard<br/>Continuous] --> B
    
    B --> F[New Articles]
    F --> G[Email Notifications]
    F --> H[Visual Analytics]
    
    H --> I[Historical Reports]
    H --> J[Live Monitoring]
    
    style A fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    style B fill:#043015,stroke:#2E8A4F,stroke-width:3px,color:#fff
    style D fill:#9B59B6,stroke:#6C3483,stroke-width:2px,color:#fff
    style E fill:#E67E22,stroke:#A04000,stroke-width:2px,color:#fff
```

---


## 🌐 Website-Specific Scraping Strategies

### Complexity Matrix

```mermaid
graph TD
    subgraph "Simple Structure"
        A[MNA Critique<br/>★☆☆☆☆]
        B[Entrackr<br/>★★☆☆☆]
    end
    
    subgraph "Moderate Complexity"
        C[Livemint<br/>★★★☆☆]
        D[MoneyControl<br/>★★★☆☆]
    end
    
    subgraph "High Complexity"
        E[ZeeBiz<br/>★★★★☆]
        F[Economic Times<br/>★★★★★]
    end
    
    style A fill:#043015,stroke:#2E8A4F
    style B fill:#043015,stroke:#2E8A4F
    style C fill:#F59527,stroke:#C17D11
    style D fill:#F59527,stroke:#C17D11
    style E fill:#FF6347,stroke:#8A2E2E
    style F fill:#DC143C,stroke:#8A2E2E,stroke-width:3px
```

### Per-Website Extraction Logic

#### 1. MoneyControl (Moderate)

```python
# Multiple selector strategy for robustness
selectors = ['div.item a', 'h2 a', 'h3 a', '.news-item a', '.story-card a']
```

**Challenges:**
- Dynamic content loading
- Multiple layout variations
- Nested article structures

**Solution:** Try multiple CSS selectors sequentially until articles are found.

---

#### 2. ZeeBiz (High Complexity)

```python
# Different selectors for Economy vs General sections
if is_economy:
    selectors = ['a.swdetl-mrgn0', '.story-title a', 'h2 a']
else:
    selectors = ['h3 a', 'h2 a', '.story-title a']
```

**Challenges:**
- Two separate sections (Economy & General)
- Inconsistent HTML structure
- Class name variations

**Solution:** Maintain separate selector sets for each section type.

---

#### 3. Economic Times (Highest Complexity)

```python
# Most diverse selector set
selectors = ['article a', '.story-card a', 'h2 a', 'h3 a', '.eachStory a']
# Filter out JavaScript links
if not href.startswith('javascript:'):
    # Process article
```

**Challenges:**
- JavaScript-heavy website
- AJAX content loading
- Invalid/broken links
- Complex nested structures

**Solution:** 
- Multiple fallback selectors
- JavaScript link filtering
- Robust URL validation

---

#### 4. Entrackr (Moderate)

```python
# Handle both direct links and parent-child relationships
selectors = ['h2 a', 'h3 a', 'a h2', 'a h3', '.post-title a']
```

**Challenges:**
- Headings sometimes inside links, sometimes wrapping links
- Inconsistent structure

**Solution:** Check both patterns (heading in link, link in heading).

---

#### 5. Livemint (Moderate)

```python
selectors = ['h2.imgStory a', 'h3 a', '.story-card a', '.headline a']
# Filter anchor-only links
if not href.startswith('#'):
    # Process article
```

**Challenges:**
- Internal navigation anchors
- Image-based story cards
- Multiple content types

**Solution:** Filter out hash-only links and use class-specific selectors.

---

#### 6. MNA Critique (Simple)

```python
elements = soup.select('h2.entry-title a, .entry-title a')
```

**Challenges:** Minimal - straightforward blog structure

**Solution:** Single selector targeting entry titles.

---

## 🎯 Keyword Matching Logic

### Category Definitions

```python
keyword_mapping = {
    "IPO": ["IPO", "Initial Public Offering"],
    
    "M&A": ["M&A", "Merger & Acquisition", "Merged", "Acquired", 
            "Merger", "Acquires", "Merge", "Acquisition", 
            "Merges", "Acquiring", "Merging"],
    
    "Demerger": ["Demerger", "Demerged", "Demerging", "Demerges", 
                 "Demerge", "Demergers", "Separate", "Separation", 
                 "Restructure", "Restructuring", "Restructures"]
}
```

### Exclusion Keywords

```python
exclusion_keywords = [
    # Marketing
    "advertisement", "ads", "sponsored", "promotion",
    
    # Entertainment
    "horoscope", "astrology", "cricket", "sports", 
    "bollywood", "entertainment", "celebrity", "movie",
    
    # Lifestyle
    "fashion", "lifestyle", "travel", "food", "recipe",
    "health tips", "fitness", "yoga",
    
    # Promotional
    "quiz", "contest", "giveaway", "discount", "offer",
    "sale", "shopping", "deals", "coupons",
    
    # Generic
    "Day", "Open"
]
```

### Matching Process

```mermaid
stateDiagram-v2
    [*] --> NormalizeTitle: Input Article Title
    NormalizeTitle --> CheckIPO: Convert to lowercase
    
    CheckIPO --> FoundIPO: Keywords matched with \b boundaries
    CheckIPO --> CheckMA: No match
    
    CheckMA --> FoundMA: Keywords matched
    CheckMA --> CheckDemerger: No match
    
    CheckDemerger --> FoundDemerger: Keywords matched
    CheckDemerger --> Irrelevant: No match
    
    FoundIPO --> CheckExclusion: Category = IPO
    FoundMA --> CheckExclusion: Category = M&A
    FoundDemerger --> CheckExclusion: Category = Demerger
    
    CheckExclusion --> Excluded: Exclusion keyword found
    CheckExclusion --> Accepted: Clean article
    
    Excluded --> [*]: Log & Skip
    Accepted --> [*]: Add to Database
    Irrelevant --> [*]: Skip silently
```

---

## 🛡️ Error Handling & Resilience

### Multi-Layer Error Protection

```mermaid
graph TB
    A[Scraper Start] --> B{Database<br/>Connected?}
    B -->|No| C[Retry Connection]
    C --> D{Success?}
    D -->|No| E[Exit with Error]
    D -->|Yes| F[Load Existing Articles]
    B -->|Yes| F
    
    F --> G{Website<br/>Accessible?}
    G -->|Timeout| H[Log & Skip Site]
    G -->|HTTP Error| H
    G -->|Success| I[Parse HTML]
    
    I --> J{Valid<br/>HTML?}
    J -->|No| H
    J -->|Yes| K[Extract Articles]
    
    K --> L{Database<br/>Still Connected?}
    L -->|No| M[Auto-Reconnect]
    M --> N{Success?}
    N -->|No| O[Buffer in Memory]
    N -->|Yes| P[Insert Batch]
    L -->|Yes| P
    
    P --> Q{Insertion<br/>Success?}
    Q -->|Error| R[Rollback & Log]
    Q -->|Success| S[Commit]
    
    H --> T[Continue Next Site]
    R --> T
    S --> T
    O --> T
    
    T --> U{More<br/>Sites?}
    U -->|Yes| G
    U -->|No| V[Wait 90 Minutes]
    V --> B
    
    style E fill:#300404,stroke:#8A2E2E,stroke-width:3px,color:#fff
    style S fill:#043015,stroke:#2E8A4F,stroke-width:2px
    style M fill:#C49F0E,stroke:#C17D11,stroke-width:2px
```

### Error Scenarios Handled

| Error Type | Detection | Recovery Strategy | Impact |
|------------|-----------|-------------------|---------|
| **Database Disconnect** | `db.is_connected()` | Auto-reconnect with retry | Minimal - Automatic recovery |
| **Website Timeout** | 15-second timeout | Skip site, continue scraping | Single site skipped |
| **HTTP Errors** | Status code check | Log & skip | Single site skipped |
| **Invalid HTML** | Content-type validation | Skip to next site | Single site skipped |
| **Duplicate Key** | Try-catch on INSERT | Rollback, continue | Article skipped |
| **SMTP Failure** | Exception handling | Log error, retry next cycle | Email delayed |
| **Memory Overflow** | Batch commits (10 articles) | Frequent commits | Reduced memory usage |

---

## 📊 Performance Metrics

### Scraping Performance

```mermaid
graph LR
    A[90 min cycle] --> B[7 websites]
    B --> C[~50 articles/site]
    C --> D[~350 total articles]
    D --> E[~10 relevant]
    E --> F[~2-5 inserted]
    
    style A fill:#4A90E2,stroke:#2E5C8A,stroke-width:2px,color:#fff
    style F fill:#043015,stroke:#2E8A4F,stroke-width:3px,color:#fff
```

**Typical Run Statistics:**
- Total articles processed: 300-400
- Relevant articles found: 8-15
- Duplicates skipped: 5-10
- New articles inserted: 2-8
- Execution time: 2-4 minutes

### Rate Limiting Strategy

```python
# Between article batches
if len(scraped_articles) % 10 == 0:
    time.sleep(30)  # 30 seconds

# Between websites
time.sleep(2)  # 2 seconds

# Between scraping cycles
time.sleep(90 * 60)  # 90 minutes
```

---

## 📧 Email Format Example

```html
<table border='1'>
    <tr>
        <th>ID</th>
        <th>Date</th>
        <th>Website</th>
        <th>Category</th>
        <th>Heading</th>
        <th>Link</th>
    </tr>
    <tr>
        <td>123</td>
        <td>2025-11-08</td>
        <td>MoneyControl</td>
        <td>IPO</td>
        <td>Tech Startup Files for IPO</td>
        <td><a href="...">View Article</a></td>
    </tr>
</table>
```

---

## 🔧 Troubleshooting

### Common Issues

**1. Database Connection Failed**
```bash
# Check MySQL service
sudo systemctl status mysql

# Test connection
mysql -u root -p -h localhost
```

**2. No Articles Found**
- Verify website URLs are accessible
- Check if HTML structure has changed
- Review CSS selectors in extraction functions

**3. Email Not Sending**
- Verify SMTP credentials
- Check firewall rules for port 587
- Ensure sender email has SMTP access enabled

**4. High CPU Usage**
- Increase sleep intervals
- Reduce number of websites
- Optimize database queries

### Dashboard-Specific Issues 🆕

**1. Real-time Dashboard Not Loading**
```bash
# Check if port 8050 is in use
netstat -ano | findstr :8050  # Windows
lsof -i :8050                  # Linux/Mac

# Change port if needed
app.run(debug=True, host='0.0.0.0', port=8051)
```

**2. Static Dashboard - No Charts Displayed**
```bash
# Check matplotlib backend
python -c "import matplotlib; print(matplotlib.get_backend())"

# If issues, try different backend
import matplotlib
matplotlib.use('TkAgg')  # or 'Qt5Agg'
```

**3. SQLAlchemy Connection Issues**
```bash
# Test connection
python -c "from sqlalchemy import create_engine; engine = create_engine('mysql+mysqlconnector://user:pass@host:port/db'); print(engine.connect())"
```

**4. Pandas Warning About mysql.connector**
- This is expected and can be ignored
- Or upgrade to SQLAlchemy (recommended)

**5. Dashboard Shows "No Data Available"**
- Verify database has records
- Check `.env` configuration
- Ensure scraper has run at least once


---

## 🚀 Future Enhancements

### Planned Features
- [ ] **Dashboard Improvements**
  - [ ] Add date range filters
  - [ ] Implement data export (CSV/Excel)
  - [ ] Add comparison mode (year-over-year)
  - [ ] Include sentiment analysis charts
  - [ ] Add drill-down capabilities
- [ ] **New Visualizations**
  - [ ] Geographic heatmaps
  - [ ] Network graphs (company relationships)
  - [ ] Trend prediction models
- [ ] **Integration Features**
  - [ ] REST API for external access
  - [ ] Webhook notifications
  - [ ] Slack/Teams integration
- [ ] **Advanced Analytics**
  - [ ] Machine learning categorization
  - [ ] Anomaly detection
  - [ ] Topic modeling
- [ ] **User Management**
  - [ ] Multi-user authentication
  - [ ] Personalized dashboards
  - [ ] Custom alert rules
---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [License](https://github.com/Acash-bits/Financial_News_Aggregator?tab=License-1-ov-file) file for details.

---

## 📞 Contact

For questions or support, contact:
- Email: akashwillstudy@gmail.com

---

## 🙏 Acknowledgments

- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP library
- **MySQL** - Database management
- **Python SMTP** - Email delivery

---

**Made with ❤️ for efficient financial news tracking**
