-- Top 5 Months with highest amount of deaths in 2020
SELECT d.month, count(*) AS total_deaths
FROM 
  "Covid19DataMart".covid19_tracking_fact AS f
  INNER JOIN
  "Covid19DataMart".phu_dimension AS phu 
  ON f.phu_dim_key = phu.phu_dim_key
  INNER JOIN
  "Covid19DataMart".date_dimension AS d
  ON f.onset_date_dim_key = d.date_dim_key
WHERE d.year = 2020 AND f.fatal = 't'
GROUP BY (d.month)
ORDER BY total_deaths DESC
LIMIT 5;
