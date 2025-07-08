#!/usr/bin/python3
from seed import connect_to_prodev


def stream_user_ages():
    """ Generatot that yields user ages """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    
    connection.close()


def compute_avg():
    """Compute Avg"""
    total = 0
    count = 0
    
    for age in stream_user_ages():
        total += age
        count += 1
    if count == 0:
        print("No users found.")
    else:
        avg = total / count
        print(f"Average age of users: {avg:.2f}")
