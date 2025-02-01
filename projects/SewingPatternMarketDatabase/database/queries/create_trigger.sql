-- This trigger updates the total_amount in dim_order whenever a new sale is added
    DELIMITER //
    CREATE TRIGGER after_sale_insert
    AFTER INSERT ON fact_sales
    FOR EACH ROW
    BEGIN
        UPDATE dim_order
        SET total_amount = (
            SELECT SUM(price_paid)
            FROM fact_sales
            WHERE order_key = NEW.order_key
        )
        WHERE order_key = NEW.order_key;
    END //
    DELIMITER ;