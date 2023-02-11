import sqlite3
import time

def delete_rows(conn):
    c = conn.cursor()

    while True:
        c.execute("SELECT * FROM mytable LIMIT 1")
        rows = c.fetchall()

        if not rows:
            print("Table is empty. Waiting for data...")
            time.sleep(5)
            continue

        for row in rows:
            # process each row
            print("Processing row:", row)

            # delete the row
            c.execute("DELETE FROM mytable WHERE id = ?", (row[0],))
        
        # commit the transaction
        conn.commit()

if __name__ == "__main__":
    conn = sqlite3.connect("mydatabase.db")
    try:
        delete_rows(conn)
    except KeyboardInterrupt:
        print("Exiting program")
