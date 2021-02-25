set schema 'Covid19DataMart';

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

