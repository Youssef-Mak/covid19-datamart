SET SCHEMA 'Covid19DataMart';

-- Load Dimensions

\copy date_dimension(date_dim_key, full_date, day, month, year, day_of_year, week_of_year, weekday, is_weekend, season, is_month_start, is_month_end, is_year_start, is_year_end, is_can_holiday, can_holiday_name, is_us_holiday, us_holiday_name) from '../../data/dimensions/date_dimension.csv' delimiter ',' csv header;

\copy patient_dimension(age_group, gender, acquisition_group, outbreak_related, patient_dim_key) from '../../data/dimensions/patient_dimension.csv' delimiter ',' csv header;

\copy phu_dimension(phu_name, address, city, postal_code, url, longitude, latitude, phu_dim_key) from '../../data/dimensions/phu_dimension.csv' delimiter ',' csv header;

\copy weather_dimension(weather_dim_key, daily_high_temperature, daily_low_temperature, precipitation) from '../../data/dimensions/weather_dimension.csv' delimiter ',' csv header;

\copy special_measures_dimension(special_measures_dim_key, keyword_one, keyword_two, title, start_date, end_date, description) from '../../data/dimensions/special_measures_dimension.csv' delimiter ',' csv header;

\copy mobility_dimension(mobility_dim_key, province, subregion, metro_area, retail_and_recreation, grocery_and_pharmacy, parks, transit_stations, workplaces, residential) from '../../data/dimensions/mobility_dimension.csv' delimiter ',' csv header;

\copy covid19_tracking_fact(resolved, un_resolved, fatal, onset_date_dim_key, reported_date_dim_key, test_date_dim_key, specimen_date_dim_key, patient_dim_key, phu_dim_key, weather_dim_key, special_measures_dim_key, mobility_dim_key) from '../../data/dimensions/fact_dimension.csv' delimiter ',' csv header;

