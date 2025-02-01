-- This query finds patterns that have above-average sales
SELECT 
    dp.pattern_name,
    pub.publisher_name,
    COUNT(*) as sales_count
FROM fact_sales fs
JOIN dim_pattern dp ON fs.pattern_key = dp.pattern_key
JOIN dim_publisher pub ON dp.publisher_key = pub.publisher_key
GROUP BY dp.pattern_key, dp.pattern_name, pub.publisher_name
HAVING sales_count > (
    SELECT AVG(pattern_sales.sale_count)
    FROM (
        SELECT COUNT(*) as sale_count
        FROM fact_sales
        GROUP BY pattern_key
    ) pattern_sales
)
ORDER BY sales_count DESC;