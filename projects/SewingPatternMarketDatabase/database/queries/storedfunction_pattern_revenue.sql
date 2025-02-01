SELECT pattern_name, calculate_pattern_revenue(pattern_key) as total_revenue
FROM dim_pattern
WHERE calculate_pattern_revenue(pattern_key) > 1000
ORDER BY total_revenue DESC;