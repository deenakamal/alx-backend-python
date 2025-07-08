#!/usr/bin/python3
import mysql.connector
import csv
from uuid import uuid4


def connect_db():
    """connect to the mysql database server """
    try:
        mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        password=''
        )
        return mydb
    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return None
    

def create_database(connection):
    """ Creates database ALX_prodev if not exists """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully")
    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return None
    finally:
        cursor.close()


def connect_to_prodev():
    """connects the ALX_prodev database in MYSQL"""
    try:
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        return mydb
    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return None


def create_table(connection):
    """Creates table user_data if not exists"""
    try:
        cursor = connection.cursor()
        query= """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL NOT NULL    
        )
        """
        cursor.execute(query)
    except mysql.connector.Error as error:
        print(f"Error: {error}")
    
    finally:
        cursor.close()            
    
   
def insert_data(connection, data):
    """Inserts data in the database if it doesn't exist (checked by email)."""
    try:
        cursor = connection.cursor()
        with open(data, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Check if email already exists
                cursor.execute("SELECT * FROM user_data WHERE email = %s", (row['email'],))
                result = cursor.fetchone()
                if result:
                    print(f"Email {row['email']} already exists. Skipping...")
                    continue  # Skip this row if email exists

                # Insert new data
                cursor.execute(
                    "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                    (str(uuid4()), row['name'], row['email'], row['age'])
                )
            connection.commit()
            print("Data insertion completed successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()