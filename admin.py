import sqlite3
from user import User

class Admin(User):
    def __init__(self, user_id, name, email, password, role):
        super().__init__(user_id, name, email, password, role)

    def add_employee(self, employee):
        conn = sqlite3.connect("hrms.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (user_id, name, email, password, role) 
                VALUES (?, ?, ?, ?, ?)
            """, (employee.user_id, employee.name, employee.email, employee.password, employee.role))
            
            cursor.execute("""
                INSERT INTO employee_profiles (user_id, phone, address, dept, designation, salary, dp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (employee.user_id, employee.phone, employee.address, employee.dept, employee.designation, employee.salary, employee.dp))
            
            conn.commit()
            print(f"Employee {employee.name} permanently saved to database.")
        except sqlite3.IntegrityError:
            print(f"Error: An employee with ID or Email already exists.")
        finally:
            conn.close()

    def remove_employee(self, employee):
        conn = sqlite3.connect("hrms.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE user_id = ?", (employee.user_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"{employee.name} completely removed from system database.")
        else:
            print("Employee record not found.")
        conn.close()

    def view_employees(self):
        conn = sqlite3.connect("hrms.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.user_id, u.name, e.dept, e.designation 
            FROM users u
            JOIN employee_profiles e ON u.user_id = e.user_id
        """)
        rows = cursor.fetchall()
        conn.close()

        print("\n--- System Employee List (Database) ---")
        if not rows:
            print("No registered employees found.")
        for row in rows:
            print(f"ID: {row[0]} | Name: {row[1]} | Dept: {row[2]} | Title: {row[3]}")

    def view_all_attendance(self):
        conn = sqlite3.connect("hrms.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.name, a.date, a.check_in, a.check_out, a.status 
            FROM attendance a
            JOIN users u ON a.user_id = u.user_id
        """)
        rows = cursor.fetchall()
        conn.close()

        print("\n--- Company Global Attendance Logs ---")
        for row in rows:
            print(f"Staff: {row[0]} | Date: {row[1]} | Time: {row[2]}-{row[3]} | Status: {row[4]}")

    def accept_leave(self, leave_id, comment="Approved"):
        from leave_manager import DBLeaveManager
        manager = DBLeaveManager()
        manager.process_request_decision(leave_id, "Approved", comment)

    def reject_leave(self, leave_id, comment="Rejected"):
        from leave_manager import DBLeaveManager
        manager = DBLeaveManager()
        manager.process_request_decision(leave_id, "Rejected", comment)

    def view_employee(self, employee):
        # 1. Display general structural profile records
        employee.view_profile()
        
        # 2. Display the extended calculation breakdown details
        from payroll_manager import DBPayrollManager
        manager = DBPayrollManager()
        pay = manager.get_employee_payroll_view(employee.user_id)
        
        print(f"Allowances:  ${pay['allowances']}")
        print(f"Deductions:  ${pay['deductions']}")
        print(f"Net Take-Home Pay: ${pay['net_salary']}")

    def edit_employee_details(self, employee, detail_to_be_updated, new_detail):
        editable_fields = ["name", "email", "phone", "address", "dept", "designation", "salary", "dp", "role"]

        if detail_to_be_updated not in editable_fields:
            print("This field cannot be updated.")
            return

        conn = sqlite3.connect("hrms.db")
        cursor = conn.cursor()

        if detail_to_be_updated in ["name", "email", "role"]:
            cursor.execute(f"UPDATE users SET {detail_to_be_updated} = ? WHERE user_id = ?", (new_detail, employee.user_id))
        else:
            cursor.execute(f"UPDATE employee_profiles SET {detail_to_be_updated} = ? WHERE user_id = ?", (new_detail, employee.user_id))
        
        conn.commit()
        conn.close()

        setattr(employee, detail_to_be_updated, new_detail)
        print(f"Database successfully updated: {detail_to_be_updated} -> '{new_detail}'.")

    def view_payroll(self):
        import sqlite3
        from payroll_manager import calculate_net_salary
        
        conn = sqlite3.connect("hrms.db")
        cursor = conn.cursor()
        # Querying the comprehensive payroll table alongside user accounts
        cursor.execute("""
            SELECT u.name, e.designation, p.base_salary, p.allowances, p.deductions 
            FROM users u
            JOIN employee_profiles e ON u.user_id = e.user_id
            LEFT JOIN payroll p ON u.user_id = p.user_id
        """)
        rows = cursor.fetchall()
        conn.close()

        print("\n--- Company Payroll Sheet (Database) ---")
        total_payout = 0
        for row in rows:
            name, designation, base, allow, deduct = row
            # Provide fallbacks if payroll records aren't set up yet
            base = base if base else 0.0
            allow = allow if allow else 0.0
            deduct = deduct if deduct else 0.0
            
            # Use our calculation logic
            net_salary = calculate_net_salary(base, allow, deduct)
            
            print(f"Employee: {name} | Position: {designation} | Net Pay: ${net_salary}")
            total_payout += net_salary
            
        print(f"Total Operational Payroll Expense: ${total_payout}")

    def modify_salary_structure(self, employee_id, new_base, new_allowances, new_deductions):
        from payroll_manager import DBPayrollManager
        manager = DBPayrollManager()
        # Full control modification override
        manager.update_structure(employee_id, new_base, new_allowances, new_deductions)

    def view_all_leave_requests(self):
        conn = sqlite3.connect("hrms.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT l.leave_id, u.name, l.leave_type, l.start_date, l.end_date, l.status, l.admin_comment
            FROM leave_requests l
            JOIN users u ON l.user_id = u.user_id
        """)
        rows = cursor.fetchall()
        conn.close()

        print("\n--- Global Leave Requests Register ---")
        if not rows:
            print("No leave applications found.")
            return

        for row in rows:
            leave_id, name, leave_type, start, end, status, comment = row
            print(f"ID: {leave_id} | Staff: {name} | Type: {leave_type} | Duration: {start} to {end} | Status: [{status}]")
            if comment:
                print(f"   Admin Note: {comment}")