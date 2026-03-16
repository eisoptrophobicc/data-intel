import sqlite3

def get_columns(db_path, table):

    conn = None

    try:
        conn = sqlite3.connect(db_path)

        cursor = conn.execute(f"PRAGMA table_info({table})")

        columns = [row[1] for row in cursor.fetchall()]

        return columns

    finally:
        if conn:
            conn.close()