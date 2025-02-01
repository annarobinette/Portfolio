-- Populate dimension tables from existing data
INSERT INTO dim_garment_category (
    category_key,
    garment_family,
    category_name,
    typical_fabric_type
)
SELECT 
    category_id,
    garment_family,
    category_name,
    typical_fabric_type
FROM garment_categories;

INSERT INTO dim_garment_type (
    garment_type_key,
    category_key,
    type_name
)
SELECT 
    garment_type_id,
    category_id,
    type_name
FROM garment_types;

INSERT INTO dim_publisher (
    publisher_key,
    publisher_name,
    website,
    commission_rate,
    country_of_origin
)
SELECT 
    publisher_id,
    publisher_name,
    website,
    commission_rate,
    country_of_origin
FROM publishers;

INSERT INTO dim_pattern (
    pattern_key,
    publisher_key,
    garment_type_key,
    pattern_name,
    price,
    description,
    suggested_fabrics,
    fabric_requirements,
    sizing,
    notions,
    pattern_includes
)
SELECT 
    pattern_id,
    publisher_id,
    garment_type_id,
    pattern_name,
    price,
    description,
    suggested_fabrics,
    fabric_requirements,
    sizing,
    notions,
    pattern_includes
FROM patterns;

INSERT INTO dim_customer (
    customer_key,
    first_name,
    last_name,
    email,
    date_joined,
    age_years,
    country
)
SELECT 
    customer_id,
    first_name,
    last_name,
    email,
    date_joined,
    age_years,
    country
FROM customers;

INSERT INTO dim_order (
    order_key,
    customer_key,
    order_date,
    total_amount
)
SELECT 
    order_id,
    customer_id,
    order_date,
    total_amount
FROM orders;

-- Finally, populate fact table
INSERT INTO fact_sales (
    order_detail_id,
    order_key,
    pattern_key,
    price_paid,
    download_status
)
SELECT 
    order_detail_id,
    order_id,
    pattern_id,
    price_paid,
    download_status
FROM order_details;