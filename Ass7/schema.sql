-- CampusEats Assignment 7: GraphQL dishes database
-- Run this script in MySQL Workbench or with: mysql -u root -p < schema.sql
CREATE DATABASE IF NOT EXISTS campuseats_graphql
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE campuseats_graphql;

CREATE TABLE IF NOT EXISTS dishes (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(120) NOT NULL,
  price DECIMAL(8,2) NOT NULL DEFAULT 0.00,
  available BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (id)
);

-- Re-seed only when the table is empty, so rerunning this script does not duplicate rows.
INSERT INTO dishes (name, price, available)
SELECT seed.name, seed.price, seed.available
FROM (
  SELECT 'Masala Dosa' AS name, 80.00 AS price, TRUE AS available
  UNION ALL SELECT 'Paneer Wrap', 110.00, TRUE
  UNION ALL SELECT 'Veg Fried Rice', 95.00, TRUE
  UNION ALL SELECT 'Cold Coffee', 60.00, FALSE
) AS seed
WHERE NOT EXISTS (SELECT 1 FROM dishes LIMIT 1);
