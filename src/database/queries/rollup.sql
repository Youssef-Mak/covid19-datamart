-- Number of cases grouped by case acquisition_group and Month 
SELECT d.month, p.acquisition_group, GROUPING(d.month, p.acquisition_group), count(*)
FROM 
  "Covid19DataMart".covid19_tracking_fact AS f
  INNER JOIN
  "Covid19DataMart".date_dimension AS d
  ON f.onset_date_dim_key = d.date_dim_key
  INNER JOIN
  "Covid19DataMart".patient_dimension AS p 
  ON f.patient_dim_key = p.patient_dim_key
GROUP BY ROLLUP(d.month, p.acquisition_group)
ORDER BY d.month, p.acquisition_group; -- To display more intuitively

-- Number of cases grouped by acquisition_group and phu_location and year
SELECT d.year, p.acquisition_group, GROUPING(d.year, phu.phu_name, p.acquisition_group), count(*)
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
GROUP BY ROLLUP(d.year, phu.phu_name, p.acquisition_group)
ORDER BY d.year, phu.phu_name, p.acquisition_group; -- To display more intuitively
