import time
import requests
from bs4 import BeautifulSoup
import yaml
import logging

logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

config = {
    'scraping': {
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-GB,en;q=0.9'
        },
        'delay': 2
    }
}

def extract_amazon_category_tree(url="https://www.amazon.co.uk/Best-Sellers-Books-Childrens-Books/zgbs/books/69/ref=zg_bs_nav_books_1", visited_urls=None):
    if visited_urls is None:
        visited_urls = set()
    
    if url in visited_urls:
        return None
        
    visited_urls.add(url)
    time.sleep(config['scraping']['delay'])
    logger.info(f"Processing URL: {url}")
    
    try:
        categories = []
        response = requests.get(url, headers=config['scraping']['headers'])
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for category links in the browse tree
        browse_tree = soup.select_one('#zg-browse-root')
        if browse_tree:
            for link in browse_tree.select('a'):
                cat_info = {
                    'name': link.text.strip(),
                    'url': link['href'] if link['href'].startswith('http') else f"https://www.amazon.co.uk{link['href']}",
                    'subcategories': []
                }
                
                # Only process if it's a children's book category
                if '/childrens' in cat_info['url'].lower() or '/books/69' in cat_info['url'].lower():
                    sub_cats = extract_amazon_category_tree(cat_info['url'], visited_urls)
                    if sub_cats:
                        cat_info['subcategories'] = sub_cats
                    categories.append(cat_info)
        
        return categories
            
    except Exception as e:
        logger.error(f"Error extracting from {url}: {str(e)}")
        return None

def generate_config_yaml(categories, indent=0):
    yaml_content = []
    
    for category in categories:
        yaml_content.append('  ' * indent + f"- name: \"{category['name']}\"")
        yaml_content.append('  ' * indent + f"  url: \"{category['url']}\"")
        yaml_content.append('  ' * indent + f"  type: \"childrens_books\"")
        
        if category['subcategories']:
            yaml_content.append('  ' * indent + "  subcategories:")
            yaml_content.extend(generate_config_yaml(category['subcategories'], indent + 2))
            
    return yaml_content

if __name__ == "__main__":
    categories = extract_amazon_category_tree()
    if categories:
        yaml_content = ["categories:"] + generate_config_yaml(categories)
        
        with open('childrens_categories_config.yaml', 'w') as f:
            f.write('\n'.join(yaml_content))
        logger.info("Category tree extraction complete")