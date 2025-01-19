# language_analysis_functions.py
import pandas as pd

def analyze_language_distribution(df):
    """
    Analyze and display detailed language distribution statistics
    
    Parameters:
    df (pandas.DataFrame): DataFrame containing a 'languages' column
    
    Returns:
    pandas.DataFrame: DataFrame with language statistics
    """
    # Split the language strings and create individual entries
    languages = df['languages'].str.split('; ').explode()
    
    # Calculate basic counts and percentages
    lang_stats = pd.DataFrame({
        'count': languages.value_counts(),
        'percentage': (languages.value_counts() / len(df) * 100).round(1)
    }).reset_index()
    
    # Rename columns
    lang_stats.columns = ['Language', 'Number of Books', 'Percentage']
    
    # Add cumulative percentage
    lang_stats['Cumulative %'] = lang_stats['Percentage'].cumsum().round(1)
    
    # Calculate average downloads per language
    lang_downloads = df.copy()
    lang_downloads['languages'] = lang_downloads['languages'].str.split('; ')
    lang_downloads = lang_downloads.explode('languages')
    avg_downloads = lang_downloads.groupby('languages')['download_count'].agg(['mean', 'median']).round(1)
    
    # Merge with main stats
    lang_stats = lang_stats.merge(
        avg_downloads, 
        left_on='Language', 
        right_index=True, 
        how='left'
    )
    
    # Rename columns
    lang_stats = lang_stats.rename(columns={
        'mean': 'Avg Downloads',
        'median': 'Median Downloads'
    })
    
    # Print formatted statistics
    print("\nLanguage Distribution Analysis")
    print("-" * 80)
    print(f"Total number of unique languages: {len(lang_stats)}")
    print(f"Languages making up 90% of collection: {len(lang_stats[lang_stats['Cumulative %'] <= 90])}")
    print("\nDetailed Statistics:")
    print(lang_stats.to_string(index=False))
    
    # Additional insights
    print("\nKey Insights:")
    print(f"- {lang_stats['Language'].iloc[0]} dominates with {lang_stats['Percentage'].iloc[0]}% of the collection")
    print(f"- Top 3 languages account for {lang_stats['Percentage'].iloc[:3].sum():.1f}% of all books")
    print(f"- Most downloaded language (avg): {lang_stats.nlargest(1, 'Avg Downloads')['Language'].iloc[0]}")
    print(f"- Number of languages with <1% representation: {len(lang_stats[lang_stats['Percentage'] < 1])}")
    
    return lang_stats


lang_stats = analyze_language_distribution(df)


def verify_language_counts(df):
    """Verify language counts using different methods"""
    
    # Method 1: Raw count of unique values (including combinations)
    raw_count = df['languages'].nunique()
    
    # Method 2: Count of individual languages after splitting
    individual_langs = df['languages'].str.split('; ').explode().unique()
    
    # Print both counts and show some examples
    print("Language Count Analysis")
    print("-" * 50)
    print(f"Raw unique entries (including combinations): {raw_count}")
    print(f"Unique individual languages: {len(individual_langs)}")
    
    # Show some examples of multi-language entries
    multi_lang = df[df['languages'].str.contains(';')]
    print("\nExample of multi-language entries:")
    print(multi_lang['languages'].head().to_string())
    
    return raw_count, len(individual_langs)

raw_count, individual_count = verify_language_counts(df)