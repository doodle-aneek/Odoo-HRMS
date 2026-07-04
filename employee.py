import sqlite3
from user import User

class Employee(User):
    def __init__(self, user_id, name, email, password, role, phone, address, dept, designation, salary, dp, documents=None):
        super().__init__(user_id, name, email, password, role)
        self.phone = phone
        self.address = address
        self.dept = dept
        self.designation = designation
        self.salary = salary
        self.dp = dp
        self.documents = documents if documents else ""

    def view_profile(self):
        # Dynamically fetch the fresh state from the database
        conn = sqlite3.connect("hrms.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.name, u.email, e.phone, e.address, e.dept, e.designation, e.salary 
            FROM users u
            JOIN employee_profiles e ON u.user_id = e.user_id
            WHERE u.user_id = ?
        """, (self.user_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            print(f"\n--- PROFILE: {row[0]} ---")
            print(f"ID: {self.user_id}")
            print(f"Email: {row[1]}")
            print(f"Phone: {row[2]}")
            print(f"Address: {row[3]}")
            print(f"Department: {row[4]}")
            print(f"Designation: {row[5]}")
            print(f"Salary: {row[6]}") # Visible to the employee as read-only
        else:
            print("Profile record not found in database.")

    def update_address(self, new_address):
        conn = sqlite3.connect("hrms.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE employee_profiles SET address = ? WHERE user_id = ?", (new_address, self.user_id))
        conn.commit()
        conn.close()
        self.address = new_address
        print("Address updated in database successfully.")

    def update_phone(self, new_phone):
        conn = sqlite3.connect("hrms.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE employee_profiles SET phone = ? WHERE user_id = ?", (new_phone, self.user_id))
        conn.commit()
        conn.close()
        self.phone = new_phone
        print("Phone number updated in database successfully.")

    def update_dp(self, new_dp):
        conn = sqlite3.connect("hrms.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE employee_profiles SET dp = ? WHERE user_id = ?", (new_dp, self.user_id))
        conn.commit()
        conn.close()
        self.dp = new_dp
        print("Profile picture updated in database successfully.")

    def check_in(self):
        # Placeholder for dynamic attendance logging
        print(f"Check in tracked for employee {self.name}.")

    def check_out(self):
        # Placeholder for dynamic attendance logging
        print(f"Check out tracked for employee {self.name}.")

    def view_daily_attendance(self):
        pass

    def view_weekly_attendance(self):
        pass

    def apply_for_leave(self, leave_type, start_date, end_date):
        # For a full implementation, you would insert rows into a separate 'leave_requests' table
        print(f"Leave request for {leave_type} sent successfully.")

    def view_salary(self):
        print(f"Salary: {self.salary}")