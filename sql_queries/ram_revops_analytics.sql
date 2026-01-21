/* PROJECT: RAM Automation AI - Subscription & Churn Analysis
   DESCRIPTION: This analysis focuses on SaaS metrics including market penetration, 
   customer segmentation, and revenue retention across Israel and USA markets.
*/

-- 1. Market Penetration by Country and Plan Type
-- Helps identify which subscription tiers are most popular in specific regions.
SELECT country, plan_type, COUNT(customer_id) AS number_of_clients
FROM ram_subscribtions
GROUP BY country, plan_type
ORDER BY number_of_clients DESC;

-- 2. Marketing ROI: Revenue vs Spend by Country
-- Joins subscription revenue with marketing costs to evaluate the profitability of each region.
-- Helps identify which markets provide the best return on ad spend (ROAS).
SELECT s.country, SUM(s.monthly_revenue) AS total_revenue, m.total_ads_spend AS marketing_budget, ROUND(SUM(s.monthly_revenue) / NULLIF(m.total_ads_spend, 0), 2) AS roi_ratio
FROM ram_subscribtions AS, ram_marketing_costs AS m 
WHERE s.country = m.country AND s.churned = false
GROUP BY s.country, m.total_ads_spend
ORDER BY roi_ratio DESC;

--3. Account Age Analysis (Customer Longevity)
-- Measures how long active customers stay with the company to evaluate loyalty and long-term retention.
SELECT (CURRENT_DATE - signup_date) AS period_with_us, customer_id
FROM ram_subscribtions
WHERE churned=false
