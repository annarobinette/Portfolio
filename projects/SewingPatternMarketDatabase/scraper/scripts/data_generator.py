import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import uuid

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)
fake = Faker()
Faker.seed(42)

class PatternDataGenerator:
    def __init__(self, pattern_data_path):
        self.patterns_df = pd.read_csv(pattern_data_path)
        self.start_date = datetime(2018, 1, 1)
        self.end_date = datetime(2025, 1, 21)  # Current date
        
    def generate_pattern_ids(self):
        """Add unique 6-digit pattern IDs"""
        # Start from 100000 to ensure 6 digits
        pattern_ids = range(100000, 100000 + len(self.patterns_df))
        self.patterns_df['pattern_id'] = pattern_ids
        return self.patterns_df
    
    def generate_publishers(self):
        """Generate publisher data"""
        unique_publishers = self.patterns_df['pattern_company'].unique()
        publishers = []
        
        for idx, name in enumerate(unique_publishers, start=1):
            website = f"www.{name.lower().replace(' ', '')}.fake.com"
            publishers.append({
                'publisher_id': idx,
                'publisher_name': name,
                'website': website,
                'commission_rate': round(random.uniform(0.10, 0.25), 2),  # 10-25% commission
                'country_of_origin': random.choice(['UK', 'US', 'France', 'Australia', 'Germany'])
            })
        
        # Add publisher_id to patterns
        publisher_map = {p['publisher_name']: p['publisher_id'] for p in publishers}
        self.patterns_df['publisher_id'] = self.patterns_df['pattern_company'].map(publisher_map)
        
        return pd.DataFrame(publishers)
    
    def generate_garment_types(self):
        """Generate garment type data"""
        garment_types = [
            # Tops
            {'type_name': 'Blouse', 'category': "women", 'typical_fabric_type': 'Woven, Light to Medium', 'garment_family': 'tops'},
            {'type_name': 'Button-up Shirt', 'category': "unisex", 'typical_fabric_type': 'Woven, Light', 'garment_family': 'tops'},
            {'type_name': 'T-Shirt', 'category': 'unisex', 'typical_fabric_type': 'Knit, Light', 'garment_family': 'tops'},
            {'type_name': 'Tank Top', 'category': 'unisex', 'typical_fabric_type': 'Knit or Woven, Light', 'garment_family': 'tops'},
            {'type_name': 'Crop Top', 'category': 'unisex', 'typical_fabric_type': 'Knit or Woven, Light', 'garment_family': 'tops'},
            
            # Dresses
            {'type_name': 'Dress', 'category': "women", 'typical_fabric_type': 'Woven or Knit, Light to Medium', 'garment_family': 'dresses'},
            {'type_name': 'Maxi Dress', 'category': "women", 'typical_fabric_type': 'Woven or Knit, Light to Medium', 'garment_family': 'dresses'},
            {'type_name': 'Wrap Dress', 'category': "women", 'typical_fabric_type': 'Woven or Knit, Light to Medium', 'garment_family': 'dresses'},
            {'type_name': 'Slip Dress', 'category': "women", 'typical_fabric_type': 'Woven, Light', 'garment_family': 'dresses'},
            
            # Bottoms
            {'type_name': 'Skirt', 'category': "women", 'typical_fabric_type': 'Woven, Light to Medium', 'garment_family': 'bottoms'},
            {'type_name': 'Pants', 'category': 'unisex', 'typical_fabric_type': 'Woven, Medium to Heavy', 'garment_family': 'bottoms'},
            {'type_name': 'Shorts', 'category': 'unisex', 'typical_fabric_type': 'Woven, Light to Medium', 'garment_family': 'bottoms'},
            {'type_name': 'Culottes', 'category': 'women', 'typical_fabric_type': 'Woven, Light to Medium', 'garment_family': 'bottoms'},
            {'type_name': 'Leggings', 'category': 'unisex', 'typical_fabric_type': 'Knit, Medium with Stretch', 'garment_family': 'bottoms'},
            
            # Outerwear
            {'type_name': 'Jacket', 'category': 'unisex', 'typical_fabric_type': 'Woven, Medium to Heavy', 'garment_family': 'outerwear'},
            {'type_name': 'Coat', 'category': 'unisex', 'typical_fabric_type': 'Woven, Heavy', 'garment_family': 'outerwear'},
            {'type_name': 'Cardigan', 'category': 'unisex', 'typical_fabric_type': 'Knit, Light to Medium', 'garment_family': 'outerwear'},
            {'type_name': 'Blazer', 'category': 'unisex', 'typical_fabric_type': 'Woven, Medium', 'garment_family': 'outerwear'},
            
            # Loungewear
            {'type_name': 'Robe', 'category': 'unisex', 'typical_fabric_type': 'Woven, Light to Medium', 'garment_family': 'loungewear'},
            {'type_name': 'Pajamas', 'category': 'unisex', 'typical_fabric_type': 'Woven or Knit, Light', 'garment_family': 'loungewear'},
            {'type_name': 'Lounge Pants', 'category': 'unisex', 'typical_fabric_type': 'Knit, Light to Medium', 'garment_family': 'loungewear'},
            
            # Active/Swimwear
            {'type_name': 'Swimsuit', 'category': 'unisex', 'typical_fabric_type': 'Knit with Stretch', 'garment_family': 'activewear'},
            {'type_name': 'Sports Bra', 'category': 'women', 'typical_fabric_type': 'Knit with Stretch', 'garment_family': 'activewear'},
            {'type_name': 'Active Leggings', 'category': 'unisex', 'typical_fabric_type': 'Knit with Stretch', 'garment_family': 'activewear'},
            
            # Children's Wear
            {'type_name': "Child's Dress", 'category': "children", 'typical_fabric_type': 'Woven, Light', 'garment_family': 'children'},
            {'type_name': "Child's Top", 'category': "children", 'typical_fabric_type': 'Knit, Light', 'garment_family': 'children'},
            {'type_name': "Child's Pants", 'category': "children", 'typical_fabric_type': 'Woven or Knit, Light to Medium', 'garment_family': 'children'},
            {'type_name': "Child's Coat", 'category': "children", 'typical_fabric_type': 'Woven, Medium', 'garment_family': 'children'},
            
            # Accessories
            {'type_name': 'Bag', 'category': 'accessories', 'typical_fabric_type': 'Woven, Heavy', 'garment_family': 'accessories'},
            {'type_name': 'Hat', 'category': 'accessories', 'typical_fabric_type': 'Woven, Light to Medium', 'garment_family': 'accessories'},
            {'type_name': 'Scarf', 'category': 'accessories', 'typical_fabric_type': 'Woven or Knit, Light', 'garment_family': 'accessories'},
            {'type_name': 'Face Mask', 'category': 'accessories', 'typical_fabric_type': 'Woven, Light', 'garment_family': 'accessories'},
            
            # Underwear/Lingerie
            {'type_name': 'Bra', 'category': 'women', 'typical_fabric_type': 'Knit with Stretch', 'garment_family': 'underwear'},
            {'type_name': 'Underwear', 'category': 'unisex', 'typical_fabric_type': 'Knit with Stretch', 'garment_family': 'underwear'},
            {'type_name': 'Camisole', 'category': 'women', 'typical_fabric_type': 'Woven or Knit, Light', 'garment_family': 'underwear'},
            
            # One-piece garments
            {'type_name': 'Jumpsuit', 'category': 'unisex', 'typical_fabric_type': 'Woven, Light to Medium', 'garment_family': 'one-piece'},
            {'type_name': 'Overalls', 'category': 'unisex', 'typical_fabric_type': 'Woven, Medium to Heavy', 'garment_family': 'one-piece'},
            {'type_name': 'Dungarees', 'category': 'unisex', 'typical_fabric_type': 'Woven, Medium', 'garment_family': 'one-piece'}
        ]
        
        # Add IDs
        for idx, item in enumerate(garment_types, start=1):
            item['garment_type_id'] = idx
        
        # Assign random garment types to patterns
        self.patterns_df['garment_type_id'] = np.random.randint(1, len(garment_types) + 1, size=len(self.patterns_df))
        
        return pd.DataFrame(garment_types)
    
    def generate_customers(self, num_customers=1000):
        """Generate customer data with realistic join dates"""
        customers = []
        
        # Calculate weights for join dates (higher during COVID lockdowns)
        date_range = pd.date_range(self.start_date, self.end_date, freq='D')
        weights = []
        for date in date_range:
            weight = 1.0
            # Increase weights during COVID lockdowns
            if datetime(2020, 3, 1) <= date <= datetime(2020, 8, 1):
                weight = 3.0
            elif datetime(2020, 8, 2) <= date <= datetime(2021, 6, 1):
                weight = 2.0
            weights.append(weight)
        
        for _ in range(num_customers):
            join_date = pd.Timestamp(np.random.choice(date_range, p=np.array(weights)/sum(weights)))
            
            customers.append({
                'customer_id': _ + 1,
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'email': fake.email(),
                'date_joined': join_date.strftime('%Y-%m-%d'),
                'age_years': random.randint(18, 75),
                'country': fake.country()
            })
        
        return pd.DataFrame(customers)
    
    def generate_orders(self, customers_df, num_orders=5000):
        """Generate order data with COVID pattern and realistic customer behavior"""
        orders = []
        order_details = []
        order_id = 1
        
        # Calculate weights for order dates
        date_range = pd.date_range(self.start_date, self.end_date, freq='D')
        weights = []
        for date in date_range:
            weight = 1.0
            # Increase weights during COVID lockdowns
            if datetime(2020, 3, 1) <= date <= datetime(2020, 8, 1):
                weight = 4.0
            elif datetime(2020, 8, 2) <= date <= datetime(2021, 6, 1):
                weight = 3.0
            weights.append(weight)
        
        # Assign customer segments
        customers_df['segment'] = np.random.choice(
            ['frequent', 'regular', 'occasional', 'one_time'],
            size=len(customers_df),
            p=[0.1, 0.2, 0.4, 0.3]  # 10% frequent, 20% regular, 40% occasional, 30% one-time
        )
        
        # Define order frequency by segment
        segment_orders = {
            'frequent': (8, 20),    # 8-20 orders over the period
            'regular': (4, 7),      # 4-7 orders
            'occasional': (2, 3),   # 2-3 orders
            'one_time': (1, 1)      # exactly 1 order
        }
        
        pattern_ids = self.patterns_df['pattern_id'].tolist()
        
        # Generate orders for each customer
        for _, customer in customers_df.iterrows():
            join_date = pd.to_datetime(customer['date_joined'])
            # Calculate potential order dates (can't order before joining)
            valid_dates = date_range[date_range >= join_date]
            if len(valid_dates) == 0:
                continue
                
            # Get weights for valid dates
            valid_weights = weights[len(weights)-len(valid_dates):]
            
            # Determine number of orders based on segment
            min_orders, max_orders = segment_orders[customer['segment']]
            num_customer_orders = random.randint(min_orders, max_orders)
            
            # Generate orders for this customer
            for _ in range(num_customer_orders):
                # Pick a date after join date, weighted for COVID
                order_date = np.random.choice(valid_dates, p=np.array(valid_weights)/sum(valid_weights))
                order_date = pd.to_datetime(order_date)
                
                # Generate between 1 and 20 items per order (weighted towards smaller orders)
                probs = [0.3, 0.3, 0.2, 0.1]  # Probabilities for 1-4 items (90% of orders)
                probs.extend([0.01] * 16)      # Small probability for 5-20 items (10% total)
                probs = [p/sum(probs) for p in probs]  # Normalize to sum to 1
                num_items = np.random.choice(range(1, 21), p=probs)
                
                # Create order
                orders.append({
                    'order_id': order_id,
                    'customer_id': customer['customer_id'],
                    'order_date': order_date.strftime('%Y-%m-%d'),
                    'total_amount': 0  # Will be updated after details
                })
                
                # Create order details
                order_total = 0
                selected_patterns = random.sample(pattern_ids, num_items)
                for pattern_id in selected_patterns:
                    pattern_price = float(self.patterns_df[self.patterns_df['pattern_id'] == pattern_id]['price'].iloc[0])
                    order_details.append({
                        'order_id': order_id,
                        'pattern_id': pattern_id,
                        'price_paid': pattern_price,
                        'download_status': random.choice(['completed', 'completed', 'completed', 'expired'])
                    })
                    order_total += pattern_price
                
                # Update order total
                orders[-1]['total_amount'] = order_total
                order_id += 1
        
        return pd.DataFrame(orders), pd.DataFrame(order_details)
    
    def generate_ratings(self, customers_df, order_details_df, min_date=datetime(2018, 1, 1)):
        """Generate ratings data"""
        ratings = []
        rating_id = 1
        
        # Generate ratings for about 20% of pattern purchases
        for _, row in order_details_df.iterrows():
            if random.random() < 0.2:  # 20% chance of rating
                ratings.append({
                    'rating_id': rating_id,
                    'pattern_id': row['pattern_id'],
                    'customer_id': random.choice(customers_df['customer_id'].tolist()),
                    'rating': random.choices([5,4,3,2,1], weights=[0.4,0.3,0.2,0.07,0.03])[0],
                    'review_text': fake.paragraph(),
                    'date_posted': fake.date_between(start_date=min_date, end_date=datetime.now()).strftime('%Y-%m-%d')
                })
                rating_id += 1
        
        return pd.DataFrame(ratings)

def main():
    # Initialize generator
    generator = PatternDataGenerator('./data/processed/combined_patterns.csv')
    
    # Generate all data
    patterns_df = generator.generate_pattern_ids()
    publishers_df = generator.generate_publishers()
    garment_types_df = generator.generate_garment_types()
    customers_df = generator.generate_customers()
    orders_df, order_details_df = generator.generate_orders(customers_df)
    ratings_df = generator.generate_ratings(customers_df, order_details_df)
    
    # Make sure output directory exists
    import os
    output_path = './data/generated/'
    os.makedirs(output_path, exist_ok=True)
    
    # Save all data
    patterns_df.to_csv(f'{output_path}patterns_final.csv', index=False)
    publishers_df.to_csv(f'{output_path}publishers.csv', index=False)
    garment_types_df.to_csv(f'{output_path}garment_types.csv', index=False)
    customers_df.to_csv(f'{output_path}customers.csv', index=False)
    orders_df.to_csv(f'{output_path}orders.csv', index=False)
    order_details_df.to_csv(f'{output_path}order_details.csv', index=False)
    ratings_df.to_csv(f'{output_path}ratings.csv', index=False)
    
    # Print summary statistics
    print("Data Generation Summary:")
    print(f"Patterns: {len(patterns_df)}")
    print(f"Publishers: {len(publishers_df)}")
    print(f"Garment Types: {len(garment_types_df)}")
    print(f"Customers: {len(customers_df)}")
    print(f"Orders: {len(orders_df)}")
    print(f"Order Details: {len(order_details_df)}")
    print(f"Ratings: {len(ratings_df)}")

if __name__ == "__main__":
    main()