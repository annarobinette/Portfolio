SELECT 
    country,
    COUNT(*) as customer_count,
    AVG(total_spent) as avg_customer_spend,
    AVG(total_orders) as avg_orders_per_customer
FROM vw_customer_activity
GROUP BY country
ORDER BY avg_customer_spend DESC;