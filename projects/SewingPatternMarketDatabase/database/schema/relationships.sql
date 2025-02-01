-- Create indexes
CREATE INDEX idx_patterns_publisher ON patterns(publisher_id);
CREATE INDEX idx_patterns_garment_type ON patterns(garment_type_id);
CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_order_details_pattern ON order_details(pattern_id);
CREATE INDEX idx_ratings_pattern ON ratings(pattern_id);
CREATE INDEX idx_ratings_customer ON ratings(customer_id);