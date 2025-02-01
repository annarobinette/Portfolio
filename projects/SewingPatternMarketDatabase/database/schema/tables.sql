USE running_stitch;

-- Create dimension tables first
CREATE TABLE dim_garment_category (
    category_key INT PRIMARY KEY,
    garment_family VARCHAR(255),
    category_name VARCHAR(255),
    typical_fabric_type VARCHAR(255)
);

CREATE TABLE dim_garment_type (
    garment_type_key INT PRIMARY KEY,
    category_key INT,
    type_name VARCHAR(255),
    FOREIGN KEY (category_key) REFERENCES dim_garment_category(category_key)
);

CREATE TABLE dim_publisher (
    publisher_key INT PRIMARY KEY,
    publisher_name VARCHAR(255),
    website VARCHAR(255),
    commission_rate DECIMAL(5,2),
    country_of_origin VARCHAR(255)
);

CREATE TABLE dim_pattern (
    pattern_key INT PRIMARY KEY,
    publisher_key INT,
    garment_type_key INT,
    pattern_name VARCHAR(255),
    price DECIMAL(10,2),
    description TEXT,
    suggested_fabrics TEXT,
    fabric_requirements TEXT,
    sizing VARCHAR(255),
    notions VARCHAR(255),
    pattern_includes TEXT,
    FOREIGN KEY (publisher_key) REFERENCES dim_publisher(publisher_key),
    FOREIGN KEY (garment_type_key) REFERENCES dim_garment_type(garment_type_key)
);

CREATE TABLE dim_customer (
    customer_key INT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255),
    date_joined DATE,
    age_years INT,
    country VARCHAR(255)
);

CREATE TABLE dim_order (
    order_key INT PRIMARY KEY,
    customer_key INT,
    order_date DATE,
    total_amount DECIMAL(10,2),
    FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key)
);

CREATE TABLE fact_sales (
    order_detail_id INT PRIMARY KEY,
    order_key INT,
    pattern_key INT,
    price_paid DECIMAL(10,2),
    download_status ENUM('expired', 'completed'),
    FOREIGN KEY (order_key) REFERENCES dim_order(order_key),
    FOREIGN KEY (pattern_key) REFERENCES dim_pattern(pattern_key)
);

