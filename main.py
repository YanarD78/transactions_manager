from psycopg2.errors import UniqueViolation

def run_app():
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
    db = None
    try:
        db = DBmanager(db_name, user, password)
        manager = Manager(db)
        client = CLI(manager)
        user_id = client.user()
        if user_id is not None:
            client.run()
    except ConnectionError as e:
        print(f"!!! {e}")
        exit(1)
    finally:
        if db is not None:
            db.drop_cursor()
            db.drop_connection()

if __name__ == "__main__":
    try:
        run_app()
    except KeyboardInterrupt:
        print("Exiting...")
        exit(0)