SET SCHEMA 'Covid19DataMart';

-- Dimensional Tables

CREATE TABLE IF NOT EXISTS date_dimension (
  date_dim_key serial not null,
  full_date varchar,
  day int,
  month int,
  year int,
  day_of_year int,
  week_of_year int,
  weekday int,
  is_weekend boolean,
  season varchar,
  is_month_start boolean,
  is_month_end boolean,
  is_year_start boolean,
  is_year_end boolean,
  is_can_holiday boolean,
  can_holiday_name varchar,
  is_us_holiday boolean,
  us_holiday_name varchar,
  primary key (date_dim_key)
);

CREATE TABLE IF NOT EXISTS patient_dimension (
  patient_dim_key serial not null,
  gender varchar,
  age_group varchar,
  acquisition_group varchar,
  outbreak_related boolean,
  primary key (patient_dim_key)
);

CREATE TABLE IF NOT EXISTS phu_dimension (
  phu_dim_key serial not null,
  phu_name varchar,
  address varchar,
  city varchar,
  postal_code varchar,
  province varchar,
  url varchar,
  latitude float,
  longitude float,
  primary key (phu_dim_key)
);

CREATE TABLE IF NOT EXISTS weather_dimension (
  weather_dim_key serial not null,
  daily_high_temperature float,
  daily_low_temperature float,
  precipitation float,
  primary key (weather_dim_key)
);

CREATE TABLE IF NOT EXISTS special_measures_dimension (
  special_measures_dim_key serial not null,
  title varchar,
  description varchar,
  keyword_one varchar,
  keyword_two varchar,
  start_date varchar,
  end_date varchar,
  primary key (special_measures_dim_key)
);

CREATE TABLE IF NOT EXISTS mobility_dimension (
  mobility_dim_key serial not null,
  metro_area varchar,
  subregion varchar,
  province varchar,
  retail_and_recreation float,
  grocery_and_pharmacy float,
  parks float,
  transit_stations float,
  workplaces float,
  residential float,
  primary key (mobility_dim_key)
);

-- Fact table

create table covid19_tracking_fact (
  onset_date_dim_key int,
  reported_date_dim_key int,
  test_date_dim_key int,
  specimen_date_dim_key int,
  patient_dim_key int,
  phu_dim_key int,
  weather_dim_key int,
  special_measures_dim_key int,
  mobility_dim_key int,
  resolved boolean,
  un_resolved boolean,
  fatal boolean,
  foreign key (onset_date_dim_key) references date_dimension(date_dim_key),
  foreign key (reported_date_dim_key) references date_dimension(date_dim_key),
  foreign key (test_date_dim_key) references date_dimension(date_dim_key),
  foreign key (specimen_date_dim_key) references date_dimension(date_dim_key),
  foreign key (phu_dim_key) references phu_dimension(phu_dim_key),
  foreign key (weather_dim_key) references weather_dimension(weather_dim_key),
  foreign key (special_measures_dim_key) references special_measures_dimension(special_measures_dim_key),
  foreign key (mobility_dim_key) references mobility_dimension(mobility_dim_key),
  primary key (onset_date_dim_key, reported_date_dim_key, test_date_dim_key, specimen_date_dim_key, patient_dim_key, phu_dim_key, weather_dim_key, special_measures_dim_key, mobility_dim_key)
);

