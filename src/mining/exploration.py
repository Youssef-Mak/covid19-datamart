import database_connect

def main():
    database_connection = database_connect.connect()
    cursor = database_connection.cursor()

    # Get the data
    query_string = '''
                    SELECT spec.title, mob.metro_area, mob.subregion, f.resolved, f.un_resolved, f.fatal, phu.phu_name, p.age_group, p.gender, d.day, d.month, d.season 
                    FROM "Covid19DataMart".covid19_tracking_fact AS f 
                    INNER JOIN "Covid19DataMart".date_dimension AS d 
                    ON f.onset_date_dim_key = d.date_dim_key 
                    INNER JOIN "Covid19DataMart".patient_dimension AS p 
                    ON f.patient_dim_key = p.patient_dim_key  
                    INNER JOIN "Covid19DataMart".phu_dimension AS phu 
                    ON f.phu_dim_key = phu.phu_dim_key
                    INNER JOIN "Covid19DataMart".mobility_dimension AS mob
                    ON f.mobility_dim_key = mob.mobility_dim_key
                    INNER JOIN "Covid19DataMart".special_measures_dimension as spec
                    ON f.special_measures_dim_key = spec.special_measures_dim_key'''
    
    raw_data = query_data(query_string, cursor)

	# close the communication with the PostgreSQL
    cursor.close()
    if database_connection is not None:
            database_connection.close()
            print('Database connection closed.')

def summarize_data(data_rows):
    """
    Splitting up the raw data so it can be summarized through visualization.

    Visualizations will include:
        1. Sum of resolved, unresolved, and fatal histogram
        2. Scatter plot of age group vs. resolved, unresolved, and fatal
        3. boxplot of gender vs. resolved, unresolved, fatal
        4. PHU location vs. num cases
        5. Season 
    """



def query_data(query, cursor):
    # "SELECT part_id, part_name FROM parts ORDER BY part_name"
    cursor.execute(query)
    rows = cursor.fetchall()
    
    return rows


if __name__ == '__main__':
    main()