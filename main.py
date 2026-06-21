from dotenv import load_dotenv
import os
from app.client import CLI
from app.database import DBmanager
from app.manager import Manager

load_dotenv()
db_name = os.getenv("DB_NAME")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")

if not db_name or not user:
    raise ValueError("DB_USER or DB_NAME does not exist in .env")

print('-'*10 + "Finance Manager" + 10*'-')
try:
    db = DBmanager(db_name, user, password)
except ConnectionError as e:
    print(e)
    exit(1)
manager = Manager(db)
client = CLI(manager)
user_id = client.user()
if user_id is not None:
    try:
        client.run()
    finally:
        db.drop_cursor()
        db.drop_connection()