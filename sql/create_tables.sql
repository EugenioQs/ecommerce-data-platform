-- ============================================
-- E-Commerce Data Warehouse
-- Create Tables — Redshift Serverless
-- ============================================

-- Drop tables if they exist (for re-runs)
DROP TABLE IF EXISTS fact_sales;
DROP TABLE IF EXISTS dim_products;
DROP TABLE IF EXISTS dim_customers;
DROP TABLE IF EXISTS dim_country;
DROP TABLE IF EXISTS dim_date;

-- ============================================
-- DIMENSION TABLES
-- ============================================

CREATE TABLE dim_products (
    product_id   INT,
    stockcode    VARCHAR(20),
    description  VARCHAR(255)
);

CREATE TABLE dim_customers (
    customer_id  INT
);

CREATE TABLE dim_country (
    country_id  INT,
    country     VARCHAR(100)
);

CREATE TABLE dim_date (
    date_id   INT,
    date      DATE,
    year      INT,
    month     INT,
    day       INT,
    weekday   VARCHAR(20)
);

-- ============================================
-- FACT TABLE
-- ============================================

CREATE TABLE fact_sales (
    invoice_no  VARCHAR(20),
    product_id  INT,
    customer_id INT,
    country_id  INT,
    date_id     INT,
    quantity    INT,
    unit_price  DECIMAL(10, 2),
    revenue     DECIMAL(10, 2)
);
