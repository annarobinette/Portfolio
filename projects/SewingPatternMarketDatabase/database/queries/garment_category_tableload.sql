-- Making sure I'm using the right database
USE running_stitch;

-- Insert the data
INSERT INTO garment_categories (category_id, garment_family, category_name, typical_fabric_type) VALUES 
(1, 'Tops', 'Blouses', 'Woven fabrics, lightweight to medium weight'),
(2, 'Tops', 'T-Shirts', 'Knit fabrics, light to medium weight'),
(3, 'Bottoms', 'Pants', 'Woven fabrics, medium to heavyweight'),
(4, 'Dresses', 'Casual Dresses', 'Woven or knit fabrics'),
(5, 'Outerwear', 'Jackets', 'Medium to heavyweight fabrics');

-- Viewing the data to verify
SELECT * FROM garment_categories;