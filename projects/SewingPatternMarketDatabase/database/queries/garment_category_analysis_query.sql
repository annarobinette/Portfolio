SELECT 
    category_name,
    SUM(pattern_count) as total_patterns,
    SUM(total_sales) as total_sales,
    SUM(total_revenue) as total_revenue
FROM vw_garment_category_analysis
GROUP BY category_name
ORDER BY total_sales DESC;