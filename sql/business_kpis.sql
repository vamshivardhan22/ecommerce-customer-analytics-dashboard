-- Executive ecommerce KPI queries

SELECT ROUND(SUM(sales), 2) AS revenue FROM orders;

SELECT ROUND(SUM(profit), 2) AS profit FROM orders;

SELECT ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS average_order_value FROM orders;

SELECT
  ROUND(
    100.0 * SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) / COUNT(*),
    2
  ) AS repeat_purchase_rate
FROM (
  SELECT customer_id, COUNT(DISTINCT order_id) AS order_count
  FROM orders
  GROUP BY customer_id
);

SELECT
  customer_id,
  ROUND(SUM(sales), 2) AS customer_lifetime_value,
  COUNT(DISTINCT order_id) AS orders
FROM orders
GROUP BY customer_id
ORDER BY customer_lifetime_value DESC
LIMIT 20;
