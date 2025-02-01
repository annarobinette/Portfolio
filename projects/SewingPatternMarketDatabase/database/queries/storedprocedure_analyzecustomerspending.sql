DELIMITER //
CREATE PROCEDURE analyze_customer_spending(
    IN start_date DATE,
    IN end_date DATE
)
BEGIN
    SELECT 
        dc.country,
        COUNT(DISTINCT dc.customer_key) as customer_count,
        SUM(fs.price_paid) as total_spent,
        AVG(fs.price_paid) as avg_order_value
    FROM dim_customer dc
    JOIN dim_order do ON dc.customer_key = do.customer_key
    JOIN fact_sales fs ON do.order_key = fs.order_key
    WHERE do.order_date BETWEEN start_date AND end_date
    GROUP BY dc.country
    ORDER BY total_spent DESC;
END //
DELIMITER ;