CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `running_stitch`.`vw_customer_activity` AS
SELECT 
    dc.customer_key,
    dc.first_name,
    dc.last_name,
    dc.country,
    COUNT(DISTINCT do.order_key) as total_orders,
    SUM(fs.price_paid) as total_spent,
    COUNT(DISTINCT fs.pattern_key) as unique_patterns_bought,
    MAX(do.order_date) as last_purchase_date
FROM 
    dim_customer dc
    LEFT JOIN dim_order do ON dc.customer_key = do.customer_key
    LEFT JOIN fact_sales fs ON do.order_key = fs.order_key
GROUP BY 
    dc.customer_key, dc.first_name, dc.last_name, dc.country;