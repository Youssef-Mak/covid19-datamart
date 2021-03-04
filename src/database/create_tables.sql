SET SCHEMA 'Covid19DataMart';

-- Create Types

DO $$
  BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'season') THEN
      CREATE TYPE season AS ENUM (
        'summer',
        'fall',
        'winter',
        'spring'
      );
END IF;
END$$;

DO $$
  BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'gender') THEN
      CREATE TYPE gender AS ENUM (
        'male',
        'female',
        'other'
      );
END IF;
END$$;

-- Dimensional Tables

CREATE TABLE IF NOT EXISTS date_dimension (
  date_dim_key serial not null,
  full_date date,
  day int,
  month int,
  year int,
  day_of_year int,
  week_of_year int,
  weekday int,
  is_weekend boolean,
  season season,
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
  gender gender,
  age_group varchar(4),
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
  primary key (onset_date_dim_key, reported_date_dim_key, test_date_dim_key, specimen_date_dim_key, patient_dim_key, phu_dim_key, weather_dim_key, special_measures_dim_key, mobility_dim_key),
  foreign key (onset_date_dim_key) references date_dimension(date_dim_key),
  foreign key (reported_date_dim_key) references date_dimension(date_dim_key),
  foreign key (test_date_dim_key) references date_dimension(date_dim_key),
  foreign key (specimen_date_dim_key) references date_dimension(date_dim_key),
  foreign key (phu_dim_key) references phu_dimension(phu_dim_key),
  foreign key (weather_dim_key) references weather_dimension(weather_dim_key),
  foreign key (special_measures_dim_key) references special_measures_dimension(special_measures_dim_key),
  foreign key (mobility_dim_key) references mobility_dimension(mobility_dim_key),
);

