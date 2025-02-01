-- Indexes for dimension tables
CREATE INDEX idx_dim_pattern_publisher ON dim_pattern(publisher_key);
CREATE INDEX idx_dim_pattern_garment ON dim_pattern(garment_type_key);
CREATE INDEX idx_dim_garment_type_category ON dim_garment_type(category_key);
CREATE INDEX idx_dim_order_customer ON dim_order(customer_key);

-- Indexes for fact table
CREATE INDEX idx_fact_sales_order ON fact_sales(order_key);
CREATE INDEX idx_fact_sales_pattern ON fact_sales(pattern_key);

-- Composite indexes for commonly joined columns
CREATE INDEX idx_fact_sales_order_pattern ON fact_sales(order_key, pattern_key);