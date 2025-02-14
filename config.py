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
    """Extracts city, street, house number, korpus, and apartment number from an address string,
       while normalizing street type names and merging 'строение' into 'корпус'.
    """
    if not address:
        return {}

    address = address.lower().strip()

    # Mapping of abbreviations to full names
    street_type_mapping = {
    "просп.": "проспект",
    "пр.": "проспект",  # Added "пр." mapping
    "ул.": "улица",
    "ш.": "шоссе",
    "а.": "аллея",
    "бульв.": "бульвар",
     "пер.": "переулок"
    }

    # Extract street type (abbreviated or full)
    street_type_match = re.search(
    r'(проспект|просп\.|пр\.|улица|ул\.|шоссе|ш\.|аллея|а\.|бульвар|бульв\.|переулок|пер\.)',
    address
)

    if street_type_match:
        type_of_street = street_type_mapping.get(street_type_match.group(0), street_type_match.group(0))
    else:
        type_of_street = ""

    # Normalize "корпус" and "строение" to just "корпус"
    # Remove unnecessary words
    address = re.sub(r'\b(город|г\.)\s*', '', address)
    address = re.sub(r'\b(дом|д\.)\s*', '', address)
    address = re.sub(r'\b(корпус|корп\.|к\.|строение|стр\.)\s*', 'корпус ', address)
    address = re.sub(r'\b(квартира|кв\.)\s*', 'квартира ', address)  

    # Remove street type from the street name but keep it separately
    address = re.sub(
        r'\b(проспект|просп\.|пр\.|улица|ул\.|шоссе|ш\.|аллея|а\.|бульвар|бульв\.|переулок|пер\.)\s*', 
        '', 
        address
    )

    # Split address into parts
    parts = [p.strip() for p in address.split(',')]

    # Extract components
    city = parts[0] if len(parts) > 0 else ''
    street = parts[1] if len(parts) > 1 else ''
    house = parts[2] if len(parts) > 2 else ''

    korpus, apartment = '', ''
    for part in parts[3:]:
        if "корпус" in part:
            korpus = part.replace("корпус", "").strip()
        elif "квартира" in part:
            apartment = part.replace("квартира", "").strip()
        else:
            apartment = part

    return {
        "city": city,
        "street": street,
        "type_of_street": type_of_street,  # Returns full street type (e.g., "проспект" instead of "просп.")
        "house": house,
        "korpus": korpus,
        "apartment": apartment
    }
