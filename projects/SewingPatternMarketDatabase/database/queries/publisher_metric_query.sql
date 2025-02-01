SELECT 
    publisher_name,
    total_patterns,
    total_sales,
    total_revenue
FROM vw_publisher_metrics
ORDER BY total_revenue DESC;