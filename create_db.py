import sqlite3

def init_database():
    # Connect to SQLite (It will create the 'hrms.db' file if it doesn't exist)
    connection = sqlite3.connect("hrms.db")
    cursor = connection.cursor()

    # 1. Create the Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('Employee', 'HR')) NOT NULL
    );
    """)

    # 2. Create the Employee Profiles Table
    # FOREIGN KEY connects the profile back to the core user account
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employee_profiles (
        user_id INTEGER PRIMARY KEY,
        phone TEXT,
        address TEXT,
        dept TEXT,
        designation TEXT,
        salary REAL,
        dp TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
    );
    """)

    # Commit the changes and close the link to the file
    connection.commit()
    connection.close()
    print("Database tables created successfully inside 'hrms.db'!")

if __name__ == "__main__":
    init_database()