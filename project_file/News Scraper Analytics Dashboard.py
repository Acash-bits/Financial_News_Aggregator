import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np
from matplotlib.dates import DateFormatter, MonthLocator, WeekdayLocator
import warnings
import os
from dotenv import load_dotenv
load_dotenv()
warnings.filterwarnings('ignore')

class NewsScraperAnalytics:
    def __init__(self, db_config: dict):
        """Initialize analytics with database configuration."""
        self.db_config = db_config
        self.db = None
        self.df = None
        self.connect_to_database()
        
    def connect_to_database(self):
        """Establish database connection."""
        try:
            self.db = mysql.connector.connect(**self.db_config)
            print("Database connection successful.")
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}")
            raise
    
    def load_data(self):
        """Load data from database into pandas DataFrame."""
        query = """
        SELECT 
            Scraped_Date,
            Website,
            Keyword,
            Title,
            Article_Link,
            inserted_at
        FROM IPO_Scraped_Articles
        ORDER BY Scraped_Date DESC
        """
        
        try:
            self.df = pd.read_sql(query, self.db)
            self.df['Scraped_Date'] = pd.to_datetime(self.df['Scraped_Date'])
            self.df['inserted_at'] = pd.to_datetime(self.df['inserted_at'])
            
            # Add time period columns
            self.df['Year'] = self.df['Scraped_Date'].dt.year
            self.df['Month'] = self.df['Scraped_Date'].dt.month
            self.df['Week'] = self.df['Scraped_Date'].dt.isocalendar().week
            self.df['Quarter'] = self.df['Scraped_Date'].dt.quarter
            self.df['YearMonth'] = self.df['Scraped_Date'].dt.to_period('M')
            self.df['YearWeek'] = self.df['Scraped_Date'].dt.to_period('W')
            self.df['YearQuarter'] = self.df['Scraped_Date'].dt.to_period('Q')
            
            print(f"Loaded {len(self.df)} articles from database.")
            return self.df
        except Exception as e:
            print(f"Error loading data: {e}")
            raise
    
    def plot_source_distribution(self):
        """Plot overall distribution of articles by source."""
        plt.figure(figsize=(14, 6))
        
        source_counts = self.df['Website'].value_counts()
        
        plt.subplot(1, 2, 1)
        source_counts.plot(kind='bar', color='steelblue')
        plt.title('Total Articles by Source', fontsize=14, fontweight='bold')
        plt.xlabel('Source', fontsize=11)
        plt.ylabel('Number of Articles', fontsize=11)
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.grid(axis='y', alpha=0.3)
        
        plt.subplot(1, 2, 2)
        wedges, texts, autotexts = plt.pie(source_counts, labels=source_counts.index, 
                                       autopct='%1.1f%%', startangle=90,
                                       pctdistance=0.85)
        # Adjust font sizes
        for text in texts:
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_fontsize(8)
            autotext.set_color('white')
            autotext.set_weight('bold')
        plt.title('Source Distribution (%)', fontsize=14, fontweight='bold')
                
        plt.tight_layout()
        plt.savefig('source_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Source distribution chart saved")
    
    def plot_keyword_distribution(self):
        """Plot overall distribution of articles by keyword."""
        plt.figure(figsize=(10, 6))
        
        keyword_counts = self.df['Keyword'].value_counts()
        
        plt.subplot(1, 2, 1)
        keyword_counts.plot(kind='bar', color='coral')
        plt.title('Total Articles by Keyword', fontsize=14, fontweight='bold')
        plt.xlabel('Keyword', fontsize=11)
        plt.ylabel('Number of Articles', fontsize=11)
        plt.xticks(rotation=45, ha='right')
        plt.grid(axis='y', alpha=0.3)
        
        plt.subplot(1, 2, 2)
        plt.pie(keyword_counts, labels=keyword_counts.index, autopct='%1.1f%%', startangle=90)
        plt.title('Keyword Distribution (%)', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('keyword_distribution.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Keyword distribution chart saved")
    
    def plot_daily_trends(self):
        """Plot daily article frequency."""
        plt.figure(figsize=(14, 6))
        
        daily_counts = self.df.groupby('Scraped_Date').size()
        
        plt.plot(daily_counts.index, daily_counts.values, marker='o', linewidth=2, markersize=4)
        plt.title('Daily Article Frequency', fontsize=14, fontweight='bold')
        plt.xlabel('Date', fontsize=11)
        plt.ylabel('Number of Articles', fontsize=11)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.savefig('daily_trends.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Daily trends chart saved")
    
    def plot_weekly_trends(self):
        """Plot weekly article frequency by source and keyword."""
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        # Weekly by source
        weekly_source = self.df.groupby(['YearWeek', 'Website']).size().unstack(fill_value=0)
        weekly_source.plot(kind='bar', stacked=False, ax=axes[0], width=0.8)
        axes[0].set_title('Weekly Articles by Source', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Week', fontsize=11)
        axes[0].set_ylabel('Number of Articles', fontsize=11)
        axes[0].legend(title='Source', bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[0].grid(axis='y', alpha=0.3)
        axes[0].tick_params(axis='x', rotation=45)
        
        # Weekly by keyword
        weekly_keyword = self.df.groupby(['YearWeek', 'Keyword']).size().unstack(fill_value=0)
        weekly_keyword.plot(kind='bar', stacked=False, ax=axes[1], width=0.8)
        axes[1].set_title('Weekly Articles by Keyword', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Week', fontsize=11)
        axes[1].set_ylabel('Number of Articles', fontsize=11)
        axes[1].legend(title='Keyword', bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[1].grid(axis='y', alpha=0.3)
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('weekly_trends.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Weekly trends chart saved")
    
    def plot_monthly_trends(self):
        """Plot monthly article frequency by source and keyword."""
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        # Monthly by source
        monthly_source = self.df.groupby(['YearMonth', 'Website']).size().unstack(fill_value=0)
        monthly_source.plot(kind='bar', stacked=False, ax=axes[0], width=0.8)
        axes[0].set_title('Monthly Articles by Source', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Month', fontsize=11)
        axes[0].set_ylabel('Number of Articles', fontsize=11)
        axes[0].legend(title='Source', bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[0].grid(axis='y', alpha=0.3)
        axes[0].tick_params(axis='x', rotation=45)
        
        # Monthly by keyword
        monthly_keyword = self.df.groupby(['YearMonth', 'Keyword']).size().unstack(fill_value=0)
        monthly_keyword.plot(kind='bar', stacked=False, ax=axes[1], width=0.8)
        axes[1].set_title('Monthly Articles by Keyword', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Month', fontsize=11)
        axes[1].set_ylabel('Number of Articles', fontsize=11)
        axes[1].legend(title='Keyword', bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[1].grid(axis='y', alpha=0.3)
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('monthly_trends.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Monthly trends chart saved")
    
    def plot_quarterly_trends(self):
        """Plot quarterly article frequency by source and keyword."""
        fig, axes = plt.subplots(2, 1, figsize=(14, 10))
        
        # Quarterly by source
        quarterly_source = self.df.groupby(['YearQuarter', 'Website']).size().unstack(fill_value=0)
        quarterly_source.plot(kind='bar', stacked=False, ax=axes[0], width=0.8)
        axes[0].set_title('Quarterly Articles by Source', fontsize=14, fontweight='bold')
        axes[0].set_xlabel('Quarter', fontsize=11)
        axes[0].set_ylabel('Number of Articles', fontsize=11)
        axes[0].legend(title='Source', bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[0].grid(axis='y', alpha=0.3)
        axes[0].tick_params(axis='x', rotation=45)
        
        # Quarterly by keyword
        quarterly_keyword = self.df.groupby(['YearQuarter', 'Keyword']).size().unstack(fill_value=0)
        quarterly_keyword.plot(kind='bar', stacked=False, ax=axes[1], width=0.8)
        axes[1].set_title('Quarterly Articles by Keyword', fontsize=14, fontweight='bold')
        axes[1].set_xlabel('Quarter', fontsize=11)
        axes[1].set_ylabel('Number of Articles', fontsize=11)
        axes[1].legend(title='Keyword', bbox_to_anchor=(1.05, 1), loc='upper left')
        axes[1].grid(axis='y', alpha=0.3)
        axes[1].tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('quarterly_trends.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Quarterly trends chart saved")
    
    def plot_comparison_dashboard(self):
        """Create comprehensive comparison dashboard."""
        fig = plt.figure(figsize=(20, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.35, wspace=0.35)
        
        # 1. Daily comparison
        ax1 = fig.add_subplot(gs[0, :2])
        daily_total = self.df.groupby('Scraped_Date').size()
        ax1.plot(daily_total.index, daily_total.values, marker='o', linewidth=2, markersize=3, label='Total')
        ax1.set_title('Daily Article Count', fontsize=12, fontweight='bold', pad= 10)
        ax1.set_xlabel('Date', fontsize=10)
        ax1.set_ylabel('Articles', fontsize=10)
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45, labelsize=8)
        ax1.legend()
        
        # 2. Source totals
        ax2 = fig.add_subplot(gs[0, 2])
        source_counts = self.df['Website'].value_counts()
        ax2.barh(range(len(source_counts)), source_counts.values, color='steelblue')
        ax2.set_yticks(range(len(source_counts)))
        ax2.set_yticklabels(source_counts.index, fontsize=9)
        ax2.set_title('Total by Source', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Articles')
        ax2.grid(axis='x', alpha=0.3)
        
        # 3. Weekly source comparison
        ax3 = fig.add_subplot(gs[1, :2])
        weekly_source = self.df.groupby(['YearWeek', 'Website']).size().unstack(fill_value=0)
        for col in weekly_source.columns:
            ax3.plot(range(len(weekly_source)), weekly_source[col].values, marker='o', label=col, linewidth=2, markersize=4)
        ax3.set_title('Weekly Articles by Source', fontsize=12, fontweight='bold')
        ax3.set_xlabel('Week')
        ax3.set_ylabel('Articles')
        ax3.legend(fontsize=7, loc='upper left', ncol=2)
        ax3.grid(True, alpha=0.3)
        
        # 4. Keyword totals
        ax4 = fig.add_subplot(gs[1, 2])
        keyword_counts = self.df['Keyword'].value_counts()
        ax4.barh(range(len(keyword_counts)), keyword_counts.values, color='coral')
        ax4.set_yticks(range(len(keyword_counts)))
        ax4.set_yticklabels(keyword_counts.index, fontsize=9)
        ax4.set_title('Total by Keyword', fontsize=12, fontweight='bold')
        ax4.set_xlabel('Articles')
        ax4.grid(axis='x', alpha=0.3)
        
        # 5. Monthly keyword comparison
        ax5 = fig.add_subplot(gs[2, :2])
        monthly_keyword = self.df.groupby(['YearMonth', 'Keyword']).size().unstack(fill_value=0)
        for col in monthly_keyword.columns:
            ax5.plot(range(len(monthly_keyword)), monthly_keyword[col].values, marker='s', label=col, linewidth=2, markersize=4)
        ax5.set_title('Monthly Articles by Keyword', fontsize=12, fontweight='bold')
        ax5.set_xlabel('Month')
        ax5.set_ylabel('Articles')
        ax5.legend(fontsize=8, loc='upper left')
        ax5.grid(True, alpha=0.3)
        
        # 6. Source vs Keyword heatmap
        ax6 = fig.add_subplot(gs[2, 2])
        heatmap_data = pd.crosstab(self.df['Keyword'], self.df['Website'])
        sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', ax=ax6, cbar_kws={'label': 'Count'}, annot_kws={'size': 8})
        ax6.set_title('Keyword vs Source', fontsize=12, fontweight='bold')
        ax6.set_xlabel('Source')
        ax6.set_ylabel('Keyword')
        ax6.tick_params(axis='x', rotation=45, labelsize=7)
        ax6.tick_params(axis='y', rotation=0, labelsize=8)
        
        plt.suptitle('News Scraper Analytics Dashboard', fontsize=16, fontweight='bold', y=0.995)
        plt.savefig('comparison_dashboard.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Comparison dashboard saved")
    
    def plot_heatmap_source_keyword(self):
        """Create detailed heatmap of source vs keyword."""
        plt.figure(figsize=(12, 6))
        
        heatmap_data = pd.crosstab(self.df['Website'], self.df['Keyword'])
        sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='Blues', linewidths=0.5, cbar_kws={'label': 'Article Count'})
        
        plt.title('Source vs Keyword Heatmap', fontsize=14, fontweight='bold')
        plt.xlabel('Keyword', fontsize=11)
        plt.ylabel('Source', fontsize=11)
        plt.tight_layout()
        
        plt.savefig('source_keyword_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("✓ Source-Keyword heatmap saved")
    
    def generate_summary_stats(self):
        """Print summary statistics."""
        print("\n" + "="*60)
        print("SUMMARY STATISTICS")
        print("="*60)
        
        print(f"\nTotal Articles: {len(self.df)}")
        print(f"Date Range: {self.df['Scraped_Date'].min().date()} to {self.df['Scraped_Date'].max().date()}")
        print(f"Total Days: {(self.df['Scraped_Date'].max() - self.df['Scraped_Date'].min()).days + 1}")
        
        print("\n--- Top Sources ---")
        print(self.df['Website'].value_counts().to_string())
        
        print("\n--- Keyword Distribution ---")
        print(self.df['Keyword'].value_counts().to_string())
        
        print("\n--- Average Articles per Day ---")
        daily_avg = self.df.groupby('Scraped_Date').size().mean()
        print(f"{daily_avg:.2f}")
        
        print("\n--- Most Active Week ---")
        weekly_counts = self.df.groupby('YearWeek').size()
        max_week = weekly_counts.idxmax()
        print(f"{max_week}: {weekly_counts.max()} articles")
        
        print("\n--- Most Active Month ---")
        monthly_counts = self.df.groupby('YearMonth').size()
        max_month = monthly_counts.idxmax()
        print(f"{max_month}: {monthly_counts.max()} articles")
        
        print("="*60 + "\n")
    
    def generate_all_visualizations(self):
        """Generate all visualizations at once."""
        print("\n🎨 Generating all visualizations...")
        print("-" * 60)
        
        self.load_data()
        self.generate_summary_stats()
        
        print("\n📊 Creating charts...")
        self.plot_source_distribution()
        self.plot_keyword_distribution()
        self.plot_daily_trends()
        self.plot_weekly_trends()
        self.plot_monthly_trends()
        self.plot_quarterly_trends()
        self.plot_heatmap_source_keyword()
        self.plot_comparison_dashboard()
        
        print("\n✅ All visualizations generated successfully!")
        print("📁 Check your working directory for PNG files")
    
    def close_connection(self):
        """Close database connection."""
        if self.db and self.db.is_connected():
            self.db.close()
            print("Database connection closed.")


def main():
    """Main function to run analytics."""
    
    # Database configuration (same as your scraper)
    db_config = {
        'host': os.getenv('DB_HOST'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('MYSQL_ROOT_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
    
    # Initialize analytics
    analytics = NewsScraperAnalytics(db_config)
    
    try:
        # Generate all visualizations
        analytics.generate_all_visualizations()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        analytics.close_connection()


if __name__ == "__main__":
    main()