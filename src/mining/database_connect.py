import psycopg2
from configparser import ConfigParser

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        password_file = open("C:/Users/grayd/OneDrive/Documents/University of Ottawa/Fourth Year/Winter 2021/CSI4142/Group Project/pass.txt", "r")
        password = password_file.read()
        conn = psycopg2.connect(
            host="www.eecs.uottawa.ca",
            port="15432",
            database="group_17",
            user="ghope049",
            password=password)
	
        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)