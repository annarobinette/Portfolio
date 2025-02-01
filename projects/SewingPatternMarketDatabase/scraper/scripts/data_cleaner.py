import pandas as pd
import re

def clean_pattern_name(row):
    """Clean pattern name by removing company name and (free)"""
    name = row['pattern_name']
    company = row['pattern_company']
    
    # Replace '&' with 'and' in company name for consistency in removal
    company_variants = [
        company,
        company.replace(' and ', ' & '),
        company.replace(' & ', ' and ')
    ]
    
    # Remove company name from pattern name
    for variant in company_variants:
        name = name.replace(f"{variant} ", "")
        name = name.replace(f"{variant}'s ", "")
    
    # Remove (free) and any extra whitespace
    name = name.replace('(free)', '').strip()
    
    return name

def clean_company_name(name):
    """Clean company name to be in Title Case with 'and' not '&'"""
    # Replace '&' with 'and'
    name = name.replace('&', 'and')
    
    # Title case the name
    words = name.split()
    cleaned_words = []
    
    for word in words:
        # Keep 'and', 'by' lowercase if they're not at the start
        if word.lower() in ['and', 'by'] and cleaned_words:
            cleaned_words.append(word.lower())
        else:
            cleaned_words.append(word.capitalize())
    
    return ' '.join(cleaned_words)

def clean_price(price):
    """Extract just the numerical price value"""
    # Extract all digits and decimal points
    if pd.isna(price):
        return None
    
    # Handle 'From' prices
    if 'From' in price:
        price = price.split('From')[-1]
    
    # Extract the first price if there are multiple
    if '/' in price:
        price = price.split('/')[0]
    
    # Extract digits and decimal point
    digits = re.findall(r'[\d.]+', price)
    if digits:
        return float(digits[0])
    return None

def clean_data(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Clean pattern names
    df['pattern_name'] = df.apply(clean_pattern_name, axis=1)
    
    # Clean company names
    df['pattern_company'] = df['pattern_company'].apply(clean_company_name)
    
    # Clean prices
    df['price'] = df['price'].apply(clean_price)
    
    # Remove any leading/trailing whitespace from string columns
    string_columns = ['pattern_name', 'pattern_company', 'description', 
                     'suggested_fabrics', 'fabric_requirements', 'sizing', 
                     'notions', 'pattern_includes']
    
    for col in string_columns:
        if col in df.columns:
            df[col] = df[col].str.strip()
    
    # Save cleaned data
    output_path = file_path.replace('.csv', '_cleaned.csv')
    df.to_csv(output_path, index=False)
    
    # Print some statistics
    print(f"Cleaned {len(df)} patterns")
    print("\nSample of cleaned pattern names:")
    print(df[['pattern_company', 'pattern_name']].head())
    print("\nSample of cleaned prices:")
    print(df['price'].head())
    
    return df

if __name__ == "__main__":
    # Clean the data
    cleaned_df = clean_data('sewing_patterns_kids.csv')