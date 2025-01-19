import pandas as pd
from datetime import datetime, timedelta
import os
from pathlib import Path

# Create output directory if it doesn't exist
Path('../data/powerbi').mkdir(parents=True, exist_ok=True)

# Create sample data
data = {
    'processing_date': [datetime.now().strftime('%Y%m%d')] * 5,
    'category': ['Fiction', 'Non-Fiction', 'Children', 'Fiction', 'Non-Fiction'],
    'format': ['Paperback', 'Hardback', 'Board Book', 'Digital', 'Paperback'],
    'price': [12.99, 24.99, 8.99, 4.99, 15.99],
    'books_count': [45, 32, 28, 15, 22],
    'avg_rating': [4.5, 4.2, 4.8, 4.1, 4.3]
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
today = datetime.now().strftime('%Y%m%d')
filename = f'../data/powerbi/category_format_analysis_{today}.csv'
df.to_csv(filename, index=False)

print(f"Created sample file: {filename}")
print("\nSample data preview:")
print(df.head())