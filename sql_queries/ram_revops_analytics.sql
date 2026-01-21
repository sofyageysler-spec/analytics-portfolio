/* PROJECT: RAM Automation AI - Subscription & Churn Analysis
   DESCRIPTION: This analysis focuses on SaaS metrics including market penetration, 
   customer segmentation, and revenue retention across Israel and USA markets.
*/

-- 1. Market Penetration by Country and Plan Type
-- Helps identify which subscription tiers are most popular in specific regions.
SELECT country, plan_type, COUNT(customer_id) AS number_of_clients
FROM ram_subscriptions
GROUP BY country, plan_type
ORDER BY number_of_clients DESC;

-- 2. High-Value Customer Identification (USA Market)
-- Target list for loyalty programs or upselling opportunities in the US region.
SELECT customer_id, plan_type, monthly_revenue
FROM ram_subscriptions
WHERE country = 'USA' AND monthly_revenue > 50 AND churned = false
ORDER BY monthly_revenue DESC;

--3. Account Age Analysis (Customer Longevity)
-- Measures how long active customers stay with the company to evaluate loyalty and long-term retention.
SELECT (CURRENT_DATE - signup_date) AS period_with_us, customer_id
FROM ram_subscribtions
WHERE churned=false
