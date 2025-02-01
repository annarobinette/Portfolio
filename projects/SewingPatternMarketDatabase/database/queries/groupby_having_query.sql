-- This query finds publishers with high-value patterns (avg price > overall avg)
SELECT 
    pub.publisher_name,
    COUNT(dp.pattern_key) as pattern_count,
    AVG(dp.price) as avg_pattern_price,
    SUM(fs.price_paid) as total_revenue
FROM dim_publisher pub
JOIN dim_pattern dp ON pub.publisher_key = dp.publisher_key
JOIN fact_sales fs ON dp.pattern_key = fs.pattern_key
GROUP BY pub.publisher_key, pub.publisher_name
HAVING avg_pattern_price > (
    SELECT AVG(price)
    FROM dim_pattern
)
ORDER BY total_revenue DESC;