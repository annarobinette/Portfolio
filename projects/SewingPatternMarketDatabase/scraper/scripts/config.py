from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables

load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Data directories
DATA_DIR = BASE_DIR / 'data'
RAW_DATA_DIR = DATA_DIR / 'raw'
PROCESSED_DATA_DIR = DATA_DIR / 'processed'

# Create directories if they don't exist
for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Scraping configuration
SCRAPING_CONFIG = {
    'base_url': 'https://thefoldline.com',
    'delay_range': (2, 4),  # Random delay between requests in seconds
    'max_retries': 3,  # Number of times to retry failed requests
    'timeout': 30,  # Request timeout in seconds
    'batch_size': 10,  # Number of products to process in each batch
}

# Default headers
DEFAULT_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
}

# Output configuration
OUTPUT_CONFIG = {
    'listings_filename': 'pattern_listings.csv',
    'details_filename': 'pattern_details.csv',
    'image_dir': RAW_DATA_DIR / 'images',
    'save_images': False,  # Set to True if you want to download images
}

# Logging configuration
LOGGING_CONFIG = {
    'filename': BASE_DIR / 'scraper.log',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'level': 'INFO',
}

# Fields to extract from pattern listings
LISTING_FIELDS = [
    'pattern_company',
    'pattern_name',
    'url',
    'price',
    'image_url',
]

# Fields to extract from pattern details
DETAIL_FIELDS = [
    'title',
    'company',
    'price',
    'description',
    'suggested_fabrics',
    'fabric_requirements',
    'sizing',
    'notions',
]
