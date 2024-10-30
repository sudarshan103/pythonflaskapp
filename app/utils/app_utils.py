from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError

from app import app, db

def check_database_status(table_name) -> bool :
    with app.app_context():
        try:
            db.session.execute(text("select 1"))
            # Check if table exists
            inspector = inspect(db.engine)
            if table_name in inspector.get_table_names():
                return True
            else:
                print(f"Table '{table_name}' does not exist in the database.")
                return False
        except OperationalError as e:
            return False