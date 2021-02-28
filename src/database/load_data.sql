SET SCHEMA 'Covid19DataMart';

- Load Dimensions

\copy date_dimension(full_date, day, month, year, day_of_year, week_of_year, weekday, is_weekend, quarter, is_month_start, is_month_end, is_year_start, is_year_end, is_can_holiday, can_holiday_name, is_us_holiday, us_holiday_name, date_dim_key) from '../../data/date_dimension.csv' delimiter ',' csv header;

