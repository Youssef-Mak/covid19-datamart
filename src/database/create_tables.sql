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

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'agegroup') THEN
        CREATE TYPE agegroup AS ENUM (
            'children', -- 0 to 14
            'youth', -- 15 to 24
            'adults', -- 25 to 64
            'seniors' -- 65 over
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
    age_group agegroup,
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
