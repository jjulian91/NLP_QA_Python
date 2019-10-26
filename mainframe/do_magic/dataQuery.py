import mysql.connector
from mysql.connector import Error

def dbQuery(select_statement):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='nba_facts',
                                             user='root',
                                             password='dBPJJWa4gkBjBQZn')

        if connection.is_connected():
            db_Info = connection.get_server_info()
            # print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            # print("Your connected to database: ", record)
            query = connection.cursor()
            query.execute(select_statement)
            records = query.fetchall()
            return records


    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")