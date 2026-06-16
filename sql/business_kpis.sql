-- Executive ecommerce KPI queries for the UCI Online Retail dataset.
-- Note: estimated_profit is modeled because the source data does not include cost.

SELECT ROUND(SUM(revenue), 2) AS revenue FROM orders;

SELECT ROUND(SUM(estimated_profit), 2) AS estimated_profit FROM orders;

SELECT ROUND(SUM(revenue) / COUNT(DISTINCT invoice_no), 2) AS average_order_value FROM orders;

SELECT
  ROUND(
    100.0 * SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS repeat_purchase_rate
FROM (
  SELECT customer_id, COUNT(DISTINCT invoice_no) AS order_count
  FROM orders
  GROUP BY customer_id
);

SELECT
  customer_id,
  ROUND(SUM(revenue), 2) AS customer_lifetime_value,
  COUNT(DISTINCT invoice_no) AS orders,
  MAX(country) AS country
FROM orders
GROUP BY customer_id
ORDER BY customer_lifetime_value DESC
LIMIT 20;

SELECT
  product_category,
  ROUND(SUM(revenue), 2) AS revenue,
  ROUND(SUM(estimated_profit), 2) AS estimated_profit,
  SUM(quantity) AS units
FROM orders
GROUP BY product_category
ORDER BY revenue DESC;
