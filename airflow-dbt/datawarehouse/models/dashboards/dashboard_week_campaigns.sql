WITH 
metrics AS 
(SELECT 
summary_week,
app_name,
campaign_name,
total_impressions,
total_clicks,
total_installs,
total_spend,
total_clicks::float / NULLIF(total_impressions, 0) AS ctr,
total_installs / NULLIF(total_spend, 0) AS cpi
 
FROM {{ ref ('datawarehouse', 'aggregation_week_campaigns') }}
)


SELECT 
summary_week,
app_name,
campaign_name,
total_impressions,
LAG(total_impressions) OVER (PARTITION BY app_name, campaign_name ORDER BY summary_week) AS prev_impressions,
total_clicks,
LAG(total_clicks) OVER (PARTITION BY app_name, campaign_name ORDER BY summary_week) AS prev_clicks,
total_installs,
LAG(total_installs) OVER (PARTITION BY app_name, campaign_name ORDER BY summary_week) AS prev_installs,
total_spend,
LAG(total_spend) OVER (PARTITION BY app_name, campaign_name ORDER BY summary_week) AS prev_spend,
ctr,
LAG(ctr) OVER (PARTITION BY app_name, campaign_name ORDER BY summary_week) AS prev_ctr,
ctr::float - LAG(ctr) OVER (PARTITION BY app_name, campaign_name ORDER BY summary_week) / NULLIF(ctr, 0) AS wow_ctr,
cpi,
LAG(cpi) OVER (PARTITION BY app_name, campaign_name ORDER BY summary_week) AS prev_cpi,
cpi::float - LAG(cpi) OVER (PARTITION BY app_name, campaign_name ORDER BY summary_week) / NULLIF(cpi, 0) AS wow_cpi

FROM metrics
