import logging, re, os

DB_BASE_PATH = "db"

appartment_number_column_name = os.getenv("APPARTMENT_COLUMN_NAME", 14)
address_column_name = os.getenv("ADDRESS_COLUMN_NAME", 13)
csv_file_name =  os.getenv("DB_NAME", 'db.csv')
csv_file = f"{DB_BASE_PATH}/{csv_file_name}" 
input_csv = f"input/{os.getenv('INPUT_FILE_NAME', 'input.csv')}"
table_name = os.getenv("TABLE_NAME", "table1")

sqlite_db = f"{DB_BASE_PATH}/dataset.db"
output_csv = "output/output.csv"

LOG_BASE_PATH = "log"
LOG_FILE = f"{LOG_BASE_PATH}/logs.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

def extract_address_parts(address):
    """Extract city, street, house number, korpus, stroenie, and apartment number from an address string."""
    if not address:
        return {}
    
    address = address.lower()
    
    # Remove unnecessary words
    address = re.sub(r'\b(город|г\.)\s*', '', address)  
    address = re.sub(r'\b(проспект|просп\.|улица|ул\.)\s*', '', address)  
    address = re.sub(r'\b(дом|д\.)\s*', '', address)  
    address = re.sub(r'\b(корпус|корп\.|к\.)\s*', 'корпус ', address)  
    address = re.sub(r'\b(стр\.)\s*', 'строение ', address)  
    address = re.sub(r'\b(квартира|кв\.)\s*', 'квартира ', address)  # Normalize "квартира"
  

    # Split address into parts
    parts = [p.strip() for p in address.split(',')]

    # Extract components
    city = parts[0] if len(parts) > 0 else ''
    street = parts[1] if len(parts) > 1 else ''
    house = parts[2] if len(parts) > 2 else ''

    korpus, stroenie, apartment = '', '', ''
    for part in parts[3:]:  
        if "корпус" in part:
            korpus = part.replace("корпус", "").strip()
        elif "строение" in part:
            stroenie = part.replace("строение", "").strip()
        elif "квартира" in part:
            apartment = part.replace("квартира", "").strip()
        elif part.isdigit():  # If there's an isolated number, assume it's an apartment
            apartment = part
    return {
        "city": city,
        "street": street,
        "house": house,
        "korpus": korpus,
        "stroenie": stroenie,
        "apartment": apartment
    }