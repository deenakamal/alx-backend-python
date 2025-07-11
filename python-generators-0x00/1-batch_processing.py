#!/usr/bin/python3

import mysql.connector


def stream_users_in_batches(batch_size):
    """Fetches rows in batches"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
            
    except connection.Error as error:
        print(f"Error: {error}")
    
    finally:
        cursor.close()
        connection.close()
        
        

def batch_processing(batch_size):
    """ Process each batch based on users with age 25 or over"""
    users = []
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                
                users.append(user)
        
    return users
                
    