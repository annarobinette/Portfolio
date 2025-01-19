# Import necessary libraries
import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
from tqdm import tqdm
import yaml
import logging
from datetime import datetime
import re

# Load configuration settings
with open('../config/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

# Setup logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../logs/scraping.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

logger.info("Starting bestseller data collection process")

def print_data_status(df):
    """
    Print detailed status of data completeness
    """
    total = len(df)
    print("\nData Completeness Report:")
    print("-" * 50)
    for column in df.columns:
        missing = df[column].isna().sum()
        complete = total - missing
        percentage = (complete/total) * 100
        print(f"{column:20s}: {complete:4d}/{total:4d} ({percentage:6.2f}%)")

def fetch_bestseller_page(url, headers, max_retries=3, backoff_factor=2):
    """
    Fetches a bestseller page with exponential backoff retry logic.
    """
    for attempt in range(max_retries):
        try:
            logger.info(f"Fetching data from {url} (Attempt {attempt + 1}/{max_retries})")
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                logger.info("Successfully retrieved page")
                return response.text
            elif response.status_code == 429:
                wait_time = (backoff_factor ** attempt) * 3  # Base delay of 3 seconds
                logger.warning(f"Rate limited. Waiting {wait_time} seconds before retry")
                time.sleep(wait_time)
                continue
            else:
                logger.warning(f"Received status code {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching page: {e}")
            if attempt < max_retries - 1:
                wait_time = (backoff_factor ** attempt) * 3
                time.sleep(wait_time)
            else:
                return None
    
    return None

def analyze_html_structure(html):
    """
    Analyzes the HTML structure to help debug parsing issues.
    """
    soup = BeautifulSoup(html, 'html.parser')
    analysis = {
        "total_divs": len(soup.find_all('div')),
        "div_classes": {},
        "potential_containers": [],
        "links": len(soup.find_all('a')),
        "text_length": len(soup.get_text()),
        "title": soup.title.string if soup.title else None
    }
    
    # Analyze div classes
    for div in soup.find_all('div', class_=True):
        for class_name in div['class']:
            analysis["div_classes"][class_name] = analysis["div_classes"].get(class_name, 0) + 1
            
            # Look for promising container classes
            if any(term in class_name.lower() for term in ['item', 'product', 'book', 'result']):
                if class_name not in analysis["potential_containers"]:
                    analysis["potential_containers"].append(class_name)
    
    logger.info("\nHTML Structure Analysis:")
    logger.info(f"Page Title: {analysis['title']}")
    logger.info(f"Total Divs: {analysis['total_divs']}")
    logger.info(f"Total Links: {analysis['links']}")
    logger.info("\nMost Common Div Classes:")
    for class_name, count in sorted(analysis["div_classes"].items(), 
                                  key=lambda x: x[1], 
                                  reverse=True)[:10]:
        logger.info(f"{class_name}: {count}")
    logger.info("\nPotential Container Classes:")
    for container in analysis["potential_containers"]:
        logger.info(f"- {container}")
    
    return analysis

def parse_bestseller_data(html, base_url="https://www.amazon.co.uk"):
    """
    Enhanced parser for Amazon UK bestseller data
    """
    logger.info("Parsing bestseller data")
    soup = BeautifulSoup(html, 'html.parser')
    books = []
    
    # Find all book items in the grid
    items = soup.select('div[class*="_cDEzb_grid-cell_1uMOS"]')
    
    if not items:
        logger.warning("No items found with grid cell selector")
        return []
    
    logger.info(f"Found {len(items)} potential book items")
    
    for i, item in enumerate(items, 1):
        try:
            book = {}
            
            # Extract rank
            rank_elem = item.select_one('.zg-bdg-text')
            if rank_elem:
                rank_text = rank_elem.text.strip('#')
                try:
                    book['rank'] = int(rank_text)
                except ValueError:
                    logger.warning(f"Could not parse rank from {rank_text}")
            
            # Extract title
            title_elem = item.select_one('div[class*="_cDEzb_p13n-sc-css-line-clamp-1"]')
            if title_elem:
                book['title'] = title_elem.text.strip()
            
            # Extract author
            author_elem = item.select_one('a.a-size-small.a-link-child div')
            if author_elem:
                book['author'] = author_elem.text.strip()
            
            # Extract rating and review count
            rating_elem = item.select_one('.a-icon-star-small span.a-icon-alt')
            if rating_elem:
                rating_text = rating_elem.text
                try:
                    book['rating'] = float(rating_text.split(' ')[0])
                except (ValueError, IndexError):
                    logger.warning(f"Could not parse rating from {rating_text}")
            
            review_count_elem = item.select_one('.a-icon-row span.a-size-small')
            if review_count_elem:
                try:
                    book['review_count'] = int(review_count_elem.text.replace(',', ''))
                except ValueError:
                    logger.warning(f"Could not parse review count from {review_count_elem.text}")
            
            # Extract format
            format_elem = item.select_one('span.a-size-small.a-color-secondary')
            if format_elem:
                book['format'] = format_elem.text.strip()
            
            # Extract price
            price_elem = item.select_one('span[class*="_cDEzb_p13n-sc-price"]')
            if price_elem:
                price_text = price_elem.text.strip('£')
                try:
                    book['price'] = float(price_text)
                except ValueError:
                    logger.warning(f"Could not parse price from {price_text}")
            
            # Extract URLs
            link_elem = item.select_one('a[href*="/dp/"]')
            if link_elem:
                href = link_elem.get('href', '')
                if href:
                    # Clean up URL
                    url_parts = href.split('/ref=')[0]  # Remove tracking parameters
                    book['product_url'] = f"{base_url}{url_parts}" if not href.startswith('http') else href
                    
                    # Extract ASIN
                    asin_match = re.search(r'/dp/([A-Z0-9]{10})/?', href)
                    if asin_match:
                        book['asin'] = asin_match.group(1)
                        # Construct high-quality image URL
                        book['image_url'] = f"https://images-eu.ssl-images-amazon.com/images/P/{book['asin']}.01.L.jpg"
            
            # Extract image URL if not already set
            if 'image_url' not in book:
                img_elem = item.select_one('img[src*="images-amazon"]')
                if img_elem:
                    book['image_url'] = img_elem.get('src', '')
            
            # Add timestamp
            book['timestamp'] = datetime.now().isoformat()
            
            # Validate and add to results
            if validate_book_entry(book):
                books.append(book)
                logger.debug(f"Successfully processed book {i}: {book.get('title', 'Unknown Title')}")
            else:
                logger.warning(f"Skipping item {i} - failed validation")
            
        except Exception as e:
            logger.error(f"Error processing item {i}: {str(e)}")
            continue
    
    # Log success statistics
    if books:
        logger.info(f"Successfully parsed {len(books)} books")
        fields = ['rank', 'title', 'author', 'price', 'format', 'rating', 'review_count']
        for field in fields:
            count = sum(1 for book in books if field in book and book[field] is not None)
            logger.info(f"{field} found in {count}/{len(books)} books ({count/len(books)*100:.1f}%)")
    else:
        logger.warning("No books were successfully parsed")
    
    return books


def extract_rank(item):
    """Extract bestseller rank"""
    rank_data = {
        'overall_rank': None,
        'category_ranks': []
    }
    
    # Main rank is now in zg-bdg-text
    rank_elem = item.select_one('.zg-bdg-text')
    if rank_elem:
        try:
            rank_text = rank_elem.text.strip('#')
            rank_num = int(rank_text)
            if 0 < rank_num <= 100:
                rank_data['overall_rank'] = rank_num
        except (ValueError, AttributeError):
            pass
    
    return rank_data

def extract_title_and_series(item):
    """Extract title and series information"""
    result = {
        'title': None,
        'series_name': None,
        'series_number': None
    }
    
    # Title is now in _cDEzb_p13n-sc-css-line-clamp-1_1Fn1y
    title_elem = item.select_one('div[class*="_cDEzb_p13n-sc-css-line-clamp-1"]')
    if title_elem:
        raw_title = title_elem.text.strip()
        if raw_title:
            # Series patterns
            series_patterns = [
                r'(.*?)\s*\((.*?)(?:Book|Volume|#)\s*(\d+)\)',
                r'(.*?):\s*(?:Book|Volume)\s*(\d+)\s*(?:of|in)\s*(.*?)\s*$'
            ]
            
            for pattern in series_patterns:
                match = re.search(pattern, raw_title, re.IGNORECASE)
                if match:
                    groups = match.groups()
                    result['title'] = groups[0].strip()
                    result['series_name'] = groups[1].strip() if len(groups) > 1 else None
                    result['series_number'] = int(groups[2]) if len(groups) > 2 else None
                    break
            else:
                result['title'] = raw_title
    
    return result

def extract_product_urls(item, base_url="https://www.amazon.co.uk"):
    """Extract product and image URLs"""
    urls = {
        'product_url': None,
        'image_url': None,
        'asin': None
    }
    
    # Product URL is in the main link
    link_elem = item.select_one('a[href*="/dp/"]')
    if link_elem:
        href = link_elem.get('href', '')
        if href:
            # Clean up URL
            url_parts = href.split('/ref=')[0]
            urls['product_url'] = f"{base_url}{url_parts}" if not href.startswith('http') else href
            
            # Extract ASIN
            asin_match = re.search(r'/dp/([A-Z0-9]{10})/?', href)
            if asin_match:
                urls['asin'] = asin_match.group(1)
                urls['image_url'] = f"https://images-eu.ssl-images-amazon.com/images/P/{urls['asin']}.01.L.jpg"
    
    # Direct image URL as backup
    if not urls['image_url']:
        img_elem = item.select_one('img[src*="images-amazon"]')
        if img_elem:
            urls['image_url'] = img_elem.get('src', '')
    
    return urls

def extract_format_details(item):
    """Extract format information"""
    format_info = {
        'format': None,
        'binding': None
    }
    
    # Format is in a-size-small a-color-secondary
    format_elem = item.select_one('span.a-size-small.a-color-secondary')
    if format_elem:
        format_text = format_elem.text.strip().lower()
        format_mapping = {
            'hardcover': {'format': 'Hardcover', 'binding': 'Hardbound'},
            'paperback': {'format': 'Paperback', 'binding': 'Perfect Bound'},
            'board book': {'format': 'Board Book', 'binding': 'Board'},
            'kindle': {'format': 'Digital', 'binding': None},
            'audio cd': {'format': 'Audio', 'binding': 'CD'}
        }
        
        for key, value in format_mapping.items():
            if key in format_text:
                format_info.update(value)
                break
    
    return format_info

def extract_rating_details(item):
    """Extract rating and review count"""
    rating_data = {
        'rating': None,
        'review_count': None
    }
    
    # Rating is in a-icon-alt
    rating_elem = item.select_one('.a-icon-star-small span.a-icon-alt')
    if rating_elem:
        rating_text = rating_elem.text.strip()
        try:
            rating = float(rating_text.split(' ')[0])
            if 0 <= rating <= 5:
                rating_data['rating'] = rating
        except (ValueError, IndexError):
            pass
    
    # Review count is in a-size-small
    review_elem = item.select_one('.a-icon-row span.a-size-small')
    if review_elem:
        try:
            count = int(review_elem.text.replace(',', ''))
            rating_data['review_count'] = count
        except ValueError:
            pass
    
    return rating_data

def extract_price(item):
    """Extract price information"""
    price_elem = item.select_one('span[class*="_cDEzb_p13n-sc-price"]')
    if price_elem:
        try:
            price_text = price_elem.text.strip('£')
            return float(price_text)
        except ValueError:
            return None
    return None

def extract_author(item):
    """Extract author information"""
    author_elem = item.select_one('a.a-size-small.a-link-child div')
    if author_elem:
        return author_elem.text.strip()
    return None

def validate_book_entry(book):
    """
    Validates book entry with detailed logging
    """
    logger.debug(f"Validating book entry: {book}")
    
    # Title is required
    if 'title' not in book or not book['title']:
        logger.debug("Validation failed: Missing title")
        return False
    
    # Need at least two additional pieces of information
    additional_fields = ['price', 'format', 'author', 'rank', 'rating']
    valid_fields = sum(1 for field in additional_fields if field in book and book[field] is not None)
    
    if valid_fields < 2:
        logger.debug(f"Validation failed: Only found {valid_fields} additional fields")
        return False
    
    # Price validation if present
    if 'price' in book and book['price'] is not None:
        try:
            price = float(book['price'])
            if price < 0:
                logger.debug(f"Validation failed: Invalid price {price}")
                return False
        except (ValueError, TypeError):
            logger.debug(f"Validation failed: Price conversion error for {book['price']}")
            return False
    
    logger.debug("Book validation passed")
    return True

# Main scraping loop
bestseller_data = []

for category in tqdm(config['categories']):
    logger.info(f"Processing category: {category['name']}")
    
    html = fetch_bestseller_page(
        category['url'], 
        config['scraping']['headers'],
        max_retries=config['scraping']['max_retries'],
        backoff_factor=config['scraping']['backoff_factor']
    )
    
    if html:
        books = parse_bestseller_data(html)
        for book in books:
            # Add category metadata
            book.update({
                'category': category['name'],
                'category_type': category.get('type'),
                'category_subtype': category.get('subtype'),
                'target_age_range': category.get('age_range')
            })
            bestseller_data.append(book)


# Column list
columns = [
    'rank', 
    'title', 
    'author',
    'price',
    'format',
    'rating',
    'review_count',
    'isbn10',
    'isbn13',
    'page_count',
    'category',
    'target_age_range',
    'timestamp',
    'asin',
    'product_url',
    'image_url',
    'category_ranks'
]

df = pd.DataFrame(bestseller_data)

# Ensure all columns exist
for col in columns:
    if col not in df.columns:
        df[col] = None

# Reorder columns
df = df[columns]

# Cross-reference data
def fill_missing_data(row):
    """
    Attempt to fill missing data by cross-referencing ASIN
    """
    if pd.isna(row['isbn10']) or pd.isna(row['isbn13']):
        if not pd.isna(row['asin']):
            # Could use ASIN to fetch additional details from product page
            pass
    
    if pd.isna(row['target_age_range']) and not pd.isna(row['category']):
        # Fill target age range based on category mapping
        category_age_mapping = {
            "Children's Books (Ages 6-8)": "6-8",
            "Middle Grade (Ages 9-12)": "9-12",
            "Young Teen (Ages 12-14)": "12-14",
            "Young Adult (Ages 14-18)": "14-18"
        }
        row['target_age_range'] = category_age_mapping.get(row['category'])
    
    return row

# Apply cross-referencing
df = df.apply(fill_missing_data, axis=1)

def parse_age_range(text):
    """
    Parse various age range formats
    """
    patterns = [
        (r'(\d+)\s*-\s*(\d+)\s*years', lambda m: f"{m.group(1)}-{m.group(2)}"),
        (r'(\d+)\+\s*years', lambda m: f"{m.group(1)}+"),
        (r'from\s*(\d+)\s*years', lambda m: f"{m.group(1)}+"),
        (r'ages\s*(\d+)(?:\s*-\s*(\d+))?', lambda m: f"{m.group(1)}-{m.group(2)}" if m.group(2) else f"{m.group(1)}+")
    ]
    
    for pattern, formatter in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return formatter(match)
    return None


def fetch_product_details(url):
    """
    Combined function to fetch ISBN, age range, and other missing details
    """
    try:
        logger.info(f"Fetching details from: {url}")
        response = requests.get(url, headers=config['scraping']['headers'])
        time.sleep(config['scraping']['delay'])
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            details = {}
            
            # Debug HTML structure
            debug_html = soup.select('#detailBullets_feature_div')
            logger.debug(f"Found detail bullets section: {bool(debug_html)}")
            
            # Process detail bullets
            bullets = soup.select('#detailBullets_feature_div .a-list-item')
            logger.debug(f"Found {len(bullets)} detail bullet points")
            
            for bullet in bullets:
                text = bullet.text.strip()
                logger.debug(f"Processing bullet: {text[:50]}...")  # First 50 chars for readability
                
                # ISBN-13
                if 'ISBN-13' in text:
                    spans = bullet.select('span')
                    if len(spans) >= 2:
                        isbn13 = ''.join(filter(str.isdigit, spans[-1].text))
                        if len(isbn13) == 13:
                            details['isbn13'] = isbn13
                            logger.info(f"Found ISBN-13: {isbn13}")
                
                # ISBN-10
                elif 'ISBN-10' in text:
                    spans = bullet.select('span')
                    if len(spans) >= 2:
                        isbn10 = ''.join(c for c in spans[-1].text if c.isdigit() or c == 'X')
                        if len(isbn10) == 10:
                            details['isbn10'] = isbn10
                            logger.info(f"Found ISBN-10: {isbn10}")
                
                # Reading Age
                elif 'Reading age' in text or 'Age range' in text:
                    spans = bullet.select('span')
                    if len(spans) >= 2:
                        age_text = spans[-1].text.strip()
                        details['target_age_range'] = parse_age_range(age_text)
                        logger.info(f"Found age range: {details.get('target_age_range')}")
                
                # Page Count
                elif 'pages' in text.lower():
                    match = re.search(r'(\d+)\s*pages', text)
                    if match:
                        details['page_count'] = int(match.group(1))
                        logger.info(f"Found page count: {details['page_count']}")
            
            return details
            
    except Exception as e:
        logger.error(f"Error fetching product details: {str(e)}")
        return None

def update_missing_data(df, batch_size=10):
    """
    Update DataFrame with missing information
    """
    # Track progress
    total_processed = 0
    total_updated = 0
    
    for i in range(0, len(df), batch_size):
        batch = df[i:i+batch_size]
        logger.info(f"Processing batch {i//batch_size + 1} of {len(df)//batch_size + 1}")
        
        for idx, row in batch.iterrows():
            if pd.notna(row['product_url']):
                # Check if we need to fetch details
                needs_update = (
                    pd.isna(row['isbn13']) or 
                    pd.isna(row['isbn10']) or 
                    pd.isna(row['target_age_range']) or 
                    pd.isna(row['page_count'])
                )
                
                if needs_update:
                    details = fetch_product_details(row['product_url'])
                    if details:
                        for key, value in details.items():
                            if pd.isna(df.at[idx, key]):
                                df.at[idx, key] = value
                                total_updated += 1
                
                total_processed += 1
                
                # Log progress
                if total_processed % 10 == 0:
                    logger.info(f"Processed {total_processed}/{len(df)} books. Updated {total_updated} fields.")
        
        # Save progress after each batch
        df.to_csv('bestsellers_enriched.csv', index=False)
        logger.info(f"Saved progress after {total_processed} books")
        
        # Delay between batches
        time.sleep(5)
    
    return df

def update_remaining_data(df, batch_size=10):
    """
    Targeted update for remaining missing data
    """
    try:
        total_processed = 0
        
        for i in range(0, len(df), batch_size):
            batch = df[i:i+batch_size]
            logger.info(f"Processing batch {i//batch_size + 1} of {len(df)//batch_size + 1}")
            
            for idx, row in batch.iterrows():
                if pd.notna(row['product_url']):
                    needs_update = (
                        pd.isna(row['category_ranks']) or 
                        pd.isna(row['author']) or
                        pd.isna(row['target_age_range']) or
                        pd.isna(row['isbn13']) or
                        pd.isna(row['page_count'])
                    )
                    
                    if needs_update:
                        try:
                            response = requests.get(row['product_url'], headers=config['scraping']['headers'])
                            soup = BeautifulSoup(response.text, 'html.parser')
                            
                            # Category ranks from Best Sellers section
                            rank_section = soup.select_one('ul.zg_hrsr')
                            if rank_section and pd.isna(row['category_ranks']):
                                category_ranks = []
                                for rank_item in rank_section.select('li'):
                                    rank_text = rank_item.text.strip()
                                    if rank_text:
                                        category_ranks.append(rank_text)
                                df.at[idx, 'category_ranks'] = ' | '.join(category_ranks)
                            
                            # Author (if missing)
                            if pd.isna(row['author']):
                                author_elem = soup.select_one('span.author a')
                                if author_elem:
                                    df.at[idx, 'author'] = author_elem.text.strip()
                            
                            # Additional data collection for remaining missing fields
                            details = fetch_product_details(row['product_url'])
                            if details:
                                for key, value in details.items():
                                    if pd.isna(df.at[idx, key]):
                                        df.at[idx, key] = value
                            
                            logger.info(f"Updated book {idx}: {row['title'][:50]}...")
                            
                        except Exception as e:
                            logger.error(f"Error processing {row['title'][:50]}: {str(e)}")
                
                total_processed += 1
                if total_processed % 10 == 0:
                    logger.info(f"Processed {total_processed}/{len(df)} books")
                    df.to_csv('bestsellers_final.csv', index=False)
            
            time.sleep(config['scraping']['delay'])
    
    except Exception as e:
        logger.error(f"Error in update process: {str(e)}")
    finally:
        df.to_csv('bestsellers_final.csv', index=False)
        print_data_status(df)
    
    return df

# Run the update
df = update_missing_data(df)

# Another round of updating
df = update_remaining_data(df)


# Save to CSV
filename = f"../data/raw/daily_bestsellers/bestsellers_{datetime.now().strftime('%Y%m%d')}.csv"
df.to_csv(filename, index=False)