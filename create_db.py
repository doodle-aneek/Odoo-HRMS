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

    # 3. Create the Attendance Table (ADDED NEW)
    # This matches the Present, Absent, Half-day requirements from the document[cite: 1]
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        check_in TEXT,
        check_out TEXT,
        status TEXT CHECK(status IN ('Present', 'Absent', 'Half-day', 'Leave')) NOT NULL,
        UNIQUE(user_id, date),
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
    );
    """)

    # Commit the changes and close the link to the file
    connection.commit()
    connection.close()
    print("Database tables created/updated successfully inside 'hrms.db'!")

if __name__ == "__main__":
    init_database()