SELECT
CAST(summary_date AS DATE) AS summary_date, 
app_id,
app_type,
app_name,
campaign_id,
campaign_name,	
ad_id,
ad_name,	
impressions,	
clicks,	
installs,	
spend
FROM {{ ref ('dataset') }}

