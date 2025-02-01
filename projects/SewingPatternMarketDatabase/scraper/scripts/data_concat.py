import pandas as pd
import glob
import re
from pathlib import Path

# Set the directory path
dir_path = '/Users/anna/Documents/GitHub/Portfolio/projects/SewingPatternMarketDatabase/scraper/data/processed'

# Get all CSV files matching the pattern
pattern = f"{dir_path}/sewing_patterns_*_cleaned.csv"
csv_files = glob.glob(pattern)

# Initialize list to store dataframes
dfs = []

# Process each file
for file in csv_files:
    # Extract type from filename using regex
    type_match = re.search(r'sewing_patterns_(.+?)_cleaned\.csv', Path(file).name)
    if type_match:
        pattern_type = type_match.group(1)
        
        # Read the CSV
        df = pd.read_csv(file)
        
        # Add type column
        df['type'] = pattern_type
        
        # Append to list of dataframes
        dfs.append(df)

# Concatenate all dataframes
combined_df = pd.concat(dfs, ignore_index=True)

# Save the combined dataset (optional)
output_path = f"{dir_path}/combined_patterns.csv"
combined_df.to_csv(output_path, index=False)

print(f"Processed {len(csv_files)} files")
print(f"Combined dataset shape: {combined_df.shape}")
print("\nSample of combined data:")
print(combined_df.head())
print("\nTypes found:", combined_df['type'].unique())