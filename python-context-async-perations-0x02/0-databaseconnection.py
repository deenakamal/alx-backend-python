#!/usr/bin/env python3
import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_name)
        return self.conn  # Return the connection to use inside the `with` block

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()  # Always close the connection

# Usage of the custom context manager to fetch data from 'users' table
if __name__ == "__main__":
    with DatabaseConnection("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
