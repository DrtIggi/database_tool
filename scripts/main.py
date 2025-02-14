import pandas as pd
import sqlite3
import re
from init_db import init_db
from config import sqlite_db, input_csv, output_csv, logger, table_name, extract_address_parts, appartment_number_column_name

def check_address_in_db(cursor, city, street, house, korpus,  type_of_street,appartment):
    cursor.execute(f'''
        SELECT * FROM {table_name} 
        WHERE city = ? AND street = ? AND house = ? AND korpus = ?  AND type_of_street = ? AND {appartment_number_column_name} = ?
    ''', (city, street, house, korpus,  type_of_street,appartment))
    
    return cursor.fetchall()


def main():
    init_db()  

    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()
    input_df = pd.read_csv(input_csv)

    updated_rows = []
    
    for _, row in input_df.iterrows():
        full_input_addr = extract_address_parts(f"{row['Город']},{row['Улица']},{row['Номер дома']},{row.get('Корпус', '')},{row.get('стр.', '')},{row.get('№ квартиры')}")
        if full_input_addr['street'] == '':
            continue
        res = check_address_in_db(cursor, full_input_addr['city'],full_input_addr['street'],full_input_addr['house'],full_input_addr.get('korpus', ''), full_input_addr.get('type_of_street'),full_input_addr.get('apartment', '')) 
        row['data'] = str(res) if res else ''        
        
        updated_rows.append(row)  

    conn.close()

    output_df = pd.DataFrame(updated_rows)
    output_df.to_csv(output_csv, index=False)

    logger.info(f"✅ Updated input file saved to '{output_csv}'.")

if __name__ == "__main__":
    main()
