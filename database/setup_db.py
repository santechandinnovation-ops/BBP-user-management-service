import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.config.database import db

def setup_database():
    try:
        with open('database/init_users_table.sql', 'r') as f:
            sql_script = f.read()

        with db.get_cursor(commit=True) as cursor:
            cursor.execute(sql_script)

        print("Database setup completed successfully!")
        print("Users table created with indexes.")

    except Exception as e:
        print(f"Error setting up database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    setup_database()
