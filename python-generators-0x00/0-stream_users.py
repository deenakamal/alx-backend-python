#!/usr/bin/python3
import mysql.connector


def streams_users():
    """Fetches data from table user_data row by row."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        for row in cursor:
            yield row
    except mysql.connector.Error as error:
        print(f"Error: {error}")
    
    finally:
        cursor.close()
        connection.close()


    