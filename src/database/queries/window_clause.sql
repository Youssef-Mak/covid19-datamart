-- Number of Cases per Public Health Unit and Day compared to moving average of three months
SELECT t.phu_name, t.full_date, total, AVG(t.total) over w as movavg
FROM
(
  SELECT phu.phu_name, d.full_date, count(*) as total
  FROM
    "Covid19DataMart".covid19_tracking_fact as f
    INNER JOIN
    "Covid19DataMart".phu_dimension as phu
    ON f.phu_dim_key = phu.phu_dim_key
    INNER JOIN
    "Covid19DataMart".date_dimension as d
    ON f.onset_date_dim_key = d.date_dim_key
  GROUP BY phu.phu_name, d.full_date
) t
WINDOW w as (PARTITION BY phu_name
            ORDER BY TO_DATE(full_date, 'YYYY-MM-DD')
            RANGE BETWEEN '1 month' PRECEDING
            AND '1 month' FOLLOWING)

