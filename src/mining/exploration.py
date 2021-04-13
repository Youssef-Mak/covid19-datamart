import database_connect
import psycopg2
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def main():
    try:
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
        
        case_counts_query = '''SELECT count(CASE WHEN f.resolved THEN 1 END), count(CASE WHEN f.un_resolved THEN 1 END), count(CASE WHEN f.fatal THEN 1 END) 
                        FROM "Covid19DataMart".covid19_tracking_fact as f'''
        
        case_counts = query_data(case_counts_query, cursor)
        print("Querying for raw data...")
        raw_data = query_data(query_string, cursor)

        visualize_case_counts(case_counts[0])
        print("Processing age groups...")
        boxplot_data = process_age_groups(raw_data, case_counts)
        visualize_age_groups(boxplot_data)
        visualize_boxplot_case_counts(case_counts[0])
        visualize_gender_location(raw_data)

        # close the communication with the PostgreSQL
        cursor.close()
        if database_connection is not None:
                database_connection.close()
                print('Database connection closed.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if database_connection is not None:
            database_connection.close()
            print('Database connection closed.')


def visualize_boxplot_case_counts(case_counts):
    boxplot_data = [1] * case_counts[0] 
    boxplot_data = boxplot_data + [2] * case_counts[1]
    boxplot_data = boxplot_data + [3] * case_counts[2]
    labels = ["x1"]

    fig, ax = plt.subplots()

    # rectangular box plot
    bplot1 = ax.boxplot(boxplot_data,
                        vert=True,  # vertical box alignment
                        patch_artist=True,  # fill with color
                        labels=labels)  # will be used to label x-ticks
    ax.set_title('Distribution of Case Status')

    ax.set_xlabel('Case Status')
    ax.set_ylabel('Observed values')

    plt.show()


def visualize_case_counts(data):
    fig, ax = plt.subplots()

    p1 = ax.bar(0, data[0], label='Resolved', color="green")
    p2 = ax.bar(1, data[1], label='Unresolved', color="blue")
    p3 = ax.bar(2, data[2], label='Fatal', color="red")

    ax.set_title('Number of Cases vs. Status')
    ax.set_ylabel('Number of Cases')
    ax.set_xlabel('Status')
    ax.legend()

    plt.show()
    # fig.savefig('./visualizations/case_counts_bar_chart.png')

def process_age_groups(data, case_counts):
    age_group_case_counts = {"<20": {}, "30s": {}, "40s": {}, "50s": {}, "60s": {}, "70s": {}, "80s": {}, "90+": {}, "UNKNOWN": {}}
    for row in data:
        age = row[7]
        resolved = row[3]
        unresolved = row[4]
        fatal = row[5]

        if age in age_group_case_counts:
            if "resolved" in age_group_case_counts[age] and resolved:
                age_group_case_counts[age]["resolved"] += 1
            elif resolved:
                age_group_case_counts[age]["resolved"] = 1

            if "unresolved" in age_group_case_counts[age] and unresolved:
                age_group_case_counts[age]["unresolved"] += 1
            elif unresolved:
                age_group_case_counts[age]["unresolved"] = 1

            if "fatal" in age_group_case_counts[age] and fatal:
                age_group_case_counts[age]["fatal"] += 1
            elif fatal:
                age_group_case_counts[age]["fatal"] = 1
        else:
            if resolved:
                age_group_case_counts[age] = {"resolved": 1, "unresolved": 0, "fatal": 0}
            if unresolved:
                age_group_case_counts[age] = {"resolved": 0, "unresolved": 1, "fatal": 0}
            if fatal:
                age_group_case_counts[age] = {"resolved": 0, "unresolved": 1, "fatal": 1}

    return age_group_case_counts

def visualize_age_groups(data):
    fig, ax = plt.subplots()
    labels = ["<20", "30s", "40s", "50s", "60s", "70s", "80s", "90+", "UNKNOWN"]
    x = np.arange(len(labels))  # the label locations
    width = 0.15  # the width of the bars

    resolved = []
    unresolved = []
    fatal = []

    for age in labels:
        resolved.append(data[age]["resolved"] if "resolved" in data[age] else 0)
        unresolved.append(data[age]["unresolved"] if "unresolved" in data[age] else 0)
        fatal.append(data[age]["fatal"] if "fatal" in data[age] else 0)

    bar1 = ax.bar(x - width/2, resolved, width, label='resolved')
    bar2 = ax.bar(x, unresolved, width, label='unresolved')
    bar3 = ax.bar(x + width/2, fatal, width, label="fatal")
    
    ax.set_xticks(x)
    ax.set_ylabel('Count')
    ax.set_xlabel("Age Group")
    ax.set_xticklabels(labels)
    ax.set_title('Age Groups vs. Case Status')
    ax.legend()

    plt.show()
    # fig.savefig('./visualizations/age_group_vs_case_status.png')

def visualize_gender_location(data):
    locations = []
    gender_vs_num_cases = dict() # {MTL: {male: 20, female: 10}, ...}

    for row in data:
        location = row[6]
        gender = row[8]
        if location in gender_vs_num_cases:
            if gender.lower() == "male":
                gender_vs_num_cases[location]["male"] += 1
            else:
                gender_vs_num_cases[location]["female"] += 1
        else:
            locations.append(location)
            if gender.lower() == "male":
                gender_vs_num_cases[location] = {"male": 1, "female": 0}
            else:
                gender_vs_num_cases[location] = {"male": 0, "female": 1}

    male_values = [gender_vs_num_cases[location]["male"] for location in locations]
    female_values = [gender_vs_num_cases[location]["female"] for location in locations]
    locations = [x.replace("Public Health", "") for x in locations]
    locations = [x.replace("Health Department", "") for x in locations]
    
    fig, ax = plt.subplots()
    ax.scatter(locations, male_values, color="blue", label="male", edgecolors='none')
    
    ax.scatter(locations, female_values, color="red", label="female", edgecolors='none')

    ax.set_xlabel("PHU Location Name")
    ax.set_ylabel("Case Count")
    ax.set_title("Gender Case Counts for PHU Locations")
    ax.legend()
    ax.grid(True)

    plt.show()
    # fig.savefig('./visualizations/gender_case_counts_phu_location.png')

def query_data(query, cursor):
    cursor.execute(query)
    rows = cursor.fetchall()

    return rows


if __name__ == '__main__':
    main()