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

def search_phrase_DB(word):
    return dbQuery("select * from phrase join lookup_table as LU on phrase.FK=LU.PK where Phrase"
                   " like " + "'%" + word + "%'")

def search_EXACT_phrase(word):
    return  dbQuery("select * from phrase join lookup_table as LU on phrase.FK=LU.PK where LOWER(Phrase) = LOWER(" + "'" + word + "')")


def search_player_dB(word):
    return dbQuery("select * from player_data where LOWER(name) LIKE LOWER ('%" + word + "%')")


def search_stats_DB(word):
    return dbQuery("select * from stats where LOWER(name) LIKE LOWER ('%" + word + "%')")

def search_player_dB_noLike(word):
    return dbQuery("select * from player_data where LOWER(name) = LOWER ('" + word + "')")


def search_stats_DB_noLike(word):
    return dbQuery("select * from stats where LOWER(name) = LOWER ('" + word + "')")

def search_stats_DB_exact_match(word): #duplicate for playerDB and Phrase DB
    return dbQuery("select * from stats where name = "+ word + "")



# the following functions require word being the RESOLVED column NAME from the stats table.
def search_stats_max_DB(columnName, searchYear):
    return dbQuery(
        "SELECT * FROM stats WHERE "+ columnName +" = ( SELECT MAX("+columnName+") FROM stats WHERE "+columnName+" != 'Unknown') "
                                                                                "AND Year = "+ searchYear + " LIMIT 1")

def search_stats_max_no_year_DB(columnName):
    return dbQuery(
        "SELECT * FROM stats WHERE "+ columnName +" = ( SELECT MAX("+columnName+") FROM stats WHERE "+ columnName +" != 'Unknown') LIMIT 1")

def search_stats_min_DB(columnName, searchYear):
    return dbQuery(
        "SELECT * FROM stats WHERE "+ columnName +" = ( SELECT MIN("+columnName+") FROM stats WHERE "+ columnName +" != 'Unknown') AND Year = "+ searchYear + " LIMIT 1")

def search_stats_min_no_year_DB(columnName):
    return dbQuery(
        "SELECT * FROM stats  WHERE "+ columnName +" = ( SELECT MIN("+columnName+") FROM stats WHERE "+ columnName +" != 'Unknown') LIMIT 1")




