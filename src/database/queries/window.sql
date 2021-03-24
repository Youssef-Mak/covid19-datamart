-- Public Health Units with total number of cases per month averaged per season
SELECT t.phu_name, t.season, t.month, total, AVG(t.total) over w
FROM
(
  SELECT phu.phu_name, d.season, d.month, count(*) as total
  FROM
    "Covid19DataMart".covid19_tracking_fact as f
    INNER JOIN
    "Covid19DataMart".phu_dimension as phu
    ON f.phu_dim_key = phu.phu_dim_key
    INNER JOIN
    "Covid19DataMart".date_dimension as d
    ON f.onset_date_dim_key = d.date_dim_key
  GROUP BY phu.phu_name, d.season, d.month
) t
WINDOW w as (PARTITION BY phu_name, season)

