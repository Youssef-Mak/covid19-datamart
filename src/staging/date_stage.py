import os
import sys
import holidays
import pandas as pd
from datetime import date, timedelta

can_holidays = holidays.Canada()
us_holidays = holidays.UnitedStates()

curr_dir = os.path.abspath(os.path.dirname(sys.argv[0]) or '.')
date_csv_path = os.path.join(curr_dir, './../../data/date_dimension.csv')


def get_season(date):
    print(date)
    m = date.month * 100
    d = date.day
    md = m + d

    if ((md >= 301) and (md <= 531)):
        s = 'spring'
    elif ((md > 531) and (md < 901)):
        s = 'summer'
    elif ((md >= 901) and (md <= 1130)):
        s = 'fall'
    elif ((md > 1130) or (md <= 229)):
        s = 'winter'
    else:
        raise IndexError("Invalid date")

    return s


def gen_full_date(df):
    sdate = date(2019, 11, 1)   # start date
    edate = date(2021, 2, 15)   # end date

    delta = edate - sdate       # as timedelta
    for i in range(delta.days + 1):
        day_date = sdate + timedelta(days=i)
        row = {}
        row['full_day_date'] = day_date
        row['day'] = day_date.day
        row['month'] = day_date.month
        row['year'] = day_date.year
        row['day_of_year'] = day_date.timetuple().tm_yday
        row['week_of_year'] = day_date.isocalendar()[1]
        row['weekday'] = day_date.strftime("%w")
        row['is_weekend'] = ((day_date.strftime("%w") == 0) or (day_date.strftime("%w") == 6))
        row['season'] = get_season(day_date)
        row['is_month_start'] = (day_date.day <= 10)
        row['is_month_end'] = (day_date.day >= 20)
        row['is_year_start'] = (day_date.day <= 100)
        row['is_year_end'] = (day_date.timetuple().tm_yday >= 300)
        row['is_can_holiday'] = (day_date in can_holidays)
        row['can_holiday_name'] = (can_holidays.get(day_date, 'Non-Holiday'))
        row['is_us_holiday'] = (day_date in us_holidays)
        row['us_holiday_name'] = (us_holidays.get(day_date, 'Non-Holiday'))
        df = df.append(row, ignore_index=True)

    return df


def generate_dates():
    date_df_columns = [
            "full_date",
            "day",
            "month",
            "year",
            "day_of_year",
            "week_of_year",
            "weekday",
            "is_weekend",
            "season",
            "is_month_start",
            "is_month_end",
            "is_year_start",
            "is_year_end",
            "is_can_holiday",
            "can_holiday_name",
            "is_us_holiday",
            "us_holiday_name",
            ]
    date_df = pd.DataFrame(columns=date_df_columns)

    date_df = gen_full_date(date_df)
    date_df.to_csv(date_csv_path, encoding='utf-8', index=False)
