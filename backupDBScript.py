import sqlite3
import shutil

database = 'libraryClean.db'
backup_file = 'library.db'

def backup_database():
    """Creates a backup copy of the database."""
    try:
        shutil.copy(database, backup_file)
        print("\nDatabase backup created successfully!")
    except Exception as e:
        print("Error during backup:", e)

if __name__ == "__main__":
    backup_database()
