-- Case outcomes per phu on April 2020
SELECT phu.phu_name, f.resolved, f.un_resolved, f.fatal, count(*)
FROM 
  "Covid19DataMart".covid19_tracking_fact AS f
  INNER JOIN
  "Covid19DataMart".phu_dimension AS phu 
  ON f.phu_dim_key = phu.phu_dim_key
  INNER JOIN
  "Covid19DataMart".date_dimension AS d
  ON f.onset_date_dim_key = d.date_dim_key
WHERE d.year = 2020 AND d.month = 4 
GROUP BY (phu.phu_name, f.resolved, f.un_resolved, f.fatal)
ORDER BY (phu.phu_name);

-- Cases per phu when special measure is Lockdown 
SELECT phu.phu_name, count(*)
FROM 
  "Covid19DataMart".covid19_tracking_fact AS f
  INNER JOIN
  "Covid19DataMart".phu_dimension AS phu 
  ON f.phu_dim_key = phu.phu_dim_key
  INNER JOIN
  "Covid19DataMart".special_measures_dimension AS s
  ON f.special_measures_dim_key = s.special_measures_dim_key
WHERE s.title = 'Lockdown'
GROUP BY (phu.phu_name)
ORDER BY (phu.phu_name, count(*));
