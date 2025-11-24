import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "News Scraper Analytics - Real-time Enhanced"

# Database configuration
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD', '')
DB_NAME = os.getenv('DB_NAME', '')

# Create SQLAlchemy engine
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)

def fetch_data():
    """Fetch latest data from database using SQLAlchemy."""
    try:
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
        
        # Use SQLAlchemy engine with pandas
        df = pd.read_sql(query, engine)
        
        # Process data
        df['Scraped_Date'] = pd.to_datetime(df['Scraped_Date'])
        df['inserted_at'] = pd.to_datetime(df['inserted_at'])
        df['Year'] = df['Scraped_Date'].dt.year
        df['Month'] = df['Scraped_Date'].dt.month
        df['Week'] = df['Scraped_Date'].dt.isocalendar().week
        df['Quarter'] = df['Scraped_Date'].dt.quarter
        df['YearMonth'] = df['Scraped_Date'].dt.to_period('M').astype(str)
        df['YearWeek'] = df['Scraped_Date'].dt.to_period('W').astype(str)
        df['YearQuarter'] = df['Scraped_Date'].dt.to_period('Q').astype(str)
        
        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        import traceback
        traceback.print_exc()
        return pd.DataFrame()

# App layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("📊 News Scraper Analytics Dashboard - Enhanced", 
                style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 10}),
        html.P(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
               id='last-update',
               style={'textAlign': 'center', 'color': '#7f8c8d', 'fontSize': 14}),
    ], style={'backgroundColor': '#ecf0f1', 'padding': '20px', 'marginBottom': '20px'}),
    
    # Auto-refresh interval component
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Update every 60 seconds
        n_intervals=0
    ),
    
    # Summary Cards Row
    html.Div([
        html.Div([
            html.Div([
                html.H4("Total Articles", style={'color': '#34495e', 'marginBottom': 5}),
                html.H2(id='total-articles', style={'color': '#3498db', 'marginTop': 5, 'marginBottom': 5}),
                html.P(id='date-range', style={'fontSize': 12, 'color': '#7f8c8d', 'marginTop': 0})
            ], className='summary-card')
        ], style={'width': '18%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.Div([
                html.H4("Today's Articles", style={'color': '#34495e', 'marginBottom': 5}),
                html.H2(id='today-articles', style={'color': '#2ecc71', 'marginTop': 5})
            ], className='summary-card')
        ], style={'width': '18%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.Div([
                html.H4("This Week", style={'color': '#34495e', 'marginBottom': 5}),
                html.H2(id='week-articles', style={'color': '#e67e22', 'marginTop': 5})
            ], className='summary-card')
        ], style={'width': '18%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.Div([
                html.H4("This Month", style={'color': '#34495e', 'marginBottom': 5}),
                html.H2(id='month-articles', style={'color': '#e74c3c', 'marginTop': 5})
            ], className='summary-card')
        ], style={'width': '18%', 'display': 'inline-block', 'margin': '1%'}),
        
        html.Div([
            html.Div([
                html.H4("Top Source", style={'color': '#34495e', 'marginBottom': 5}),
                html.H2(id='top-source', style={'color': '#9b59b6', 'marginTop': 5, 'fontSize': 18})
            ], className='summary-card')
        ], style={'width': '18%', 'display': 'inline-block', 'margin': '1%'}),
    ], style={'marginBottom': 30}),
    
    # Tab Navigation
    dcc.Tabs(id='tabs', value='overview', children=[
        dcc.Tab(label='📈 Overview', value='overview', style={'fontWeight': 'bold'}),
        dcc.Tab(label='📅 Daily Analysis', value='daily', style={'fontWeight': 'bold'}),
        dcc.Tab(label='📊 Weekly Analysis', value='weekly', style={'fontWeight': 'bold'}),
        dcc.Tab(label='📆 Monthly Analysis', value='monthly', style={'fontWeight': 'bold'}),
        dcc.Tab(label='📋 Quarterly Analysis', value='quarterly', style={'fontWeight': 'bold'}),
        dcc.Tab(label='🔥 Heatmaps', value='heatmaps', style={'fontWeight': 'bold'}),
    ]),
    
    html.Div(id='tabs-content', style={'marginTop': 20})
    
], style={'fontFamily': 'Arial, sans-serif', 'padding': '20px', 'backgroundColor': '#f8f9fa'})

# Add CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            .summary-card {
                background-color: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Callback to update summary cards
@app.callback(
    [Output('last-update', 'children'),
     Output('total-articles', 'children'),
     Output('today-articles', 'children'),
     Output('week-articles', 'children'),
     Output('month-articles', 'children'),
     Output('top-source', 'children'),
     Output('date-range', 'children')],
    [Input('interval-component', 'n_intervals')]
)
def update_summary(n):
    """Update summary cards."""
    df = fetch_data()
    
    if df.empty:
        return ("No data available", "0", "0", "0", "0", "N/A", "")
    
    # Calculate metrics
    total_articles = len(df)
    today = datetime.now().date()
    today_articles = len(df[df['Scraped_Date'].dt.date == today])
    week_start = datetime.now() - timedelta(days=7)
    week_articles = len(df[df['Scraped_Date'] >= week_start])
    month_start = datetime.now() - timedelta(days=30)
    month_articles = len(df[df['Scraped_Date'] >= month_start])
    top_source = df['Website'].value_counts().index[0] if len(df) > 0 else "N/A"
    
    date_range = f"{df['Scraped_Date'].min().strftime('%Y-%m-%d')} to {df['Scraped_Date'].max().strftime('%Y-%m-%d')}"
    
    last_update = f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    return (
        last_update,
        f"{total_articles:,}",
        f"{today_articles:,}",
        f"{week_articles:,}",
        f"{month_articles:,}",
        top_source,
        date_range
    )

# Callback to render tab content
@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value'),
     Input('interval-component', 'n_intervals')]
)
def render_content(tab, n):
    """Render content based on selected tab."""
    df = fetch_data()
    
    if df.empty:
        return html.Div("No data available", style={'textAlign': 'center', 'padding': '50px'})
    
    if tab == 'overview':
        return create_overview_tab(df)
    elif tab == 'daily':
        return create_daily_tab(df)
    elif tab == 'weekly':
        return create_weekly_tab(df)
    elif tab == 'monthly':
        return create_monthly_tab(df)
    elif tab == 'quarterly':
        return create_quarterly_tab(df)
    elif tab == 'heatmaps':
        return create_heatmaps_tab(df)

def create_overview_tab(df):
    """Create overview tab with source and keyword distributions."""
    # Source Distribution Bar Chart
    source_counts = df['Website'].value_counts()
    fig_source_bar = px.bar(
        x=source_counts.index, 
        y=source_counts.values,
        title="Total Articles by Source",
        labels={'x': 'Source', 'y': 'Count'},
        color=source_counts.values,
        color_continuous_scale='Blues'
    )
    fig_source_bar.update_layout(showlegend=False, height=400)
    
    # Source Distribution Pie Chart
    fig_source_pie = px.pie(
        values=source_counts.values,
        names=source_counts.index,
        title="Source Distribution (%)",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_source_pie.update_layout(height=400)
    
    # Keyword Distribution Bar Chart
    keyword_counts = df['Keyword'].value_counts()
    fig_keyword_bar = px.bar(
        x=keyword_counts.index,
        y=keyword_counts.values,
        title="Total Articles by Keyword",
        labels={'x': 'Keyword', 'y': 'Count'},
        color=keyword_counts.values,
        color_continuous_scale='Reds'
    )
    fig_keyword_bar.update_layout(showlegend=False, height=400)
    
    # Keyword Distribution Pie Chart
    fig_keyword_pie = px.pie(
        values=keyword_counts.values,
        names=keyword_counts.index,
        title="Keyword Distribution (%)",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_keyword_pie.update_layout(height=400)
    
    return html.Div([
        html.H3("📊 Overview - Source & Keyword Analysis", style={'color': '#2c3e50', 'marginBottom': 20}),
        
        # Source Charts
        html.Div([
            html.Div([dcc.Graph(figure=fig_source_bar)], 
                    style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
            html.Div([dcc.Graph(figure=fig_source_pie)], 
                    style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        ]),
        
        # Keyword Charts
        html.Div([
            html.Div([dcc.Graph(figure=fig_keyword_bar)], 
                    style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
            html.Div([dcc.Graph(figure=fig_keyword_pie)], 
                    style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),
        ]),
    ])

def create_daily_tab(df):
    """Create daily analysis tab."""
    # Daily Trends
    daily_counts = df.groupby(df['Scraped_Date'].dt.date).size().reset_index()
    daily_counts.columns = ['Date', 'Count']
    fig_daily = px.line(
        daily_counts,
        x='Date',
        y='Count',
        title="Daily Article Frequency",
        markers=True
    )
    fig_daily.update_layout(height=450)
    fig_daily.update_traces(line_color='#3498db', marker=dict(size=8))
    
    # Daily Average
    daily_avg = df.groupby(df['Scraped_Date'].dt.date).size().mean()
    
    return html.Div([
        html.H3("📅 Daily Analysis", style={'color': '#2c3e50', 'marginBottom': 20}),
        
        html.Div([
            html.Div([
                html.H4("Average Articles/Day", style={'color': '#34495e'}),
                html.H2(f"{daily_avg:.2f}", style={'color': '#3498db'})
            ], className='summary-card', style={'width': '30%', 'display': 'inline-block', 'margin': '10px'})
        ], style={'textAlign': 'center', 'marginBottom': 20}),
        
        dcc.Graph(figure=fig_daily, style={'padding': '10px'}),
    ])

def create_weekly_tab(df):
    """Create weekly analysis tab."""
    # Weekly by Source
    weekly_source = df.groupby(['YearWeek', 'Website']).size().reset_index()
    weekly_source.columns = ['Week', 'Source', 'Count']
    fig_weekly_source = px.line(
        weekly_source,
        x='Week',
        y='Count',
        color='Source',
        title="Weekly Articles by Source",
        markers=True
    )
    fig_weekly_source.update_layout(height=450)
    
    # Weekly by Keyword
    weekly_keyword = df.groupby(['YearWeek', 'Keyword']).size().reset_index()
    weekly_keyword.columns = ['Week', 'Keyword', 'Count']
    fig_weekly_keyword = px.line(
        weekly_keyword,
        x='Week',
        y='Count',
        color='Keyword',
        title="Weekly Articles by Keyword",
        markers=True
    )
    fig_weekly_keyword.update_layout(height=450)
    
    # Most Active Week
    weekly_counts = df.groupby('YearWeek').size()
    max_week = weekly_counts.idxmax()
    max_week_count = weekly_counts.max()
    
    return html.Div([
        html.H3("📊 Weekly Analysis", style={'color': '#2c3e50', 'marginBottom': 20}),
        
        html.Div([
            html.Div([
                html.H4("Most Active Week", style={'color': '#34495e'}),
                html.H3(f"{max_week}", style={'color': '#e67e22', 'fontSize': 16}),
                html.P(f"{max_week_count} articles", style={'color': '#7f8c8d'})
            ], className='summary-card', style={'width': '30%', 'display': 'inline-block', 'margin': '10px'})
        ], style={'textAlign': 'center', 'marginBottom': 20}),
        
        dcc.Graph(figure=fig_weekly_source, style={'padding': '10px'}),
        dcc.Graph(figure=fig_weekly_keyword, style={'padding': '10px'}),
    ])

def create_monthly_tab(df):
    """Create monthly analysis tab."""
    # Monthly by Source
    monthly_source = df.groupby(['YearMonth', 'Website']).size().reset_index()
    monthly_source.columns = ['Month', 'Source', 'Count']
    fig_monthly_source = px.bar(
        monthly_source,
        x='Month',
        y='Count',
        color='Source',
        title="Monthly Articles by Source",
        barmode='group'
    )
    fig_monthly_source.update_layout(height=450)
    
    # Monthly by Keyword
    monthly_keyword = df.groupby(['YearMonth', 'Keyword']).size().reset_index()
    monthly_keyword.columns = ['Month', 'Keyword', 'Count']
    fig_monthly_keyword = px.bar(
        monthly_keyword,
        x='Month',
        y='Count',
        color='Keyword',
        title="Monthly Articles by Keyword",
        barmode='group'
    )
    fig_monthly_keyword.update_layout(height=450)
    
    # Most Active Month
    monthly_counts = df.groupby('YearMonth').size()
    max_month = monthly_counts.idxmax()
    max_month_count = monthly_counts.max()
    
    return html.Div([
        html.H3("📆 Monthly Analysis", style={'color': '#2c3e50', 'marginBottom': 20}),
        
        html.Div([
            html.Div([
                html.H4("Most Active Month", style={'color': '#34495e'}),
                html.H3(f"{max_month}", style={'color': '#e74c3c', 'fontSize': 16}),
                html.P(f"{max_month_count} articles", style={'color': '#7f8c8d'})
            ], className='summary-card', style={'width': '30%', 'display': 'inline-block', 'margin': '10px'})
        ], style={'textAlign': 'center', 'marginBottom': 20}),
        
        dcc.Graph(figure=fig_monthly_source, style={'padding': '10px'}),
        dcc.Graph(figure=fig_monthly_keyword, style={'padding': '10px'}),
    ])

def create_quarterly_tab(df):
    """Create quarterly analysis tab."""
    # Quarterly by Source
    quarterly_source = df.groupby(['YearQuarter', 'Website']).size().reset_index()
    quarterly_source.columns = ['Quarter', 'Source', 'Count']
    fig_quarterly_source = px.bar(
        quarterly_source,
        x='Quarter',
        y='Count',
        color='Source',
        title="Quarterly Articles by Source",
        barmode='group'
    )
    fig_quarterly_source.update_layout(height=450)
    
    # Quarterly by Keyword
    quarterly_keyword = df.groupby(['YearQuarter', 'Keyword']).size().reset_index()
    quarterly_keyword.columns = ['Quarter', 'Keyword', 'Count']
    fig_quarterly_keyword = px.bar(
        quarterly_keyword,
        x='Quarter',
        y='Count',
        color='Keyword',
        title="Quarterly Articles by Keyword",
        barmode='group'
    )
    fig_quarterly_keyword.update_layout(height=450)
    
    return html.Div([
        html.H3("📋 Quarterly Analysis", style={'color': '#2c3e50', 'marginBottom': 20}),
        
        dcc.Graph(figure=fig_quarterly_source, style={'padding': '10px'}),
        dcc.Graph(figure=fig_quarterly_keyword, style={'padding': '10px'}),
    ])

def create_heatmaps_tab(df):
    """Create heatmaps tab."""
    # Source vs Keyword Heatmap
    heatmap_data_1 = pd.crosstab(df['Keyword'], df['Website'])
    fig_heatmap_1 = px.imshow(
        heatmap_data_1,
        title="Keyword vs Source Heatmap",
        labels=dict(x="Source", y="Keyword", color="Count"),
        color_continuous_scale='YlOrRd',
        text_auto=True
    )
    fig_heatmap_1.update_layout(height=450)
    
    # Website vs Keyword Heatmap (reversed)
    heatmap_data_2 = pd.crosstab(df['Website'], df['Keyword'])
    fig_heatmap_2 = px.imshow(
        heatmap_data_2,
        title="Source vs Keyword Heatmap",
        labels=dict(x="Keyword", y="Source", color="Count"),
        color_continuous_scale='Blues',
        text_auto=True
    )
    fig_heatmap_2.update_layout(height=450)
    
    return html.Div([
        html.H3("🔥 Heatmap Analysis", style={'color': '#2c3e50', 'marginBottom': 20}),
        
        dcc.Graph(figure=fig_heatmap_1, style={'padding': '10px'}),
        dcc.Graph(figure=fig_heatmap_2, style={'padding': '10px'}),
    ])

if __name__ == '__main__':
    print("🚀 Starting Enhanced Real-time Dashboard...")
    print(f"📊 Dashboard will be available at: http://127.0.0.1:8050")
    print(f"🔗 Database: {DB_HOST}:{DB_PORT}/{DB_NAME}")
    print("🔄 Auto-refresh interval: 60 seconds")
    print("✨ All features from Analytics Dashboard included!")
    print("Press Ctrl+C to stop")
    app.run(debug=True, host='0.0.0.0', port=8050)