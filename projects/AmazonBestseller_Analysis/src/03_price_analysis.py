import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def prepare_format_price_data(df):
    """
    Prepare format-based price analysis data for PowerBI
    - Uses predefined format categories
    - Calculates daily statistics per format
    """
    # Define standard format categories
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
    
    # Apply standard format grouping
    df['format_grouped'] = df['standardized_format'].map(
        lambda x: STANDARD_FORMATS.get(x, 'Other')
    )
    
    # Group by date and format, calculate statistics
    format_daily_stats = df.groupby(['processing_date', 'format_grouped']).agg({
        'price': ['count', 'mean', 'median', 'min', 'max'],
        'main_category_rank': 'min',  # Best rank achieved
        'review_count': 'sum'
    }).round(2)
    
    # Flatten column names
    format_daily_stats.columns = [
        f'price_{x[1]}' if x[0] == 'price' else f'{x[0]}' 
        for x in format_daily_stats.columns
    ]
    
    return format_daily_stats.reset_index()

def prepare_category_price_data(df):
    """
    Prepare category-based price analysis data for PowerBI
    - Focuses on main categories
    - Includes daily price trends
    """
    category_daily_stats = df.groupby(['processing_date', 'main_category']).agg({
        'price': ['count', 'mean', 'median', 'min', 'max'],
        'main_category_rank': 'min',
        'review_count': 'sum'
    }).round(2)
    
    # Flatten column names
    category_daily_stats.columns = [
        f'price_{x[1]}' if x[0] == 'price' else f'{x[0]}' 
        for x in category_daily_stats.columns
    ]
    
    return category_daily_stats.reset_index()

def prepare_bestseller_details(df):
    """
    Prepare detailed bestseller tracking data for PowerBI
    - Tracks individual bestsellers over time
    - Includes category and subcategory rankings
    """
    bestseller_tracking = df.groupby(['processing_date', 'isbn13', 'asin']).agg({
        'price': 'first',
        'standardized_format': 'first',
        'main_category': 'first',
        'main_category_rank': 'first',
        'category_1': 'first',
        'category_1_rank': 'first',
        'category_2': 'first',
        'category_2_rank': 'first',
        'category_3': 'first',
        'category_3_rank': 'first',
        'rating': 'first',
        'review_count': 'first',
        'title': 'first',
        'author': 'first'
    }).reset_index()
    
    return bestseller_tracking

def prepare_price_changes(df):
    """
    Analyze price changes for each product over time
    Handles both single-day and multi-day datasets
    """
    # Check if we have multiple dates
    if df['processing_date'].nunique() <= 1:
        # For single day data, return empty dataframe with correct structure
        return pd.DataFrame(columns=[
            'isbn13', 'price_change', 'processing_date', 'title', 
            'author', 'standardized_format', 'main_category',
            'previous_price', 'new_price'
        ])
    
    # Sort by date and calculate price changes for multi-day data
    df_sorted = df.sort_values(['isbn13', 'processing_date'])
    
    # Calculate price changes
    df_sorted['previous_price'] = df_sorted.groupby('isbn13')['price'].shift(1)
    df_sorted['price_change'] = df_sorted['price'] - df_sorted['previous_price']
    
    # Select only rows where price changed
    price_changes = df_sorted[df_sorted['price_change'] != 0].copy()
    
    # Select relevant columns
    price_changes = price_changes[[
        'isbn13', 'price_change', 'processing_date', 'title', 
        'author', 'standardized_format', 'main_category',
        'previous_price', 'price'
    ]].rename(columns={'price': 'new_price'})
    
    return price_changes

def export_powerbi_data(df):
    """
    Main function to prepare and export all data for PowerBI
    """
    # Create output directory
    output_dir = Path('../data/powerbi')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Prepare all datasets
    format_stats = prepare_format_price_data(df)
    category_stats = prepare_category_price_data(df)
    bestseller_tracking = prepare_bestseller_details(df)
    price_changes = prepare_price_changes(df)
    
    # Export to CSV with timestamp
    timestamp = datetime.now().strftime('%Y%m%d')
    
    # Export main datasets
    format_stats.to_csv(
        output_dir / f'format_price_analysis_{timestamp}.csv',
        index=False
    )
    category_stats.to_csv(
        output_dir / f'category_price_analysis_{timestamp}.csv',
        index=False
    )
    bestseller_tracking.to_csv(
        output_dir / f'bestseller_tracking_{timestamp}.csv',
        index=False
    )
    price_changes.to_csv(
        output_dir / f'price_changes_{timestamp}.csv',
        index=False
    )
    
    # Export a summary of what was processed
    summary = pd.DataFrame({
        'dataset': ['format_stats', 'category_stats', 'bestseller_tracking', 'price_changes'],
        'record_count': [
            len(format_stats),
            len(category_stats),
            len(bestseller_tracking),
            len(price_changes)
        ],
        'export_date': timestamp
    })
    
    summary.to_csv(output_dir / f'export_summary_{timestamp}.csv', index=False)
    
    return {
        'format_stats': format_stats,
        'category_stats': category_stats,
        'bestseller_tracking': bestseller_tracking,
        'price_changes': price_changes,
        'summary': summary
    }

if __name__ == "__main__":
    # Load the master dataset
    df = pd.read_csv('../data/processed/master_bestsellers.csv')
    
    # Run the export
    results = export_powerbi_data(df)
    
    # Print summary of export
    print("\n=== Export Summary ===")
    print(results['summary'].to_string(index=False))