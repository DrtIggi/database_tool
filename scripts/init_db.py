import pandas as pd
import sqlite3, os, sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from config import csv_file, sqlite_db, table_name, logger, address_column_name, extract_address_parts

def add_missing_parts():
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()
    
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN city TEXT;")
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN street TEXT;")
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN house TEXT;")
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN korpus TEXT;")
    cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN type_of_street TEXT;")

    cursor.execute(f'SELECT rowid, {address_column_name} FROM {table_name}')
    rows = cursor.fetchall()

    for rowid, address in rows:
        new_ad = extract_address_parts(address)
        cursor.execute(f'UPDATE {table_name} SET city = ?, street = ?, house = ?, korpus = ?, type_of_street = ? WHERE rowid = ?', (new_ad.get('city'),new_ad.get('street'), new_ad.get('house'), new_ad.get('korpus'),  new_ad.get('type_of_street'),rowid))
        

    conn.commit()
    conn.close()

def sort_database():
    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()

    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_first_letter ON {table_name}(street);")
    
    conn.commit()
    conn.close()

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
    add_missing_parts()
    sort_database()
    logger.info(f"CSV file '{csv_file}' successfully converted to SQLite database '{sqlite_db}'.")
    test_db()
    return

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

            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            logger.info(f"Columns in table '{table_name}':")
            for column in columns:
                logger.info(f"Column: {column[1]}")
            
        else:
            logger.warning(f"The table '{table_name}' exists but is empty.")
    else:
        logger.error(f"The table '{table_name}' does not exist in the database.")

    conn.close()
