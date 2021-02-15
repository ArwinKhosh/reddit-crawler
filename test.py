from common.database import SQLiteConnection
from common.constants import DB_FILE

db_connector = SQLiteConnection(DB_FILE)

db_connector.create_tables()

print(db_connector.get_latest_comment())

