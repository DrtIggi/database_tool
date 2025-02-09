import pandas as pd
import sqlite3, os, sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from config import csv_file, sqlite_db, table_name, logger


def init_db():

    if not os.path.exists(sqlite_db):
        logger.info(f"Database file '{sqlite_db}' does not exist. Initializing the database...")
    else:
        logger.info(f"Database file '{sqlite_db}' already exists. Skipping initialization.")
        return
    df = pd.read_csv(csv_file)

    conn = sqlite3.connect(sqlite_db)

    df.to_sql(table_name, conn, if_exists="replace", index=False)

    conn.close()

    logger.info(f"CSV file '{csv_file}' successfully converted to SQLite database '{sqlite_db}'.")
    test_db()

def test_db():
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()

    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    table_exists = cursor.fetchone()

    if table_exists:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
    
        if count > 0:
            logger.info(f"The table '{table_name}' contains {count} records.")
        
            cursor.execute(f"SELECT * FROM {table_name} LIMIT 5;")
            rows = cursor.fetchall()
        
            logger.info("Top 5 entries:")
            for row in rows:
                logger.info(row)

            # Get column names
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            logger.info(f"Columns in table '{table_name}':")
            for column in columns:
                logger.info(f"Column: {column[1]}")  # column[1] is the column name
            
        else:
            logger.warning(f"The table '{table_name}' exists but is empty.")
    else:
        logger.error(f"The table '{table_name}' does not exist in the database.")

    conn.close()
