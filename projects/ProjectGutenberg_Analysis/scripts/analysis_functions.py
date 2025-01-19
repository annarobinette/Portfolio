# analysis_functions.py

def check_data_quality(df):
    """Perform basic data quality checks"""
    print("Data Quality Report")
    print("-" * 50)
    
    # Check for missing values
    missing_data = df.isnull().sum()
    print("\nMissing Values:")
    print(missing_data[missing_data > 0])
    
    # Check unique values in key fields
    print("\nUnique Languages:", df['languages'].nunique())
    print("Unique Authors:", df['authors'].nunique())
    
    # Basic statistics for download counts
    print("\nDownload Count Statistics:")
    print(df['download_count'].describe())

check_data_quality(df)
