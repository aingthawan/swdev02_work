import sqlite3
import random
import time

def insert_rows(conn):
    c = conn.cursor()

    while True:
        # insert random data into the table
        c.execute("INSERT INTO mytable (data) VALUES (?)", (random.randint(0, 100),))
        
        # commit the transaction
        conn.commit()

        # wait for a random amount of time
        time.sleep(random.uniform(0, 5))

if __name__ == "__main__":
    conn = sqlite3.connect("mydatabase.db")
    c = conn.cursor()

    # create the table if it doesn't exist
    c.execute("""
        CREATE TABLE IF NOT EXISTS mytable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data INTEGER
        )
    """)

    # start the insert process
    insert_process = insert_rows(conn)

    try:
        delete_rows(conn)
    except KeyboardInterrupt:
        print("Exiting program")
    
    # close the connection
    conn.close()
