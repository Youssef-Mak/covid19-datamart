-- Explore the total number of possible cases in your datamart; drill down to a year, drill down to a month and drill down to a day
SELECT d.day, count(*)
FROM 
  "Covid19DataMart".covid19_tracking_fact AS f
  INNER JOIN
  "Covid19DataMart".date_dimension AS d
  ON f.onset_date_dim_key = d.date_dim_key
WHERE d.year = 2020 AND d.month = 4 
GROUP BY d.day
ORDER BY d.day; -- To display more intuitively


-- Explore the total number of resolved cases in your datamart; drill down to a month, and drill down to a acquisition_group 
SELECT p.acquisition_group, count(*)
FROM 
  "Covid19DataMart".covid19_tracking_fact AS f
  INNER JOIN
  "Covid19DataMart".date_dimension AS d
  ON f.onset_date_dim_key = d.date_dim_key
  INNER JOIN
  "Covid19DataMart".patient_dimension AS p 
  ON f.patient_dim_key = p.patient_dim_key
WHERE d.year = 2021 AND d.month = 1
GROUP BY p.acquisition_group 
ORDER BY count(*); -- To display more intuitively





