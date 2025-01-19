# data_processor.py
import pandas as pd

def process_raw_data(books):
    """Transform raw book data into a structured DataFrame"""
    processed_books = []
    
    for book in books:
        processed_book = {
            'id': book['id'],
            'title': book['title'],
            'authors': '; '.join([author['name'] for author in book['authors']]),
            'languages': '; '.join(book['languages']),
            'download_count': book['download_count'],
            'subjects': '; '.join(book['subjects'] if book['subjects'] else []),
            'bookshelves': '; '.join(book['bookshelves'] if book['bookshelves'] else []),
            'copyright': book['copyright']
        }
        processed_books.append(processed_book)
    
    return pd.DataFrame(processed_books)

# Process collected data
df = process_raw_data(books)

# Display basic information about dataset
print("Dataset Overview:")
print("-" * 50)
print(df.info())
print("\nSample of processed data:")
display(df.head())