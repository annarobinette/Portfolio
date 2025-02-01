import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from tqdm import tqdm
import re

class PatternScraper:
    def __init__(self):
        self.base_url = "https://thefoldline.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def _get_page(self, url):
        """Fetch a page with proper delays and error handling"""
        try:
            time.sleep(random.uniform(2, 4))
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def _clean_description(self, text):
        """Clean and extract relevant parts of the description"""
        if not text:
            return {}
        
        # Find the initial description (everything before "This sewing pattern")
        initial_desc = ""
        if "This sewing pattern" in text:
            initial_desc = text.split("This sewing pattern")[0].strip()
        else:
            initial_desc = text.split("Suggested fabrics")[0].strip()

        # Create a dictionary to store all extracted parts
        parts = {
            'description': initial_desc,
            'suggested_fabrics': '',
            'fabric_requirements': '',
            'sizing': '',
            'notions': '',
            'pattern_includes': ''
        }
        
        # Helper function to extract content between markers
        def extract_between(text, start_marker, end_markers):
            if start_marker not in text:
                return ''
            start_idx = text.find(start_marker) + len(start_marker)
            end_idx = len(text)
            for end_marker in end_markers:
                if end_marker in text[start_idx:]:
                    temp_idx = text.find(end_marker, start_idx)
                    if temp_idx < end_idx and temp_idx != -1:
                        end_idx = temp_idx
            return text[start_idx:end_idx].strip()

        # Extract each section
        parts['suggested_fabrics'] = extract_between(text, 
            'Suggested fabrics:', 
            ['Fabric requirements:', 'Sizing:'])
        
        parts['fabric_requirements'] = extract_between(text, 
            'Fabric requirements:', 
            ['Sizing:', 'Notions:'])
        
        parts['sizing'] = extract_between(text, 
            'Sizing:', 
            ['Notions:', 'PDF pattern includes:'])
        if parts['sizing']:
            # Extract just the size range
            size_match = re.search(r'(XXS|XS|S|M|L|XL|XXL).+?(XXS|XS|S|M|L|XL|XXL)', parts['sizing'])
            if size_match:
                parts['sizing'] = size_match.group(0)
        
        parts['notions'] = extract_between(text, 
            'Notions:', 
            ['PDF pattern includes:', 'If you'])
        
        parts['pattern_includes'] = extract_between(text, 
            'PDF pattern includes:', 
            ['If you', '\n\n'])

        return parts

    def get_patterns(self, num_products=50):
        """Get patterns with all details"""
        patterns = []
        page = 1
        
        while len(patterns) < num_products:
            url = f"{self.base_url}/collections/childrens-sewing-patterns?sort_by=best-selling?page={page}"
            
            html = self._get_page(url)
            
            if not html:
                break
                
            soup = BeautifulSoup(html, 'html.parser')
            product_cards = soup.find_all('loess-product-card', {'class': 'card'})
            
            if not product_cards:
                break
                
            for card in product_cards:
                if len(patterns) >= num_products:
                    break
                    
                try:
                    # Get basic info from listing
                    company_element = card.find('span', {'class': 'small-text'})
                    title_element = card.find('a', {'class': 'card__title'})
                    price_element = card.find('span', {'class': 'price-item--regular'})
                    image_element = card.find('img', {'class': 'card__primary-image'})
                    
                    if title_element and company_element:
                        # Get product URL
                        product_url = self.base_url + title_element['href'] if title_element['href'].startswith('/') else title_element['href']
                        
                        # Get detailed info
                        details_html = self._get_page(product_url)
                        if details_html:
                            details_soup = BeautifulSoup(details_html, 'html.parser')
                            description = details_soup.find('div', {'class': 'rte small-body-text'})
                            
                            if description:
                                cleaned_parts = self._clean_description(description.text.strip())
                                
                                pattern = {
                                    'pattern_company': company_element.text.strip(),
                                    'pattern_name': title_element.text.strip(),
                                    'price': price_element.text.strip() if price_element else 'N/A',
                                    'url': product_url,
                                    'image_url': image_element['src'] if image_element else None,
                                    'description': cleaned_parts['description'],
                                    'suggested_fabrics': cleaned_parts['suggested_fabrics'],
                                    'fabric_requirements': cleaned_parts['fabric_requirements'],
                                    'sizing': cleaned_parts['sizing'],
                                    'notions': cleaned_parts['notions'],
                                    'pattern_includes': cleaned_parts['pattern_includes']
                                }
                                patterns.append(pattern)
                                print(f"Found: {pattern['pattern_name']} by {pattern['pattern_company']}")
                        
                except Exception as e:
                    print(f"Error parsing product card: {e}")
                    continue
            
            page += 1
            
        return pd.DataFrame(patterns)

if __name__ == "__main__":
    scraper = PatternScraper()
    
    # Get patterns with details
    print("Scraping patterns...")
    patterns_df = scraper.get_patterns(num_products=50)
    patterns_df.to_csv('sewing_patterns_kids.csv', index=False)
    print(f"Found {len(patterns_df)} patterns")
    print("Done!")