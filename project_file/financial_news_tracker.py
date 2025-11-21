import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urljoin, urlparse
import mysql.connector
import time
import traceback
import sys
import re
from typing import Set, List, Dict, Tuple, Optional
import hashlib
from dotenv import load_dotenv
import os


class NewsArticleScraper:
    def __init__(self, db_config: dict):
        """Initialize the scraper with database configuration."""
        self.db_config = db_config
        self.db = None
        self.connect_to_database()
        
        # Enhanced keyword mapping with exact word matching
        self.keyword_mapping = {
            "IPO": ["IPO", "Initial Public Offering"],
            "M&A": ["M&A", "Merger & Acquisition", "Merged", "Acquired", "Merger", 
                    "Acquires", "Merge", "Acquisition", "Merges", "Acquiring", "Merging"],
            "Demerger": ["Demerger", "Demerged", "Demerging", "Demerges", "Demerge", 
                        "Demergers", "Separate", "Separation", "Restructure", 
                        "Restructuring", "Restructures"]
        }
        
        # Exclusion keywords - articles with these keywords will be filtered out
        self.exclusion_keywords = [
            "advertisement", "ads", "sponsored", "promotion", "promo",
            "horoscope", "astrology", "cricket", "sports", "bollywood",
            "entertainment", "celebrity", "movie", "film", "weather",
            "obituary", "death", "died", "birthday", "anniversary",
            "fashion", "lifestyle", "travel", "food", "recipe",
            "health tips", "fitness", "yoga", "meditation", "games",
            "quiz", "contest", "giveaway", "discount", "offer",
            "sale", "shopping", "deals", "coupons","Day", "Open"
            
        ]
        
        # URLs configuration
        self.urls = {
            'MoneyControl': 'https://www.moneycontrol.com/news',
            'ZeeBiz Economy': "https://www.zeebiz.com/topics/economy",
            'ZeeBiz': "https://www.zeebiz.com/",
            'Economic Times': "https://economictimes.indiatimes.com/",
            'MNA Critique': "https://mnacritique.mergersindia.com/news-category/national-news/",
            'Entrackr': "https://entrackr.com/",
            'Livemint': "https://www.livemint.com/"
        }
        
        # Request headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }

    def connect_to_database(self) -> None:
        """Establish database connection with error handling."""
        try:
            self.db = mysql.connector.connect(**self.db_config)
            print("Database connection successful.")
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            print("Please check your database connection details and ensure the server is running.")
            sys.exit("Exiting due to database connection failure.")

    def ensure_db_connection(self) -> bool:
        """Ensure database connection is active, reconnect if needed."""
        try:
            if not self.db.is_connected():
                print("Database connection lost. Attempting to reconnect...")
                self.db.reconnect()
                print("Database reconnected.")
            return True
        except mysql.connector.Error as err:
            print(f"Failed to reconnect to database: {err}")
            return False

    def get_existing_articles(self) -> Tuple[Set[str], Set[str]]:
        """
        Fetch existing article titles and links from database to prevent duplicates.
        Returns tuple of (title_hashes, link_hashes) for efficient duplicate checking.
        """
        existing_titles = set()
        existing_links = set()
        
        if not self.ensure_db_connection():
            return set(), set()

        cursor = self.db.cursor()
        try:
            cursor.execute("SELECT Title, Article_Link FROM IPO_Scraped_Articles")
            for title, link in cursor.fetchall():
                # Use hash for efficient comparison and normalize case
                existing_titles.add(self.normalize_text(title))
                existing_links.add(self.normalize_url(link))
                
            print(f"Loaded {len(existing_titles)} existing articles from database.")
        except mysql.connector.Error as err:
            print(f"Error fetching existing articles from DB: {err}")
        finally:
            cursor.close()
            
        return existing_titles, existing_links

    def normalize_text(self, text: str) -> str:
        """Normalize text for comparison (lowercase, remove extra spaces)."""
        return re.sub(r'\s+', ' ', text.lower().strip())

    def normalize_url(self, url: str) -> str:
        """Normalize URL for comparison (remove fragments, normalize scheme)."""
        if not url:
            return ""
        return url.split('#')[0].lower().strip()

    def exact_keyword_match(self, text: str, keywords: List[str]) -> Tuple[bool, str]:
        """
        Check if any keyword appears as a complete word in the text.
        Returns (is_match, matched_keyword)
        """
        if not text:
            return False, ""
            
        # Normalize text for matching
        normalized_text = text.lower()
        
        for keyword in keywords:
            # Create word boundary pattern for exact matching
            pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
            if re.search(pattern, normalized_text):
                return True, keyword
                
        return False, ""

    def is_excluded_article(self, heading: str) -> Tuple[bool, str]:
        """
        Check if article should be excluded based on exclusion keywords.
        Returns (is_excluded, matched_exclusion_keyword)
        """
        if not heading:
            return False, ""
            
        # Check for exclusion keywords using exact word matching
        is_excluded, matched_keyword = self.exact_keyword_match(heading, self.exclusion_keywords)
        return is_excluded, matched_keyword

    def categorize_article(self, heading: str) -> Tuple[bool, str, bool]:
        """
        Categorize article based on exact keyword matching.
        Returns (is_relevant, category, has_relevant_but_excluded)
        """
        # First check for relevant keywords
        has_relevant_keyword = False
        relevant_category = "Other"
        
        for category, keywords in self.keyword_mapping.items():
            is_match, matched_keyword = self.exact_keyword_match(heading, keywords)
            if is_match:
                has_relevant_keyword = True
                relevant_category = category
                break
        
        # If has relevant keywords, check for exclusion keywords
        if has_relevant_keyword:
            is_excluded, _ = self.is_excluded_article(heading)
            if is_excluded:
                # This article has relevant keywords but is excluded
                return False, "Excluded", True
            else:
                # This article has relevant keywords and is not excluded
                return True, relevant_category, False
        
        # No relevant keywords found
        return False, "Other", False

    def fetch_and_parse(self, url: str, timeout: int = 15) -> Optional[BeautifulSoup]:
        """Fetch URL and return BeautifulSoup object with enhanced error handling."""
        try:
            session = requests.Session()
            session.headers.update(self.headers)
            
            response = session.get(url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            
            # Check if response is HTML
            content_type = response.headers.get('content-type', '').lower()
            if 'html' not in content_type:
                print(f"Non-HTML content received from {url}")
                return None
                
            return BeautifulSoup(response.content, 'html.parser')
            
        except requests.exceptions.Timeout:
            print(f"Request timed out for {url}")
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error for {url}: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Request error for {url}: {e}")
        except Exception as e:
            print(f"Unexpected error parsing {url}: {e}")
            
        return None

    def extract_articles_moneycontrol(self, soup: BeautifulSoup, base_url: str) -> List[Tuple[str, str]]:
        """Extract articles from MoneyControl with multiple selectors."""
        articles = []
        
        # Try multiple selectors for robustness
        selectors = [
            'div.item a',
            'h2 a',
            'h3 a',
            '.news-item a',
            '.story-card a'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                title = element.get('title') or element.get_text(strip=True)
                href = element.get('href')
                
                if title and href:
                    full_url = urljoin(base_url, href)
                    articles.append((full_url, title))
                    
        return articles

    def extract_articles_zeebiz(self, soup: BeautifulSoup, base_url: str, is_economy: bool = False) -> List[Tuple[str, str]]:
        """Extract articles from ZeeBiz with different selectors for economy vs general."""
        articles = []
        
        if is_economy:
            selectors = ['a.swdetl-mrgn0', '.story-title a', 'h2 a', 'h3 a']
        else:
            selectors = ['h3 a', 'h2 a', '.story-title a', '.news-title a']
            
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                title = element.get('title') or element.get_text(strip=True)
                href = element.get('href')
                
                if title and href:
                    full_url = urljoin(base_url, href)
                    articles.append((full_url, title))
                    
        return articles

    def extract_articles_economic_times(self, soup: BeautifulSoup, base_url: str) -> List[Tuple[str, str]]:
        """Extract articles from Economic Times."""
        articles = []
        
        selectors = [
            'article a',
            '.story-card a',
            'h2 a',
            'h3 a',
            '.eachStory a'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                title = element.get('title') or element.get_text(strip=True)
                href = element.get('href')
                
                if title and href and not href.startswith('javascript:'):
                    full_url = urljoin(base_url, href)
                    articles.append((full_url, title))
                    
        return articles

    def extract_articles_mna_critique(self, soup: BeautifulSoup, base_url: str) -> List[Tuple[str, str]]:
        """Extract articles from MNA Critique."""
        articles = []
        
        elements = soup.select('h2.entry-title a, .entry-title a')
        for element in elements:
            title = element.get_text(strip=True)
            href = element.get('href')
            
            if title and href:
                full_url = urljoin(base_url, href)
                articles.append((full_url, title))
                
        return articles

    def extract_articles_entrackr(self, soup: BeautifulSoup, base_url: str) -> List[Tuple[str, str]]:
        """Extract articles from Entrackr."""
        articles = []
        
        # Look for headings within links or parent links of headings
        selectors = ['h2 a', 'h3 a', 'a h2', 'a h3', '.post-title a']
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                if element.name == 'a':
                    title = element.get_text(strip=True)
                    href = element.get('href')
                else:
                    # If element is heading, find parent link
                    parent_link = element.find_parent('a')
                    if parent_link:
                        title = element.get_text(strip=True)
                        href = parent_link.get('href')
                    else:
                        continue
                
                if title and href:
                    full_url = urljoin(base_url, href)
                    articles.append((full_url, title))
                    
        return articles

    def extract_articles_livemint(self, soup: BeautifulSoup, base_url: str) -> List[Tuple[str, str]]:
        """Extract articles from Livemint."""
        articles = []
        
        selectors = [
            'h2.imgStory a',
            'h3 a',
            '.story-card a',
            '.headline a',
            'h2 a'
        ]
        
        for selector in selectors:
            elements = soup.select(selector)
            for element in elements:
                title = element.get_text(strip=True)
                href = element.get('href')
                
                if title and href and not href.startswith('#'):
                    full_url = urljoin(base_url, href)
                    articles.append((full_url, title))
                    
        return articles

    def scrape_articles(self, scraped_date: str, existing_titles: Set[str], existing_links: Set[str]) -> Tuple[List[Dict], List[Dict]]:
        """
        Scrape articles from all configured websites with enhanced duplicate detection.
        Returns tuple of (scraped_articles, relevant_but_excluded_articles)
        """
        scraped_articles = []
        relevant_but_excluded_articles = []  # Only articles with relevant keywords but excluded
        total_processed = 0
        total_relevant = 0
        total_duplicates = 0
        total_relevant_but_excluded = 0

        for site_name, url in self.urls.items():
            print(f"\n--- Scraping {site_name} ---")
            
            soup = self.fetch_and_parse(url)
            if not soup:
                print(f"Failed to fetch {site_name}")
                continue

            # Extract articles based on site
            raw_articles = []
            
            if site_name == 'MoneyControl':
                raw_articles = self.extract_articles_moneycontrol(soup, url)
            elif site_name == 'ZeeBiz Economy':
                raw_articles = self.extract_articles_zeebiz(soup, url, is_economy=True)
            elif site_name == 'ZeeBiz':
                raw_articles = self.extract_articles_zeebiz(soup, url, is_economy=False)
            elif site_name == 'Economic Times':
                raw_articles = self.extract_articles_economic_times(soup, url)
            elif site_name == 'MNA Critique':
                raw_articles = self.extract_articles_mna_critique(soup, url)
            elif site_name == 'Entrackr':
                raw_articles = self.extract_articles_entrackr(soup, url)
            elif site_name == 'Livemint':
                raw_articles = self.extract_articles_livemint(soup, url)

            print(f"Found {len(raw_articles)} raw articles from {site_name}")

            # Process articles for keywords and duplicates
            site_processed = 0
            site_relevant = 0
            site_duplicates = 0
            site_relevant_but_excluded = 0
            
            for article_url, heading in raw_articles:
                site_processed += 1
                
                # Skip invalid articles
                if not article_url or not heading or len(heading.strip()) < 10:
                    continue
                
                # Normalize for duplicate checking
                normalized_title = self.normalize_text(heading)
                normalized_url = self.normalize_url(article_url)
                
                # Check for duplicates
                if normalized_title in existing_titles or normalized_url in existing_links:
                    site_duplicates += 1
                    continue
                
                # Check keyword relevance and exclusion
                is_relevant, category, has_relevant_but_excluded = self.categorize_article(heading)
                
                if has_relevant_but_excluded:
                    # Article has relevant keywords but contains exclusion keywords
                    site_relevant_but_excluded += 1
                    is_excluded, matched_exclusion = self.is_excluded_article(heading)
                    relevant_but_excluded_articles.append({
                        'website': site_name,
                        'heading': heading.strip(),
                        'link': article_url,
                        'exclusion_reason': matched_exclusion,
                        'relevant_category': category
                    })
                    continue
                
                if is_relevant:
                    site_relevant += 1
                    
                    # Add to results
                    scraped_articles.append({
                        'scraped_date': scraped_date,
                        'website': site_name,
                        'keyword': category,
                        'heading': heading.strip(),
                        'link': article_url
                    })
                    
                    # Add to existing sets to prevent duplicates in current run
                    existing_titles.add(normalized_title)
                    existing_links.add(normalized_url)
                    
                    # Batch pause every 10 relevant articles
                    if len(scraped_articles) % 10 == 0:
                        print(f"Found {len(scraped_articles)} relevant articles, pausing 30 seconds...")
                        time.sleep(30)

            print(f"{site_name}: Processed={site_processed}, Relevant={site_relevant}, Duplicates={site_duplicates}, Relevant_but_Excluded={site_relevant_but_excluded}")
            
            total_processed += site_processed
            total_relevant += site_relevant
            total_duplicates += site_duplicates
            total_relevant_but_excluded += site_relevant_but_excluded
            
            # Small delay between sites
            time.sleep(2)

        print(f"\n--- Scraping Summary ---")
        print(f"Total processed: {total_processed}")
        print(f"Total relevant: {total_relevant}")
        print(f"Total duplicates skipped: {total_duplicates}")
        print(f"Total relevant but excluded: {total_relevant_but_excluded}")
        print(f"New articles to insert: {len(scraped_articles)}")

        return scraped_articles, relevant_but_excluded_articles

    def insert_into_db(self, scraped_articles: List[Dict]) -> None:
        """Insert scraped articles into database with enhanced error handling."""
        if not scraped_articles:
            print("No new articles to insert.")
            return

        if not self.ensure_db_connection():
            print("Database connection failed. Cannot insert articles.")
            return

        cursor = self.db.cursor()
        query = """
        INSERT INTO IPO_Scraped_Articles 
        (Scraped_Date, Website, Keyword, Title, Article_Link, sent_status, inserted_at)
        VALUES (%s, %s, %s, %s, %s, 0, NOW())
        """
        
        successful_inserts = 0
        failed_inserts = 0

        try:
            for i, article in enumerate(scraped_articles):
                try:
                    article_date = datetime.strptime(article['scraped_date'], '%d-%m-%y').date()
                    
                    cursor.execute(query, (
                        article_date,
                        article['website'],
                        article['keyword'],
                        article['heading'],
                        article['link']
                    ))
                    
                    successful_inserts += 1
                    
                    # Commit in batches
                    if successful_inserts % 10 == 0:
                        self.db.commit()
                        print(f"Inserted {successful_inserts}/{len(scraped_articles)} articles...")
                        
                except mysql.connector.Error as err:
                    print(f"Error inserting article: {err}")
                    failed_inserts += 1
                    self.db.rollback()

            # Final commit
            self.db.commit()
            
        except Exception as e:
            print(f"Unexpected error during insertion: {e}")
            self.db.rollback()
        finally:
            cursor.close()

        print(f"Insertion complete: {successful_inserts} successful, {failed_inserts} failed")

    def print_relevant_but_excluded_articles(self, relevant_but_excluded_articles: List[Dict]) -> None:
        """Print details of articles that had relevant keywords but were excluded."""
        if not relevant_but_excluded_articles:
            print("\nNo relevant articles were excluded due to exclusion keywords.")
            return

        print(f"\n{'='*80}")
        print(f"RELEVANT ARTICLES EXCLUDED DUE TO EXCLUSION KEYWORDS: {len(relevant_but_excluded_articles)}")
        print(f"{'='*80}")
        print("These articles contained relevant business keywords but also had exclusion keywords")

        # Group by exclusion reason for better readability
        exclusion_groups = {}
        for article in relevant_but_excluded_articles:
            reason = article['exclusion_reason']
            if reason not in exclusion_groups:
                exclusion_groups[reason] = []
            exclusion_groups[reason].append(article)

        for reason, articles in exclusion_groups.items():
            print(f"\n--- Excluded due to keyword: '{reason}' ({len(articles)} articles) ---")
            for i, article in enumerate(articles, 1):
                print(f"[{i}] {article['website']} | Would have been: {article.get('relevant_category', 'Unknown')}")
                print(f"    Title: {article['heading']}")
                print(f"    Link: {article['link']}")
                print("-" * 60)

    def print_articles(self, articles: List[Dict]) -> None:
        """Print article details in a formatted way."""
        if not articles:
            print("\nNo new articles found.")
            return

        print(f"\n{'='*80}")
        print(f"NEW ARTICLES FOUND: {len(articles)}")
        print(f"{'='*80}")

        for i, article in enumerate(articles, 1):
            print(f"\n[{i}] {article['keyword']} | {article['website']}")
            print(f"Title: {article['heading']}")
            print(f"Link: {article['link']}")
            print("-" * 80)

    def run_scraper(self) -> None:
        """Execute the complete scraping process."""
        print(f"\n{'='*80}")
        print(f"SCRAPER RUN STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")

        scraped_date = datetime.now().strftime('%d-%m-%y')

        # Get existing articles to prevent duplicates
        existing_titles, existing_links = self.get_existing_articles()

        # Scrape new articles and get relevant but excluded ones
        scraped_articles, relevant_but_excluded_articles = self.scrape_articles(scraped_date, existing_titles, existing_links)

        # Display results
        self.print_articles(scraped_articles)
        
        # Display relevant articles that were excluded due to exclusion keywords
        self.print_relevant_but_excluded_articles(relevant_but_excluded_articles)

        # Insert into database
        if scraped_articles:
            self.insert_into_db(scraped_articles)

        print(f"\n{'='*80}")
        print(f"SCRAPER RUN COMPLETED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*80}")

    def close_connection(self) -> None:
        """Close database connection."""
        if self.db and self.db.is_connected():
            self.db.close()
            print("Database connection closed.")

load_dotenv()

def main():
    """Main function to run the scraper continuously."""
    
    # Database configuration
    db_config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('MYSQL_ROOT_PASSWORD'),  # or MYSQL_PASSWORD
        'database': os.getenv('DB_NAME'),
        'autocommit': False,
        'use_unicode': True,
        'charset': 'utf8mb4'
    }
    scraper = NewsArticleScraper(db_config)

    print("Enhanced News Scraper initialized. Starting in 5 seconds...")
    time.sleep(5)

    try:
        while True:
            scraper.run_scraper()
            
            wait_minutes = os.getenv('SCRAPE_INTERVAL_MINUTES')
            print(f"\nWaiting {wait_minutes} minutes before next run...")
            time.sleep(wait_minutes * 60)
            
    except KeyboardInterrupt:
        print("\nScraper interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
    finally:
        scraper.close_connection()
        print("Scraper shutdown complete.")


if __name__ == "__main__":
    main()