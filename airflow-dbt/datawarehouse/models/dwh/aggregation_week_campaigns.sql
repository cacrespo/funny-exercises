SELECT 
DATE_TRUNC('week', summary_date) AS summary_week,
app_name,
campaign_name,
SUM(impressions) AS total_impressions,
SUM(clicks) AS total_clicks,
SUM(installs) AS total_installs,
SUM(spend) AS total_spend
 
FROM {{ ref ('datawarehouse', 'transformed_dataset') }}
GROUP BY 1, 2, 3
