import pandas as pd

# Read the garment_types.csv file
df = pd.read_csv('../scraper/data/generated/garment_types.csv')

# Extract unique combinations and create a new dataframe
categories_df = df[['garment_family', 'category', 'typical_fabric_type']].drop_duplicates()

# Reset index to create an auto-incrementing category_id
categories_df = categories_df.reset_index(drop=True)
categories_df.index += 1  # Start from 1 instead of 0
categories_df.insert(0, 'category_id', categories_df.index)

# Rename columns to match database schema
categories_df = categories_df.rename(columns={'category': 'category_name'})

# Save to CSV
categories_df.to_csv('../scraper/data/generated/garment_categories.csv', index=False, quoting=1)

# Print summary
print(f"Created garment_categories.csv with {len(categories_df)} unique categories")
print("\nFirst few rows:")
print(categories_df.head())

# Create a mapping file for later use with garment_types
mapping_df = df.merge(categories_df, 
                     on=['garment_family', 'typical_fabric_type'],
                     how='left')

# Save mapping for reference
mapping_df[['type_name', 'category_id']].to_csv('category_mapping.csv', index=False)

print("\nMapping file created as category_mapping.csv")