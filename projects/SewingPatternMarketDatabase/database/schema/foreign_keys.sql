SELECT 
    TABLE_NAME AS source_table,
    COLUMN_NAME AS foreign_key,
    REFERENCED_TABLE_NAME AS target_table,
    REFERENCED_COLUMN_NAME AS target_column,
    CONSTRAINT_NAME
FROM 
    INFORMATION_SCHEMA.KEY_COLUMN_USAGE
WHERE 
    REFERENCED_TABLE_NAME IS NOT NULL
    AND TABLE_SCHEMA = DATABASE() -- current database
    AND TABLE_NAME IN (
        'fact_sales',
        'dim_order',
        'dim_pattern',
        'dim_garment_type',
        'dim_customer'
    )
ORDER BY 
    TABLE_NAME, 
    COLUMN_NAME;