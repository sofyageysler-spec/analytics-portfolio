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

-- 2. Marketing ROI: Revenue vs Spend by Country
-- Joins subscription revenue with marketing costs to evaluate the profitability of each region.
-- Helps identify which markets (e.g., USA vs Israel) provide the best return on ad spend.

SELECT s.country, SUM(s.monthly_revenue) AS total_mrr, m.ads_spend,(SUM(s.monthly_revenue) - m.ads_spend) AS net_profit
FROM ram_subscriptions AS s
JOIN ram_marketing_costs AS m ON s.country = m.country
WHERE s.churned = false
GROUP BY s.country, m.ads_spend;

--3. Account Age Analysis (Customer Longevity)
-- Measures how long active customers stay with the company to evaluate loyalty and long-term retention.
SELECT (CURRENT_DATE - signup_date) AS period_with_us, customer_id
FROM ram_subscribtions
WHERE churned=false
