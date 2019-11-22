import mysql.connector
from mysql.connector import Error
import do_magic.answerFinder as answer


#todo refactor the search -- do non %like% search first.. if no result then do %like%.

def dbQuery(select_statement):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='nba_facts',
                                             user='root',
                                             password='dBPJJWa4gkBjBQZn',
                                             auth_plugin='mysql_native_password')

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


def dbInsert(statement):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='nba_facts',
                                             user='root',
                                             password='dBPJJWa4gkBjBQZn',
                                             auth_plugin='mysql_native_password')

        if connection.is_connected():
            db_Info = connection.get_server_info()
            # print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")

            cursor.execute(statement)
            connection.commit()

    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            # print("MySQL connection is closed")


def search_player_dB(word):
    return dbQuery(
        "select * from player_data where LOWER(name) LIKE LOWER ('%" + word + "%')")


def search_stats_DB(word):
    return dbQuery(
        "select * from stats where LOWER(name) LIKE LOWER ('%" + word + "%')")


#work min first --- max will be the exact same

def search_stats_max_DB(word, searchYear):
    return dbQuery(
        "select max(word) from stats where Year = searchYear")


#todo get this to a single result so we can resolve the column to get.  once the column is identified we will copy function
# to the max and change the key word.
def search_stats_min_DB(word, searchYear):
    #search for phrase to find column -> get column name from result and plug into where clause
    result = search_phrase_DB(word)
    wordAsArray = []
    wordAsArray.append(word)
    if len(result) > 1:
        result = answer.processResults(result, wordAsArray)
    #get result to single tuple -- extract index 4
    return dbQuery(
        "SELECT * FROM stats WHERE "+ result[4] +" =  ( SELECT MIN(word) FROM stats ) AND Year = "+ searchYear)


def search_phrase_DB(word):
    return dbQuery("select * from phrase join lookup_table as LU on phrase.FK=LU.PK where Phrase"
                   " like " + "'%" + word + "%'")
