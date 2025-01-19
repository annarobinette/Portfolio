# Import necessary libraries
import pandas as pd
import numpy as np
import os
import glob
import re
from datetime import datetime

today = datetime.now().strftime("%Y%m%d")
raw_file_path = f'../data/raw/daily_bestsellers/bestsellers_{today}.csv'
master_file_path = '../data/processed/master_bestsellers.csv'

print(f"Processing data for {today}")
print(f"Loading raw data from: {raw_file_path}")

# Load today's data
df_today = pd.read_csv(raw_file_path)
print(f"Loaded {len(df_today)} records from today's scrape")
print("Dataset Info:")
print(df_today.info())

print("Missing Values:")
print(df_today.isnull().sum())

print("Value Counts for Format:")
print(df_today['format'].value_counts(dropna=False))

print("Value Counts for Category:")
print(df_today['category'].value_counts())
# Convert integer columns from float
integer_columns = ['review_count', 'page_count', 'isbn13']
for col in integer_columns:
    df_today[col] = df_today[col].fillna(0)
    df_today[col] = df_today[col].astype(int)

def extract_age_range(age_str):
    """Extract age range from string formats like '1-2', '7+', etc."""
    if pd.isna(age_str):
        return None, None
    
    age_str = str(age_str).lower().strip()
    
    # Handle '+' format (e.g., '7+')
    if '+' in age_str:
        start_age = int(''.join(filter(str.isdigit, age_str)))
        return start_age, None
    
    # Handle range format (e.g., '1-2', '7 to 9')
    numbers = [int(n) for n in ''.join(c if c.isdigit() else ' ' for c in age_str).split()]
    if len(numbers) >= 2:
        return numbers[0], numbers[1]
    elif len(numbers) == 1:
        return numbers[0], None
        
    return None, None

def map_to_standard_range(start_age, end_age):
    """Map extracted ages to standard publishing ranges"""
    standard_ranges = [
        (0, 2, '0-2'),
        (3, 5, '3-5'),
        (6, 8, '6-8'),
        (9, 12, '9-12'),
        (13, 14, '13-14'),
        (15, 18, '15-18')
    ]
    
    if start_age is None:
        return None
        
    # Handle '+' format
    if end_age is None:
        if start_age <= 2:
            return '0-2'
        elif start_age <= 5:
            return '3-5'
        elif start_age <= 8:
            return '6-8'
        elif start_age <= 12:
            return '9-12'
        elif start_age <= 14:
            return '13-14'
        else:
            return '15-18'
            
    # Handle range format
    avg_age = (start_age + end_age) / 2
    for low, high, range_str in standard_ranges:
        if low <= avg_age <= high:
            return range_str
            
    # Default to closest range
    if avg_age < 0:
        return '0-2'
    elif avg_age > 18:
        return '15-18'
    
    return None

def standardise_age_range(row):
    """Create standardised age ranges based on target_age_range or category"""
    # First try to use target_age_range
    if pd.notna(row['target_age_range']):
        start_age, end_age = extract_age_range(row['target_age_range'])
        if start_age is not None:
            std_range = map_to_standard_range(start_age, end_age)
            if std_range:
                return std_range
    
    # If no valid age range found, use category
    category = str(row['category']).lower()
    category_mappings = {
        'baby': '0-2',
        'toddler': '0-2',
        'preschool': '3-5',
        'kindergarten': '3-5',
        'early reader': '6-8',
        'ages 6-8': '6-8',
        'middle grade': '9-12',
        'ages 9-12': '9-12',
        'young teen': '13-14',
        'ages 12-14': '13-14',
        'teen': '15-18',
        'young adult': '15-18',
        'ages 14-18': '15-18'
    }
    
    for key, value in category_mappings.items():
        if key in category:
            return value
            
    return None

# Apply age range standardization
df_today['age_range_std'] = df_today.apply(standardise_age_range, axis=1)

# Create age group categories
age_group_mapping = {
    '0-2': '0-2',
    '3-5': '3-5',
    '6-8': '6-8',
    '9-12': '9-12',
    '13-14': '13-14',
    '15-18': '15-18'
}
df_today['age_range_std'] = df_today['age_range_std'].map(age_group_mapping)
#df_today = df_today.drop(['target_age_range','target_age_group'], axis =1)
# Print age range distribution
print("\nAge Range Distribution:")
print(df_today['age_range_std'].value_counts(dropna=False))
# Rename basic ranking columns for clarity
df_today = df_today.rename(columns={
    'rank': 'main_category_rank',
    'category': 'main_category'
})
def parse_category_ranking(category_str):
    """Parse category ranking string into separate categories and ranks"""
    if pd.isna(category_str):
        return pd.Series({
            'category_1': None, 
            'category_1_rank': pd.NA,
            'category_2': None, 
            'category_2_rank': pd.NA,
            'category_3': None, 
            'category_3_rank': pd.NA
        })
        
    # Split into individual category-rank pairs
    categories = [x.strip() for x in str(category_str).split('|')]
    
    # Initialise results dictionary
    results = {}
    
    # Process up to 3 categories
    for i in range(3):
        # Set default values
        results[f'category_{i+1}'] = None
        results[f'category_{i+1}_rank'] = pd.NA
        
        # If data for this position, process it
        if i < len(categories):
            cat_data = categories[i].strip()
            
            # Extract rank (first number in string)
            rank_match = re.match(r'(\d+)', cat_data)
            if rank_match:
                results[f'category_{i+1}_rank'] = pd.NA if rank_match is None else int(rank_match.group(1))
                
                # Extract category (everything after 'in ')
                category = re.search(r' in (.+)', cat_data)
                if category:
                    results[f'category_{i+1}'] = category.group(1).strip()
    
    # Convert to series with proper types
    series = pd.Series(results)
    for i in range(1, 4):
        if pd.notna(series[f'category_{i}_rank']):
            series[f'category_{i}_rank'] = int(series[f'category_{i}_rank'])
    return series
# Apply the parsing function and add new columns
df_today = df_today.rename(columns={'rank': 'main_category_rank', 'category': 'main_category'})
parsed_categories = df_today['category_ranks'].apply(parse_category_ranking)
df_today = pd.concat([df_today, parsed_categories], axis=1)
# Clean titles
df_today['clean_title'] = df_today['title'].str.strip()
df_today['clean_title'] = df_today['clean_title'].str.replace('"', '"').str.replace('"', '"')

# Clean author names
df_today['author'] = df_today['author'].str.strip()
df_today['author'] = df_today['author'].str.replace(r'\s+', ' ', regex=True)
format_mapping = {
    'paperback': 'Paperback',
    'hardcover': 'Hardcover',
    'hard cover': 'Hardcover',
    'board book': 'Board Book',
    'board': 'Board Book',
    'kindle': 'Digital',
    'ebook': 'Digital',
    'e-book': 'Digital',
    'audiobook': 'Audio',
    'audio book': 'Audio'
}

df_today['standardised_format'] = df_today['format'].str.lower().map(format_mapping)
df_today['processing_date'] = today
df_today['data_batch'] = f'batch_{today}'

validation_issues = []

# Check for critical issues
if len(df_today) == 0:
    validation_issues.append("No records found in today's data")
    
if df_today['price'].isnull().all():
    validation_issues.append("All prices are missing")
    
if df_today['standardised_format'].isnull().all():
    validation_issues.append("All formats are missing")

# Check for suspicious patterns
    
if df_today['price'].max() > 100:
    validation_issues.append(f"Suspicious high price found: {df_today['price'].max()}")

if len(validation_issues) > 0:
    print("\nWARNING: Data validation issues found:")
    for issue in validation_issues:
        print(f"- {issue}")
    print("\nPlease review the issues before proceeding.")
else:
    print("Data validation passed")

if os.path.exists(master_file_path):
    # Load existing master data
    df_master = pd.read_csv(master_file_path)
    print(f"Loaded {len(df_master)} existing records from master dataset")
    
    # Append new data
    df_master = pd.concat([df_master, df_today], ignore_index=True)
    
    # Remove duplicates based on business key (adjust columns as needed)
    df_master = df_master.drop_duplicates(
        subset=['clean_title', 'author', 'standardised_format', 'processing_date'],
        keep='last'
    )
else:
    print("No existing master dataset found. Creating new one.")
    df_master = df_today

# Save updated master dataset
df_master.to_csv(master_file_path, index=False)
print("\nDaily Processing Summary:")
print("-" * 50)
print(f"Date: {today}")
print(f"Records processed: {len(df_today)}")
print(f"Records in master dataset: {len(df_master)}")
print("\nFormat Distribution (Today):")
print(df_today['standardised_format'].value_counts())
print("\nPrice Statistics (Today):")
print(df_today['price'].describe())

# 10. Save daily summary to log
log_file_path = '../data/processed/processing_log.csv'
daily_summary = {
    'date': today,
    'records_processed': len(df_today),
    'total_records': len(df_master),
    'validation_issues': '; '.join(validation_issues) if validation_issues else 'None'
}

if os.path.exists(log_file_path):
    df_log = pd.read_csv(log_file_path)
else:
    df_log = pd.DataFrame(columns=['date', 'records_processed', 'total_records', 'validation_issues'])

df_log = pd.concat([df_log, pd.DataFrame([daily_summary])], ignore_index=True)
df_log.to_csv(log_file_path, index=False)

print("\nProcessing complete. Check processing_log.csv for historical records.")
