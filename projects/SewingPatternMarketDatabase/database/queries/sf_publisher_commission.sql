SELECT 
    publisher_name,
    commission_rate,
    calculate_publisher_earnings(publisher_key) as earnings
FROM dim_publisher
WHERE publisher_key = 1;