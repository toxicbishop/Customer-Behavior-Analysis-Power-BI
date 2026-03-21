-- SQL queries for customer shopping behavior analysis
-- Example: Find top 5 customers by purchase amount
SELECT customer_id, SUM(purchase_amount) AS total_spent
FROM customer_shopping_behavior
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 5;
