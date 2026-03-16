import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
DB_FILE = BASE_DIR / "backend" / "youtube_content.db"

def execute_query(sql: str) -> pd.DataFrame:
    """
    Executes SQL query against SQLite database
    and returns results as a Pandas DataFrame.
    """

    conn = None

    try:
        conn = sqlite3.connect(DB_FILE)

        df = pd.read_sql_query(sql, conn)

        return df

    except Exception as e:
        raise RuntimeError(f"Query execution failed: {e}")

    finally:
        if conn:
            conn.close()