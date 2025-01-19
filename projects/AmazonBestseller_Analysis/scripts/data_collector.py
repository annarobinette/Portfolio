class GutenbergCollector:
    def __init__(self):
        self.base_url = 'https://gutendex.com/books'
        self.books = []
    
    def fetch_catalog(self, max_pages=5000):
        """Fetch book metadata from the Gutenberg API"""
        next_page = self.base_url
        
        with tqdm(total=max_pages, desc='Fetching pages') as pbar:
            while next_page and len(self.books) < max_pages * 32:  # 32 books per page
                try:
                    response = requests.get(next_page)
                    response.raise_for_status()
                    data = response.json()
                    
                    # Process each book to add derived fields
                    for book in data['results']:
                        # Get text length from formats if available
                        formats = book.get('formats', {})
                        if 'text/plain' in formats:
                            # Check if the format is a dictionary or string
                            format_info = formats['text/plain']
                            if isinstance(format_info, dict):
                                book['text_length'] = format_info.get('size', 0)
                            else:
                                book['text_length'] = 0
                        else:
                            book['text_length'] = 0
                            
                        # Get available formats list
                        book['available_formats'] = list(formats.keys())
                    
                    self.books.extend(data['results'])
                    next_page = data.get('next')
                    pbar.update(1)
                    
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching data: {e}")
                    break
        
        print(f"Successfully collected metadata for {len(self.books)} books")
        return self.books
    
    def save_raw_data(self):
        """Save the raw JSON data"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'../data/raw/gutenberg_catalog_{timestamp}.json'
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.books, f, ensure_ascii=False, indent=2)
        
        print(f"Raw data saved to {filename}")
        return filename

# Initialize the collector and fetch the data
collector = GutenbergCollector()
books = collector.fetch_catalog(max_pages=5000) 
raw_file = collector.save_raw_data()