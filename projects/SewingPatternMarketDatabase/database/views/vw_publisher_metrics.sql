CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `running_stitch`.`vw_publisher_metrics` AS
    SELECT 
        `dpub`.`publisher_key` AS `publisher_key`,
        `dpub`.`publisher_name` AS `publisher_name`,
        `dpub`.`country_of_origin` AS `country_of_origin`,
        COUNT(DISTINCT `dp`.`pattern_key`) AS `total_patterns`,
        COUNT(DISTINCT `fs`.`order_key`) AS `total_sales`,
        SUM(`fs`.`price_paid`) AS `total_revenue`,
        AVG(`fs`.`price_paid`) AS `avg_sale_price`,
        COUNT(DISTINCT `dgt`.`garment_type_key`) AS `garment_types_offered`
    FROM
        (((`running_stitch`.`dim_publisher` `dpub`
        LEFT JOIN `running_stitch`.`dim_pattern` `dp` ON ((`dpub`.`publisher_key` = `dp`.`publisher_key`)))
        LEFT JOIN `running_stitch`.`fact_sales` `fs` ON ((`dp`.`pattern_key` = `fs`.`pattern_key`)))
        LEFT JOIN `running_stitch`.`dim_garment_type` `dgt` ON ((`dp`.`garment_type_key` = `dgt`.`garment_type_key`)))
    GROUP BY `dpub`.`publisher_key` , `dpub`.`publisher_name` , `dpub`.`country_of_origin`