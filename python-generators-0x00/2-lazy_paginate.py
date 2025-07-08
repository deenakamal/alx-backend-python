#!/usr/bin/python3

import mysql.connector
from seed import connect_to_prodev


def paginate_users(page_size, offset):
    """ Returs data from database using offset and limit"""
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """Generator rresponsible for loading pages """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        
        yield page
        offset += page_size
        
         
    
