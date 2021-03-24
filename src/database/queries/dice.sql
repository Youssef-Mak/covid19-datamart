-- Number of fatal cases in period of two months(November and December) in Peel and Ottawa
SELECT d.month, phu.phu_name, count(*)
FROM 
  "Covid19DataMart".covid19_tracking_fact AS f
  INNER JOIN
  "Covid19DataMart".date_dimension AS d
  ON f.onset_date_dim_key = d.date_dim_key
  INNER JOIN
  "Covid19DataMart".phu_dimension AS phu
  ON f.phu_dim_key = phu.phu_dim_key
WHERE d.month IN (11, 12) AND phu.phu_name IN ('Peel Public Health', 'Ottawa Public Health') AND f.fatal = 't'
GROUP BY (d.month, phu.phu_name);

-- Number of fatal cases in period of the summer and spring seasons in contrasting age groups (20s and 70s)
SELECT d.season, pat.age_group, count(*)
FROM 
  "Covid19DataMart".covid19_tracking_fact AS f
  INNER JOIN
  "Covid19DataMart".patient_dimension AS pat
  ON f.patient_dim_key = pat.patient_dim_key
  INNER JOIN
  "Covid19DataMart".date_dimension AS d
  ON f.onset_date_dim_key = d.date_dim_key
WHERE d.season IN ('summer', 'spring') AND pat.age_group IN ('20s', '70s') 
GROUP BY (d.season, pat.age_group);
