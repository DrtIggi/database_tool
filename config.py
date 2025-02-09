import logging

appartment_number_column_name = "14"

DB_BASE_PATH = "db"
csv_file = "db.csv" 
sqlite_db = f"{DB_BASE_PATH}/dataset.db"
table_name = "table1"
input_csv = "input.csv"
output_csv = "output.csv"

LOG_BASE_PATH = "log"
LOG_FILE = f"{LOG_BASE_PATH}/logs.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)