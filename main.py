import argparse

def run_app():
    from src.clients.cli.client import CLI
    from src.core.manager import Manager

    parser = argparse.ArgumentParser(description="choise the database")
    parser.add_argument("-d", "--db", type=str, choices=["sqlite", "postgres"], default="sqlite", help="select a database")
    args = parser.parse_args()
    if args.db == "postgres":
        from src.db.database import DBmanager
        from dotenv import load_dotenv
        import os

        load_dotenv()
        db_name = os.getenv("DB_NAME")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

        if not db_name or not user:
            raise ValueError("DB_USER or DB_NAME does not exist in .env")
        db = None
        try:
            db = DBmanager(db_name, user, password)
        except ConnectionError as e:
            print(f"!!! {e}")
            exit(1)


    elif args.db == "sqlite":
        from src.db.database_sqlite import DBmanager

        db = None
        db = DBmanager("db_name.db")



    print('-'*10 + "Finance Manager" + 10*'-')
    try:
        manager = Manager(db)
        client = CLI(manager)
        user_id = client.user()
        if user_id is not None:
            client.run()
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