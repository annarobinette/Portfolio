# Amazon Bestseller Analysis Project

## Project Structure
```
amazon_bestseller_analysis/
├── README.md                   # Project documentation
├── requirements.txt            # Project dependencies
├── config/
│   └── config.yaml            # Configuration settings
├── data/
│   ├── raw/                   # Raw scraped data
│   │   ├── daily_bestsellers/
│   │   └── historical/
│   └── processed/             # Cleaned and transformed data
│       ├── price_data.csv
│       ├── genre_data.csv
│       ├── format_data.csv
│       └── seasonal_data.csv
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_price_analysis.ipynb
│   ├── 04_genre_analysis.ipynb
│   ├── 05_format_analysis.ipynb
│   └── 06_seasonal_analysis.ipynb
├── src/
│   ├── collect_bestsellers.py
│   ├── __init__.py
│   ├── scraper/
│   │   ├── __init__.py
│   │   ├── scraper.py
│   │   └── utils.py
│   ├── processing/
│   │   ├── __init__.py
│   │   └── cleaner.py
│   └── analysis/
│       ├── __init__.py
│       └── analytics.py
├── power_bi/
│   ├── price_dashboard.pbix
│   ├── genre_dashboard.pbix
│   └── seasonal_dashboard.pbix
└── reports/
    └── findings/

## Project Overview

![Amazon Bestseller page](../visualisations/Screenshots/Amazon_bestseller.png)


## Notebook Details

### 01_data_collection.ipynb
Could be more widespread on all the details

### 02_data_cleaning.ipynb


### 03_price_analysis.ipynb


## Power BI Integration

### Price Analysis Dashboard
- Data Source: '../data/processed/price_segments.csv'
- Visualizations:
  1. Price Distribution by Format
  2. Price Segments by Category
  3. Price Trends Over Time
  4. Price vs. Rating Correlation

### Genre Analysis Dashboard
- Data Source: '../data/processed/genre_data.csv'
- Visualizations:
  1. Genre Popularity Trends
  2. Cross-Genre Analysis
  3. Genre Price Points
  4. Genre Rating Distribution

### Seasonal Analysis Dashboard
- Data Source: '../data/processed/seasonal_data.csv'
- Visualizations:
  1. Monthly Sales Patterns
  2. Genre Seasonality
  3. Price Fluctuations
  4. Holiday Impact Analysis

## Configuration (config.yaml)
```yaml
scraping:
  delay: 3  # Seconds between requests
  headers:
    User-Agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
    Accept-Language: "en-GB,en;q=0.9"
  max_retries: 3
  backoff_factor: 2

categories:
  - name: "Classic Books"
    url: "https://www.amazon.co.uk/gp/bestsellers/books/291745/ref=pd_zg_hrsr_books"
    type: "fiction"
    subtype: "classics"
    
  - name: "Sport and Outdoors"
    url: "https://www.amazon.co.uk/Best-Sellers-Books-Childrens-Books-on-Sports-the-Outdoors/zgbs/books/291772/ref=zg_bs_nav_books_2_69"
    type: "non_fiction"
    subtype: "sports"
    
  - name: "Teen and Young Adult"
    url: "https://www.amazon.co.uk/Best-Sellers-Teen-Young-Adult/zgbs/books/52"
    type: "fiction"
    subtype: "young_adult"
    default_age_range: "14-18"
    
  - name: "Comics and Graphic Novels"
    url: "https://www.amazon.co.uk/Best-Sellers-Books-Comics-Graphic-Novels-for-Children/zgbs/books/291767/ref=zg_bs_nav_books_2_69"
    type: "fiction"
    subtype: "graphic_novels"
    
  - name: "Science, Nature & How It Works"
    url: "https://www.amazon.co.uk/Best-Sellers-Books-Childrens-Books-on-Science-Nature-How-It-Works/zgbs/books/492622/ref=zg_bs_nav_books_2_69"
    type: "non_fiction"
    subtype: "science"
    
  - name: "TV, Movie & Video Game Adaptations"
    url: "https://www.amazon.co.uk/Best-Sellers-Books-TV-Movie-Video-Game-Adaptations-for-Children/zgbs/books/15512249031/ref=zg_bs_nav_books_3_15512039031"
    type: "fiction"
    subtype: "adaptations"
    
  - name: "Educational Books"
    url: "https://www.amazon.co.uk/Best-Sellers-Books-Education-Reference-for-Children/zgbs/books/291673/ref=zg_bs_nav_books_2_69"
    type: "education"
    subtype: "general"
    
  - name: "Reference Books"
    url: "https://www.amazon.co.uk/Best-Sellers-Books-Childrens-Reference-Books/zgbs/books/291707/ref=zg_bs_nav_books_3_291673"
    type: "education"
    subtype: "reference"

output:
  base_path: "../data"
  raw_data: "raw/daily_bestsellers"
  processed_data: "processed"
  file_prefix: "bestsellers"
```

### Dependencies (requirements.txt)
```
pandas==2.1.0
beautifulsoup4==4.12.2
requests==2.31.0
pyyaml==6.0.1
seaborn==0.12.2
matplotlib==3.7.2
numpy==1.24.3
tqdm==4.65.0
```

### Data Collection Schedule
1. Daily bestseller scraping (automated)
2. Weekly price trend analysis
3. Monthly seasonal pattern analysis
4. Quarterly comprehensive report generation

### Ethical Considerations
- Respect robots.txt directives
- Implement appropriate request delays
- No excessive scraping
- Data used for analysis only
- No personal data collection

## Future Plans
This project looks at a select number of categories to show proof of concept. In the future, I think that building a complete category mapping would be valuable because it would demonstrate how different publishers position their books, identify underserved categories/opportunities and could help with competitive analysis. At the moment, this project provides a reusable framework for future analysis

For a full look at the Amazon bestsellers lists, I would start the process by scraping the category tree that would be used to create the config file. Here is a demonstration of what the code would look like:

```python
extract_amazon_category_tree(url="https://www.amazon.co.uk/Best-Sellers-Books-Childrens/zgbs/books/69"):
    """
    Extract Amazon's complete children's book category hierarchy
    """
    try:
        categories = []
        response = requests.get(url, headers=config['scraping']['headers'])
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the category navigation tree
        category_tree = soup.select('div._p13n-zg-nav-tree-all_style_zg-browse-group__88fbz')
        
        for category in category_tree:
            cat_info = {
                'name': category.select_one('div._p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf').text.strip(),
                'url': category.select_one('a')['href'],
                'subcategories': []
            }
            
            # Get subcategories
            subcats = category.select('div._p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf')
            for subcat in subcats[1:]:  # Skip first as it's the parent
                cat_info['subcategories'].append({
                    'name': subcat.text.strip(),
                    'url': subcat.parent.get('href', '')
                })
            
            categories.append(cat_info)
        
        return categories
            
    except Exception as e:
        logger.error(f"Error extracting category tree: {str(e)}")
        return None
```
