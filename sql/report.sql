-- Task 1: Order totals

SELECT
    COUNT(*) AS total_orders,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ),
        2
    ) AS total_revenue,
    ROUND(
        AVG(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ),
        2
    ) AS avg_order_value
FROM orders o
JOIN product p
    ON o.product_id = p.product_id;


-- Task 2: COUNT(*) vs COUNT(rating)

SELECT
    COUNT(*) AS total_orders,
    COUNT(rating) AS rated_orders,
    COUNT(*) - COUNT(rating) AS missing_ratings
FROM orders;

-- Task 3A: Customers with zero orders using LEFT JOIN

SELECT
    c.customer_id,
    c.name
FROM customers c
LEFT JOIN orders o
    ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
HAVING COUNT(o.order_id) = 0;


-- Task 3B: Customers with zero orders using NOT IN

SELECT
    c.customer_id,
    c.name
FROM customers c
WHERE c.customer_id NOT IN (
    SELECT DISTINCT customer_id
    FROM orders
);

-- Task 4A: Top 5 customers by total spend

-- customer_id ASC breaks ties consistently when two customers have the same total spend.

SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ),
        2
    ) AS total_spend
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN product p
    ON o.product_id = p.product_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC, c.customer_id ASC
LIMIT 5;


-- Task 4B: Ranks 3–5 using LIMIT and OFFSET

SELECT
    c.customer_id,
    c.name,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ),
        2
    ) AS total_spend
FROM orders o
JOIN customers c
    ON o.customer_id = c.customer_id
JOIN product p
    ON o.product_id = p.product_id
GROUP BY c.customer_id, c.name
ORDER BY total_spend DESC, c.customer_id ASC
LIMIT 3 OFFSET 2;

-- Task 5: Category-level order count and revenue

SELECT
    p.category,
    COUNT(o.order_id) AS order_count,
    ROUND(
        SUM(
            o.quantity * p.price *
            (1 - COALESCE(o.discount_pct, 0) / 100.0)
        ),
        2
    ) AS category_revenue
FROM orders o
JOIN product p
    ON o.product_id = p.product_id
JOIN customers c
    ON o.customer_id = c.customer_id
GROUP BY p.category
ORDER BY category_revenue DESC;

-- Task 6: Customers whose names start with 'A'

SELECT
    customer_id,
    name
FROM customers
WHERE name LIKE 'A%';

-- Task 7: Distinct acquisition sources

SELECT DISTINCT
    acquisition_source
FROM customers
ORDER BY acquisition_source;

-- Task 8: Add and populate loyalty tier

ALTER TABLE customers
ADD COLUMN loyalty_tier VARCHAR(10);

UPDATE customers
SET loyalty_tier =
    CASE
        WHEN city_tier = 1 THEN 'Gold'
        ELSE 'Silver'
    END;