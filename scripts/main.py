import pandas as pd
import sqlite3
import re
from init_db import init_db
from config import sqlite_db, input_csv, output_csv, logger, table_name, appartment_number_column_name

def check_address_in_db(cursor, apartment_number):
    """Check if the address exists in the database."""
    query = f'SELECT * FROM {table_name} WHERE "{appartment_number_column_name}" LIKE ?'  # Adjust column names
    cursor.execute(query, (f"%{apartment_number}%",))
    return cursor.fetchall(), [desc[0] for desc in cursor.description]  # Returns a list of matches (or empty list if no match)

def extract_address_parts(address):
    """Extract city, street, house number, korpus, and stroenie from an address string."""
    address = address.lower()
    
    # Remove unnecessary words
    address = re.sub(r'\b(город|г\.)\s*', '', address)  
    address = re.sub(r'\b(проспект|просп\.|улица|ул\.)\s*', '', address)  
    address = re.sub(r'\b(дом|д\.)\s*', '', address)  
    address = re.sub(r'\b(корпус|корп\.|к\.)\s*', 'корпус ', address)  
    address = re.sub(r'\b(стр\.)\s*', 'строение ', address)  

    # Split address into parts
    parts = [p.strip() for p in address.split(',')]

    # Extract components
    city = parts[0] if len(parts) > 0 else ''
    street = parts[1] if len(parts) > 1 else ''
    house = parts[2] if len(parts) > 2 else ''

    korpus, stroenie = '', ''
    for part in parts[3:]:  
        if "корпус" in part:
            korpus = part.replace("корпус", "").strip()
        elif "строение" in part:
            stroenie = part.replace("строение", "").strip()

    return {
        "city": city,
        "street": street,
        "house": house,
        "korpus": korpus,
        "stroenie": stroenie
    }

def main():
    init_db()  

    conn = sqlite3.connect(sqlite_db)
    cursor = conn.cursor()
    input_df = pd.read_csv(input_csv)

    updated_rows = []
    
    for _, row in input_df.iterrows():
        apartment_number = str(row['№ квартиры'])  
        db_results, db_columns = check_address_in_db(cursor, apartment_number)  

        matched = False  
        
        for db_entry in db_results:
            # db_address, db_apartment = db_entry
            db_data = dict(zip(db_columns, db_entry))
            db_address = db_entry[12]
            db_apartment = db_entry[13]
            db_parts = extract_address_parts(db_address)

            # Construct input address string and normalize
            input_address = f"{row['Город']},{row['Улица']},{row['Номер дома']},{row.get('Корпус', '')},{row.get('стр.', '')}"
            input_parts = extract_address_parts(input_address)

            # Compare all components
            if (db_parts['city'] == input_parts['city'] and
                db_parts['street'] == input_parts['street'] and
                db_parts['house'] == input_parts['house'] and
                db_parts['korpus'] == input_parts['korpus'] and
                db_parts['stroenie'] == input_parts['stroenie'] and
                str(db_apartment) == apartment_number):
                
                print("✅ Found match:")
                print(f"Input: {input_parts}, Appartment Number: {apartment_number}")
                print(f"DB:{db_parts}, DB Appartment Number: {db_apartment}")
                logger.info(f"Found match: {input_parts}, Appartment Number: {apartment_number}")
                
                # row['Город'] = db_parts['city']
                # row['Улица'] = db_parts['street']
                # row['Номер дома'] = db_parts['house']
                # row['Корпус'] = db_parts['korpus']
                # row['стр.'] = db_parts['stroenie']
                for col in db_columns:
                    if col not in row or pd.isna(row[col]):  # Only add missing columns
                        row[col] = db_data[col]
                
                matched = True
                break  # Stop checking if match is found
        
        updated_rows.append(row)  

    conn.close()

    # Save updated data to output CSV
    output_df = pd.DataFrame(updated_rows)
    output_df.to_csv(output_csv, index=False)

    logger.info(f"✅ Updated input file saved to '{output_csv}'.")

if __name__ == "__main__":
    main()
