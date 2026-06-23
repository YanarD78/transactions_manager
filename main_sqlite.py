def run_app():
    from app.client import CLI
    from app.database_sqlite import DBmanager
    from app.manager import Manager


    print('-'*10 + "Finance Manager" + 10*'-')
    db = None
    try:
        db = DBmanager("db_name.db")
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