# Contributing to Financial News Aggregator

First off, thank you for considering contributing to this project! 🎉

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Adding New News Sources](#adding-new-news-sources)

---

## Code of Conduct

This project adheres to a code of conduct that all contributors are expected to follow. Please be respectful and constructive in all interactions.

---

## How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected vs actual behavior**
- **System information** (OS, Python version, MySQL version)
- **Error messages or logs**

**Example:**
```
Title: MoneyControl scraper fails with timeout error

Description:
The scraper consistently fails when accessing MoneyControl website
after running for 2 hours.

Steps to reproduce:
1. Start scraper with `python Ipo_tracker.py`
2. Wait for 2 hours
3. Observe timeout errors in logs

Expected: Successful scraping
Actual: Timeout after 15 seconds

Error: requests.exceptions.Timeout: HTTPSConnectionPool...
```

### 💡 Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- **Use a clear, descriptive title**
- **Provide detailed description** of the proposed feature
- **Explain why this enhancement would be useful**
- **Include examples** if applicable

### 🔧 Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly
5. Commit with clear messages
6. Push to your fork
7. Open a Pull Request

---

## Development Setup

### Prerequisites

```bash
# Python 3.7 or higher
python --version

# MySQL 5.7 or higher
mysql --version
```

### Installation

1. **Clone your fork:**
```bash
git clone https://github.com/Acash-bits/financial-news-aggregator.git
cd financial-news-aggregator
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up configuration:**
```bash
cp config.example.py config.py
# Edit config.py with your credentials
```

5. **Set up database:**
```bash
mysql -u root -p < database/setup.sql
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_scraper.py
```

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line length**: 100 characters (not 79)
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Single quotes for strings, double for docstrings
- **Imports**: Grouped and sorted (standard lib, third-party, local)

### Code Formatting

Use `black` for automatic formatting:

```bash
black Ipo_tracker.py mail_sending_agent.py
```

### Linting

Use `flake8` to check code quality:

```bash
flake8 --max-line-length=100 *.py
```

### Documentation

- **All functions must have docstrings** explaining purpose, parameters, and return values
- **Use type hints** where appropriate
- **Comment complex logic** but avoid obvious comments

**Example:**

```python
def extract_articles_moneycontrol(self, soup: BeautifulSoup, base_url: str) -> List[Tuple[str, str]]:
    """
    Extract articles from MoneyControl with multiple selectors.
    
    Args:
        soup (BeautifulSoup): Parsed HTML content
        base_url (str): Base URL for resolving relative links
    
    Returns:
        List[Tuple[str, str]]: List of (article_url, title) tuples
    
    Raises:
        None - Errors are logged but not raised
    """
    # Implementation
```

---

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding tests
- **chore**: Maintenance tasks

### Examples

**Good:**
```
feat(scraper): add support for Business Standard website

- Implemented extraction logic for BS article structure
- Added specific CSS selectors for headlines
- Tested with 100+ sample articles

Closes #42
```

**Bad:**
```
fixed stuff
```

---

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Comments added to complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] Added tests
- [ ] Tests pass
```

### Review Process

1. Maintainer reviews code
2. Feedback provided if changes needed
3. Once approved, PR is merged
4. Branch is deleted

---

## Adding New News Sources

To add a new website to scrape:

### 1. Add URL to Configuration

```python
# In Ipo_tracker.py, add to self.urls dictionary
self.urls = {
    'MoneyControl': 'https://www.moneycontrol.com/news',
    # ... existing sites ...
    'YourNewSite': 'https://example.com/business'  # Add here
}
```

### 2. Create Extraction Function

```python
def extract_articles_yournewsite(self, soup: BeautifulSoup, base_url: str) -> List[Tuple[str, str]]:
    """
    Extract articles from YourNewSite.
    
    Args:
        soup: Parsed HTML content
        base_url: Base URL for resolving links
    
    Returns:
        List of (article_url, title) tuples
    """
    articles = []
    
    # Your extraction logic here
    selectors = ['h2.article-title a', '.news-item a']
    
    for selector in selectors:
        elements = soup.select(selector)
        for element in elements:
            title = element.get_text(strip=True)
            href = element.get('href')
            
            if title and href:
                full_url = urljoin(base_url, href)
                articles.append((full_url, title))
    
    return articles
```

### 3. Add to Scraping Logic

```python
# In scrape_articles() method
elif site_name == 'YourNewSite':
    raw_articles = self.extract_articles_yournewsite(soup, url)
```

### 4. Test Thoroughly

```python
# Create test cases
def test_yournewsite_extraction():
    scraper = NewsArticleScraper(db_config)
    soup = scraper.fetch_and_parse('https://example.com/business')
    articles = scraper.extract_articles_yournewsite(soup, 'https://example.com')
    
    assert len(articles) > 0
    assert all(isinstance(a, tuple) and len(a) == 2 for a in articles)
```

### 5. Document the Addition

Update README.md:
- Add to supported websites list
- Document any special handling
- Add complexity rating

---

## Questions?

Feel free to open an issue with the `question` label or reach out to the maintainers.

---

Thank you for contributing! 🙌