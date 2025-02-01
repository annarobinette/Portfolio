# Running Stitch: Sewing Pattern Database Project

## Pattern Scraper

## Overview
For the CodeFirstGirls SQL course, I needed to demonstrate my ability to build and maintain a database. As a sewist, I devised a fake company that sells sewing patterns from a variety of pattern companies and wanted to use current data as the core. A well known sewing website is The FoldLine, selling patterns in the same way. To create the database, I built a Python-based web scraper designed to ethically collect sewing pattern data from The Foldine and then generate believable but fake customers, orders and reviews around those patterns. This readme shows the four main Python scripts that work together to create a comprehensive sewing pattern database. Each script handles a specific part of the data pipeline, from web scraping to data cleaning and synthetic data generation.

## Features
- Ethical web scraping with appropriate delays and user agents
- Comprehensive pattern data collection
- Data cleaning and standardization
- CSV export for database import
[dummy](./data/processed/combined_patterns.csv)

## Data Location
- The raw data from the scraper is [here](./data/raw/) and separated into categories (women, men, kids).
- The cleaned data is [here](./data/processed/).
- The combined data is [here](./data/processed/combined_patterns.csv).
- The generated data is [here](./data/generated/).

## 1. Pattern Scraper ([pattern_scraper.py](pattern_scraper.py))

### Purpose
Scrapes sewing pattern data from an online marketplace (TheFoldLine.com) to collect pattern information.

### Key Components

#### PatternScraper Class
```python
class PatternScraper:
    def __init__(self):
        self.base_url = "https://thefoldline.com"
        self.headers = {...}
```

- **Initialization**: Sets up the base URL and headers for web requests
- **Web Scraping Best Practices**: Implements delays and user-agent headers to be respectful of the website

#### Core Methods

1. `_get_page(url)`:
   - Handles HTTP requests with proper error handling
   - Implements random delays (2-4 seconds) to prevent server overload
   - Returns the HTML content of the page

2. `_clean_description(text)`:
   - Parses raw text into structured data
   - Extracts key information like fabric requirements, sizing, and notions
   - Uses regex for consistent pattern matching

3. `get_patterns(num_products)`:
   - Main scraping method
   - Iterates through product pages
   - Extracts both basic and detailed pattern information
   - Creates a pandas DataFrame with standardized data

## 2. Data Cleaner (data_cleaner.py)

### Purpose
Standardizes and cleans the raw scraped data to ensure consistency.

### Key Functions

1. `clean_pattern_name(row)`:
   - Removes company names from pattern titles
   - Strips unnecessary text like "(free)"
   - Ensures consistent formatting

2. `clean_company_name(name)`:
   - Standardizes company names
   - Converts '&' to 'and'
   - Applies proper title case formatting

3. `clean_price(price)`:
   - Extracts numerical price values
   - Handles various price formats (e.g., "From $X")
   - Converts strings to float values

## 3. Data Concatenator (data_concat.py)

### Purpose
Combines multiple CSV files containing different pattern types into a single dataset.

### Key Features

- Uses glob pattern matching to find relevant CSV files
- Extracts pattern type from filenames using regex
- Adds type column to differentiate pattern categories
- Concatenates DataFrames while maintaining data integrity

## 4. Data Generator (data_generator.py)

### Purpose
Creates synthetic data for the database, including customers, orders, and ratings.

### Key Classes and Methods

#### PatternDataGenerator Class

1. Pattern and Publisher Generation:
```python
def generate_pattern_ids(self):
    """Add unique 6-digit pattern IDs"""
    pattern_ids = range(100000, 100000 + len(self.patterns_df))
    self.patterns_df['pattern_id'] = pattern_ids
    return self.patterns_df
```

2. Customer Generation:
```python
def generate_customers(self, num_customers=1000):
    """Generate customer data with realistic join dates"""
    # Implements weighted date selection for COVID-19 period
    # Creates realistic customer profiles
```

3. Order Generation:
```python
def generate_orders(self, customers_df, num_orders=5000):
    """Generate order data with COVID pattern and realistic customer behavior"""
    # Creates customer segments
    # Implements realistic ordering patterns
    # Handles COVID-19 impact on ordering behavior
```

### Unique Features

1. **COVID-19 Impact Modeling**:
I know that home-based hobbies such as knnitting and sewing increased over the Covid-19 lockdowns, so I asked the script to increase the numbers of orders over those time periods.
   - Increased weights during lockdown periods
   - Realistic customer behaviour changes
   - Different patterns for different time periods

2. **Customer Segmentation**:
   - Frequent buyers (10%)
   - Regular buyers (20%)
   - Occasional buyers (40%)
   - One-time buyers (30%)

3. **Realistic Data Patterns**:
   - Order frequency varies by customer segment
   - Rating distribution follows realistic patterns
   - Time-based patterns in customer behavior

## Data Pipeline Flow

1. **Data Collection**: pattern_scraper.py scrapes raw data
2. **Data Cleaning**: data_cleaner.py standardizes the data
3. **Data Consolidation**: data_concat.py combines multiple sources
4. **Synthetic Data Generation**: data_generator.py creates additional realistic data

## Technical Implementation Details

### Error Handling
- Good error catching in web scraping
- Validation of data types and formats
- Good handling of missing or malformed data

### Performance Considerations
- Efficient DataFrame operations
- Proper use of pandas methods
- Memory management for large datasets

### Scalability
- Modular design for easy expansion
- Configurable parameters
- Reusable components

## Best Practices Demonstrated

1. **Code Organization**:
   - Clear class and function structure
   - Proper separation of concerns
   - Well-documented methods

2. **Data Processing**:
   - Consistent data cleaning approaches
   - Standardized formatting
   - Proper type handling

3. **Web Scraping Ethics**:
   - Respectful delays between requests
   - Proper user agent identification
   - Error handling and retry logic

This project demonstrates professional-level Python programming with a focus on data engineering and analysis. It showcases skills in web scraping, data cleaning, synthetic data generation, and database design.

---
Created as part of my 'Running Stitch' project for the CodeFirstGirls SQL course.