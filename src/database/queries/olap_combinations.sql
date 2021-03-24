-- Grouped by Acquisition Groups and phu name when there is a holiday
SELECT phu.phu_name, p.acquisition_group, count(*), GROUPING(phu.phu_name, p.acquisition_group)
FROM 
  "Covid19DataMart".covid19_tracking_fact AS f
  INNER JOIN
  "Covid19DataMart".date_dimension AS d
  ON f.onset_date_dim_key = d.date_dim_key
  INNER JOIN
  "Covid19DataMart".patient_dimension AS p 
  ON f.patient_dim_key = p.patient_dim_key
  INNER JOIN
  "Covid19DataMart".phu_dimension AS phu
  ON f.phu_dim_key = phu.phu_dim_key 
WHERE d.is_can_holiday = 't' OR d.is_us_holiday = 't'
GROUP BY ROLLUP(phu.phu_name, p.acquisition_group)
ORDER BY (phu.phu_name, p.acquisition_group); -- To display more intuitively

-- Number of cases grouped by acquisition_group and phu_location and season for patients in their 20s
SELECT d.season, p.acquisition_group, phu.phu_name, GROUPING(d.season, phu.phu_name, p.acquisition_group), count(*)
FROM 
  "Covid19DataMart".covid19_tracking_fact AS f
  INNER JOIN
  "Covid19DataMart".date_dimension AS d
  ON f.onset_date_dim_key = d.date_dim_key
  INNER JOIN
  "Covid19DataMart".patient_dimension AS p 
  ON f.patient_dim_key = p.patient_dim_key
  INNER JOIN
  "Covid19DataMart".phu_dimension AS phu 
  ON f.phu_dim_key = phu.phu_dim_key
  WHERE p.age_group = '20s'
GROUP BY ROLLUP(d.season, phu.phu_name, p.acquisition_group)
ORDER BY d.season, phu.phu_name, p.acquisition_group; -- To display more intuitively

-- Number of fatal cases of female close contact fatalities and retail and recreation metric in period of two months(November and December) in Peel and Ottawa
SELECT mob.retail_and_recreation, phu.phu_name, count(*)
FROM 
  "Covid19DataMart".covid19_tracking_fact AS f
  INNER JOIN
  "Covid19DataMart".date_dimension AS d
  ON f.onset_date_dim_key = d.date_dim_key
  INNER JOIN
  "Covid19DataMart".patient_dimension AS p 
  ON f.patient_dim_key = p.patient_dim_key
  INNER JOIN
  "Covid19DataMart".phu_dimension AS phu 
  ON f.phu_dim_key = phu.phu_dim_key
  INNER JOIN
  "Covid19DataMart".mobility_dimension AS mob
  ON f.mobility_dim_key = mob.mobility_dim_key
  WHERE d.month IN (11, 12) AND p.gender = 'MALE' AND p.acquisition_group = 'CC' AND phu.phu_name IN ('Peel Public Health', 'Ottawa Public Health') AND f.fatal = 't'
GROUP BY (phu.phu_name, mob.retail_and_recreation)
ORDER BY count(*);
