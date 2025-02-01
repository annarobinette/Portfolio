CREATE EVENT daily_order_processing
ON SCHEDULE EVERY 1 DAY
STARTS CURRENT_TIMESTAMP
DO
    CALL process_daily_orders() //

DELIMITER ;