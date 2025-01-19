import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def prepare_date_features(df):
    """
    Add date-based features to the dataset
    """
    # Convert processing_date to datetime if it isn't already
    df['date'] = pd.to_datetime(df['processing_date'], format='%Y%m%d')
    
    # Extract date features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%B')
    df['week'] = df['date'].dt.isocalendar().week
    df['day_of_week'] = df['date'].dt.dayofweek
    df['day_name'] = df['date'].dt.strftime('%A')
    df['quarter'] = df['date'].dt.quarter
    
    return df

def prepare_daily_metrics(df):
    """
    Calculate daily performance metrics
    """
    daily_stats = df.groupby('processing_date').agg({
        'isbn13': 'count',  # Total books
        'price': ['mean', 'median', 'std'],
        'rating': ['mean', 'median'],
        'review_count': 'sum',
        'main_category': 'nunique',  # Number of unique categories
        'standardized_format': 'nunique'  # Number of unique formats
    }).round(2)
    
    # Flatten column names
    daily_stats.columns = [
        f'{x[0]}_{x[1]}' if x[1] != '' else x[0]
        for x in daily_stats.columns
    ]
    
    return daily_stats.reset_index()

def prepare_weekly_trends(df):
    """
    Analyze trends by day of week
    """
    weekly_stats = df.groupby(['year', 'week', 'day_of_week', 'day_name']).agg({
        'isbn13': 'count',
        'price': ['mean', 'median'],
        'rating': 'mean',
        'review_count': 'sum',
        'main_category': 'nunique',
        'standardized_format': 'nunique'
    }).round(2)
    
    # Flatten column names
    weekly_stats.columns = [
        f'{x[0]}_{x[1]}' if x[1] != '' else x[0]
        for x in weekly_stats.columns
    ]
    
    return weekly_stats.reset_index()

def prepare_monthly_trends(df):
    """
    Analyze trends by month
    """
    monthly_stats = df.groupby(['year', 'month', 'month_name']).agg({
        'isbn13': 'count',
        'price': ['mean', 'median'],
        'rating': 'mean',
        'review_count': 'sum',
        'main_category': 'nunique',
        'standardized_format': 'nunique'
    }).round(2)
    
    # Flatten column names
    monthly_stats.columns = [
        f'{x[0]}_{x[1]}' if x[1] != '' else x[0]
        for x in monthly_stats.columns
    ]
    
    return monthly_stats.reset_index()

def prepare_category_seasonality(df):
    """
    Analyze seasonal patterns by category
    """
    category_seasonal = df.groupby(
        ['year', 'month', 'month_name', 'main_category']
    ).agg({
        'isbn13': 'count',
        'price': ['mean', 'median'],
        'main_category_rank': ['min', 'max', 'mean'],
        'rating': 'mean',
        'review_count': 'sum'
    }).round(2)
    
    # Flatten column names
    category_seasonal.columns = [
        f'{x[0]}_{x[1]}' if x[1] != '' else x[0]
        for x in category_seasonal.columns
    ]
    
    return category_seasonal.reset_index()

def prepare_format_seasonality(df):
    """
    Analyze seasonal patterns by format
    Uses standardized format groupings
    """
    # Define standard format categories (same as other notebooks)
    STANDARD_FORMATS = {
        'Hardcover': 'Hardback',
        'Hardback': 'Hardback',
        'Paperback': 'Paperback',
        'Kindle Edition': 'Digital',
        'Kindle': 'Digital',
        'eBook': 'Digital',
        'Audio CD': 'Audio',
        'Audiobook': 'Audio',
        'Board Book': 'Board books',
        'Pop-up Book': 'Novelty',
        'Sound Book': 'Novelty',
        'Touch and Feel': 'Novelty',
        'Novelty Book': 'Novelty',
        'Activity Book': 'Novelty',
        'Spiral-bound': 'Other',
        'Calendar': 'Other',
        'Cards': 'Other',
        'Map': 'Other',
        'Library Binding': 'Hardback',
        'Mass Market Paperback': 'Paperback'
    }
    
    # Apply format grouping
    df['format_grouped'] = df['standardized_format'].map(
        lambda x: STANDARD_FORMATS.get(x, 'Other')
    )
    
    format_seasonal = df.groupby(
        ['year', 'month', 'month_name', 'format_grouped']
    ).agg({
        'isbn13': 'count',
        'price': ['mean', 'median'],
        'rating': 'mean',
        'review_count': 'sum'
    }).round(2)
    
    # Flatten column names
    format_seasonal.columns = [
        f'{x[0]}_{x[1]}' if x[1] != '' else x[0]
        for x in format_seasonal.columns
    ]
    
    return format_seasonal.reset_index()

def prepare_bestseller_persistence(df):
    """
    Analyze how long books stay in bestseller lists
    Tracks presence across different dates
    """
    if df['processing_date'].nunique() <= 1:
        # Return empty DataFrame for single-day data
        return pd.DataFrame(columns=[
            'isbn13', 'title', 'author', 'main_category', 
            'first_seen', 'last_seen', 'days_present',
            'rank_changes', 'avg_rank'
        ])
    
    persistence = df.groupby('isbn13').agg({
        'processing_date': ['min', 'max', 'count'],
        'title': 'first',
        'author': 'first',
        'main_category': 'first',
        'main_category_rank': ['mean', 'std']
    }).round(2)
    
    # Flatten column names
    persistence.columns = [
        f'{x[0]}_{x[1]}' if x[1] != '' else x[0]
        for x in persistence.columns
    ]
    
    # Rename columns for clarity
    persistence = persistence.rename(columns={
        'processing_date_min': 'first_seen',
        'processing_date_max': 'last_seen',
        'processing_date_count': 'days_present',
        'main_category_rank_mean': 'avg_rank',
        'main_category_rank_std': 'rank_volatility'
    })
    
    return persistence.reset_index()

def export_seasonal_analysis(df):
    """
    Main function to prepare and export all seasonal analysis for PowerBI
    """
    # Create output directory
    output_dir = Path('../data/powerbi')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Add date features
    df = prepare_date_features(df)
    
    # Prepare all datasets
    daily_metrics = prepare_daily_metrics(df)
    weekly_trends = prepare_weekly_trends(df)
    monthly_trends = prepare_monthly_trends(df)
    category_seasonal = prepare_category_seasonality(df)
    format_seasonal = prepare_format_seasonality(df)
    bestseller_persistence = prepare_bestseller_persistence(df)
    
    # Export to CSV with timestamp
    timestamp = datetime.now().strftime('%Y%m%d')
    
    # Export main datasets
    daily_metrics.to_csv(
        output_dir / f'daily_metrics_{timestamp}.csv',
        index=False
    )
    weekly_trends.to_csv(
        output_dir / f'weekly_trends_{timestamp}.csv',
        index=False
    )
    monthly_trends.to_csv(
        output_dir / f'monthly_trends_{timestamp}.csv',
        index=False
    )
    category_seasonal.to_csv(
        output_dir / f'category_seasonal_{timestamp}.csv',
        index=False
    )
    format_seasonal.to_csv(
        output_dir / f'format_seasonal_{timestamp}.csv',
        index=False
    )
    bestseller_persistence.to_csv(
        output_dir / f'bestseller_persistence_{timestamp}.csv',
        index=False
    )
    
    # Export a summary of what was processed
    summary = pd.DataFrame({
        'dataset': [
            'daily_metrics',
            'weekly_trends',
            'monthly_trends',
            'category_seasonal',
            'format_seasonal',
            'bestseller_persistence'
        ],
        'record_count': [
            len(daily_metrics),
            len(weekly_trends),
            len(monthly_trends),
            len(category_seasonal),
            len(format_seasonal),
            len(bestseller_persistence)
        ],
        'export_date': timestamp
    })
    
    summary.to_csv(output_dir / f'seasonal_export_summary_{timestamp}.csv', index=False)
    
    return {
        'daily_metrics': daily_metrics,
        'weekly_trends': weekly_trends,
        'monthly_trends': monthly_trends,
        'category_seasonal': category_seasonal,
        'format_seasonal': format_seasonal,
        'bestseller_persistence': bestseller_persistence,
        'summary': summary
    }

if __name__ == "__main__":
    # Load the master dataset
    df = pd.read_csv('../data/processed/master_bestsellers.csv')
    
    # Run the export
    results = export_seasonal_analysis(df)
    
    # Print summary of export
    print("\n=== Export Summary ===")
    print(results['summary'].to_string(index=False))