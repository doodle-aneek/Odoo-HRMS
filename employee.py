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
            print(f"Salary: ${row[6]}") # Read-only view for employee
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
        from datetime import datetime
        from attendance_manager import DBAttendanceTracker
        
        today = datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%H:%M")
        
        tracker = DBAttendanceTracker()
        tracker.add_record(self.user_id, today, now_time, "")
        print(f"Check in successful at {now_time}")

    def check_out(self):
        from datetime import datetime
        from attendance_manager import DBAttendanceTracker
        
        today = datetime.now().strftime("%Y-%m-%d")
        now_time = datetime.now().strftime("%H:%M")
        
        # Pull check-in time to run correct calculations
        conn = sqlite3.connect("hrms.db")
        cursor = conn.cursor()
        cursor.execute("SELECT check_in FROM attendance WHERE user_id = ? AND date = ?", (self.user_id, today))
        row = cursor.fetchone()
        conn.close()
        
        check_in_time = row[0] if row else "09:00"
        
        tracker = DBAttendanceTracker()
        tracker.add_record(self.user_id, today, check_in_time, now_time)
        print(f"Checkout successful at {now_time}")

    def view_daily_attendance(self):
        pass

    def view_weekly_attendance(self):
        from attendance_manager import format_weekly_summary_db
        summary = format_weekly_summary_db(self.user_id)
        print(f"\n--- Attendance Summary for {self.name} ---")
        for status, count in summary.items():
            print(f"{status}: {count} days")

    def apply_for_leave(self, leave_type, start_date, end_date):
        from leave_manager import DBLeaveManager
        manager = DBLeaveManager()
        manager.submit_request(self.user_id, leave_type, start_date, end_date)

    def view_salary(self):
        print(f"Salary: ${self.salary}")