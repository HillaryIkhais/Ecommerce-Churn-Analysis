-- ============================================================
-- Ecommerce Churn Feature Engineering
-- All features built from raw transactions using SQL
-- Snapshot date: 2011-12-09 (last date in dataset)
-- ============================================================

-- Step 1: establish the reference date
-- (latest invoice date in the data, used to calculate recency)
-- SELECT MAX(InvoiceDate) FROM transactions;
-- → 2011-12-09

-- ============================================================
-- CORE FEATURE TABLE
-- One row per customer, all 8 model features + extras
-- ============================================================

CREATE VIEW IF NOT EXISTS customer_features AS

WITH snapshot AS (
    SELECT DATE('2011-12-09') AS ref_date
),

customer_stats AS (
    SELECT
        CustomerID,

        -- original 8 features your model already uses
        COUNT(DISTINCT InvoiceNo)                          AS total_orders,
        SUM(Quantity)                                      AS total_items,
        ROUND(SUM(Revenue), 2)                             AS total_revenue,
        ROUND(SUM(Revenue) / COUNT(DISTINCT InvoiceNo), 2) AS avg_order_value,
        COUNT(DISTINCT StockCode)                          AS unique_products,
        CAST(
            JULIANDAY((SELECT ref_date FROM snapshot)) -
            JULIANDAY(MAX(InvoiceDate))
        AS INTEGER)                                        AS days_since_last_purchase,
        CAST(
            JULIANDAY(MAX(InvoiceDate)) -
            JULIANDAY(MIN(InvoiceDate))
        AS INTEGER)                                        AS customer_lifespan,
        ROUND(
            COUNT(DISTINCT InvoiceNo) * 1.0 /
            NULLIF(
                CAST(
                    JULIANDAY(MAX(InvoiceDate)) -
                    JULIANDAY(MIN(InvoiceDate))
                AS INTEGER),
            0),
        4)                                                 AS purchase_frequency,

        -- new features SQL makes easy
        COUNT(DISTINCT strftime('%Y-%m', InvoiceDate))     AS active_months,
        COUNT(DISTINCT Country)                            AS countries_ordered_from,
        ROUND(MIN(Revenue), 2)                             AS smallest_order_value,
        ROUND(MAX(Revenue), 2)                             AS largest_order_value,
        MIN(InvoiceDate)                                   AS first_purchase_date,
        MAX(InvoiceDate)                                   AS last_purchase_date

    FROM transactions
    GROUP BY CustomerID
),

-- Step 2: define churn
-- A customer is churned if their last purchase was 90+ days before snapshot
-- This is explicit and reproducible — not buried in a notebook
churn_labels AS (
    SELECT
        CustomerID,
        CASE WHEN days_since_last_purchase >= 90 THEN 1 ELSE 0 END AS churned
    FROM customer_stats
)

SELECT
    s.*,
    c.churned
FROM customer_stats s
JOIN churn_labels c ON s.CustomerID = c.CustomerID;