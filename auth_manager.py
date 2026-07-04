import sqlite3

def validate_password_rules(password):
    # Fix: Check for length AND ensure at least one special character is present
    special_characters = "!@#$%^&*()"
    has_special = any(char in special_characters for char in password)
    
    if len(password) > 5 and has_special:
        return True
    return False


class DBAuthManager:
    def __init__(self):
        self.db_name = "hrms.db"

    def sign_up_user(self, name, email, password, role):
        # 1. Enforce security rules using your function
        if not validate_password_rules(password):
            print("Error: Password must be longer than 5 characters and contain a special character.")
            return False
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        try:
            # Replaces: self.registered_users[email] = password
            # Inserts the new credential record directly into the database[cite: 1]
            cursor.execute("""
                INSERT INTO users (name, email, password, role) 
                VALUES (?, ?, ?, ?)
            """, (name, email, password, role))
            
            conn.commit()
            print("Signup successful!")
            return True
            
        except sqlite3.IntegrityError:
            # Replaces: if email in self.registered_users.keys()
            # SQLite raises an IntegrityError automatically due to the UNIQUE constraint on email[cite: 1]
            print("Error: Email already exists.")
            return False
        finally:
            conn.close()

    def sign_in_user(self, email, password):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Pull the record matching the email address[cite: 1]
        cursor.execute("SELECT password, role, name, user_id FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            db_password, role, name, user_id = row
            # Replaces: if self.registered_users[email] == password
            if db_password == password:
                print(f"Login successful! Welcome back, {name}.")
                # Return a dictionary containing session information to guide dashboard routing[cite: 1]
                return {"status": True, "role": role, "user_id": user_id, "name": name}
        
        print("Error: Incorrect credentials.")
        return {"status": False, "role": None, "user_id": None, "name": None}