SELECT 
    pattern_name, publisher_name,
    total_orders, total_revenue
FROM vw_pattern_performance
WHERE total_orders > 0
ORDER BY total_revenue DESC
LIMIT 10;