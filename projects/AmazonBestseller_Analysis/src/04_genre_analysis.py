import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

def prepare_main_category_data(df):
    """
    Prepare main category performance data for PowerBI
    Tracks daily performance metrics for main categories
    """
    main_category_stats = df.groupby(['processing_date', 'main_category']).agg({
        'isbn13': 'count',  # Number of books in category
        'main_category_rank': ['min', 'max', 'mean'],  # Rank statistics
        'price': ['mean', 'median'],
        'rating': ['mean', 'min', 'max'],
        'review_count': 'sum'
    }).round(2)
    
    # Flatten column names
    main_category_stats.columns = [
        f'{x[0]}_{x[1]}' if x[1] != '' else x[0]
        for x in main_category_stats.columns
    ]
    
    return main_category_stats.reset_index()

def prepare_subcategory_data(df):
    """
    Prepare subcategory analysis for PowerBI
    Handles all three category levels
    """
    # Process each category level
    category_levels = []
    
    for i in range(1, 4):
        category_col = f'category_{i}'
        rank_col = f'category_{i}_rank'
        
        if category_col in df.columns and rank_col in df.columns:
            level_stats = df.groupby(['processing_date', category_col]).agg({
                'isbn13': 'count',
                rank_col: ['min', 'max', 'mean'],
                'price': ['mean', 'median'],
                'rating': 'mean',
                'review_count': 'sum'
            }).round(2)
            
            # Flatten column names and add category level
            level_stats.columns = [
                f'{x[0]}_{x[1]}' if x[1] != '' else x[0]
                for x in level_stats.columns
            ]
            
            level_data = level_stats.reset_index()
            level_data['category_level'] = i
            level_data = level_data.rename(columns={category_col: 'category_name'})
            
            category_levels.append(level_data)
    
    # Combine all category levels
    if category_levels:
        return pd.concat(category_levels, ignore_index=True)
    return pd.DataFrame()  # Return empty DataFrame if no category data

def prepare_category_format_analysis(df):
    """
    Analyze format distribution within categories
    Uses the standardized format groupings
    """
    # Define standard format categories (same as price analysis)
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
    
    # Calculate format distribution by category
    format_dist = df.groupby(
        ['processing_date', 'main_category', 'format_grouped']
    ).agg({
        'isbn13': 'count',
        'price': ['mean', 'median'],
        'rating': 'mean',
        'review_count': 'sum'
    }).round(2)
    
    # Flatten column names
    format_dist.columns = [
        f'{x[0]}_{x[1]}' if x[1] != '' else x[0]
        for x in format_dist.columns
    ]
    
    return format_dist.reset_index()

def prepare_category_crossover(df):
    """
    Analyze books appearing in multiple categories
    Tracks category combinations and their frequency
    """
    # Create pairs of categories where books appear in multiple categories
    category_pairs = []
    
    for index, row in df.iterrows():
        categories = [
            row['main_category'],
            row.get('category_1'),
            row.get('category_2'),
            row.get('category_3')
        ]
        # Remove None/NaN values
        categories = [c for c in categories if pd.notna(c)]
        categories = list(set(categories))  # Remove duplicates
        
        # Create pairs if book appears in multiple categories
        if len(categories) > 1:
            for i in range(len(categories)):
                for j in range(i + 1, len(categories)):
                    category_pairs.append({
                        'processing_date': row['processing_date'],
                        'category_1': categories[i],
                        'category_2': categories[j],
                        'isbn13': row['isbn13'],
                        'title': row['title']
                    })
    
    if category_pairs:
        crossover_df = pd.DataFrame(category_pairs)
        # Calculate frequency of category pairs
        pair_stats = crossover_df.groupby(
            ['processing_date', 'category_1', 'category_2']
        ).agg({
            'isbn13': 'count'  # Number of books in both categories
        }).reset_index()
        
        return pair_stats
    
    return pd.DataFrame()  # Return empty DataFrame if no crossover

def export_category_analysis(df):
    """
    Main function to prepare and export all category analysis for PowerBI
    """
    # Create output directory
    output_dir = Path('../data/powerbi')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Prepare all datasets
    main_category_stats = prepare_main_category_data(df)
    subcategory_stats = prepare_subcategory_data(df)
    format_distribution = prepare_category_format_analysis(df)
    category_crossover = prepare_category_crossover(df)
    
    # Export to CSV with timestamp
    timestamp = datetime.now().strftime('%Y%m%d')
    
    # Export main datasets
    main_category_stats.to_csv(
        output_dir / f'main_category_analysis_{timestamp}.csv',
        index=False
    )
    subcategory_stats.to_csv(
        output_dir / f'subcategory_analysis_{timestamp}.csv',
        index=False
    )
    format_distribution.to_csv(
        output_dir / f'category_format_analysis_{timestamp}.csv',
        index=False
    )
    category_crossover.to_csv(
        output_dir / f'category_crossover_{timestamp}.csv',
        index=False
    )
    
    # Export a summary of what was processed
    summary = pd.DataFrame({
        'dataset': [
            'main_category_stats', 
            'subcategory_stats',
            'format_distribution',
            'category_crossover'
        ],
        'record_count': [
            len(main_category_stats),
            len(subcategory_stats),
            len(format_distribution),
            len(category_crossover)
        ],
        'export_date': timestamp
    })
    
    summary.to_csv(output_dir / f'category_export_summary_{timestamp}.csv', index=False)
    
    return {
        'main_category_stats': main_category_stats,
        'subcategory_stats': subcategory_stats,
        'format_distribution': format_distribution,
        'category_crossover': category_crossover,
        'summary': summary
    }

if __name__ == "__main__":
    # Load the master dataset
    df = pd.read_csv('../data/processed/master_bestsellers.csv')
    
    # Run the export
    results = export_category_analysis(df)
    
    # Print summary of export
    print("\n=== Export Summary ===")
    print(results['summary'].to_string(index=False))