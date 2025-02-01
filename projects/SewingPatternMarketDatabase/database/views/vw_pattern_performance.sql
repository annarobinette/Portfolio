CREATE OR REPLACE VIEW vw_pattern_performance AS
SELECT 
    dp.pattern_key,
    dp.pattern_name,
    dpub.publisher_name,
    dgt.type_name,
    dp.price,
    COUNT(DISTINCT fs.order_key) as total_orders,
    SUM(fs.price_paid) as total_revenue
FROM 
    dim_pattern dp
    LEFT JOIN dim_publisher dpub ON dp.publisher_key = dpub.publisher_key
    LEFT JOIN dim_garment_type dgt ON dp.garment_type_key = dgt.garment_type_key
    LEFT JOIN fact_sales fs ON dp.pattern_key = fs.pattern_key
GROUP BY 
    dp.pattern_key, 
    dp.pattern_name, 
    dpub.publisher_name, 
    dgt.type_name, 
    dp.price;