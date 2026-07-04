import sys
import sqlite3
from datetime import datetime

# Import all modules built across our milestone track
from auth_manager import DBAuthManager
from employee import Employee
from admin import Admin
from attendance_manager import DBAttendanceTracker
from leave_manager import DBLeaveManager

def instantiate_logged_in_user(session):
    """
    Takes the session dictionary returned from successful login 
    and instantiates the correct object populated with database fields.
    """
    user_id = session["user_id"]
    role = session["role"]
    
    conn = sqlite3.connect("hrms.db")
    cursor = conn.cursor()
    
    if role == "HR":
        cursor.execute("SELECT name, email, password FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Admin(user_id, row[0], row[1], row[2], "HR")
            
    elif role == "Employee":
        cursor.execute("""
            SELECT u.name, u.email, u.password, e.phone, e.address, e.dept, e.designation, e.salary, e.dp
            FROM users u
            JOIN employee_profiles e ON u.user_id = e.user_id
            WHERE u.user_id = ?
        """, (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Employee(user_id, row[0], row[1], row[2], "Employee", 
                            row[3], row[4], row[5], row[6], row[7], row[8])
    return None


def employee_dashboard_loop(employee_obj):
    """Continuous operations interface loop for standard staff members."""
    while True:
        print(f"\n=========================================")
        print(f"        EMPLOYEE DASHBOARD: {employee_obj.name.upper()}        ")
        print(f"=========================================")
        print("1. View Profile Details")
        print("2. Update Residential Address")
        print("3. Update Contact Phone Number")
        print("4. Update Display Picture Link")
        print("5. Perform Daily Clock-In")
        print("6. Perform Daily Clock-Out")
        print("7. View Today's Attendance Status")
        print("8. View Long-Term Attendance Metrics")
        print("9. Apply for Leave / Time-Off")
        print("10. View Detailed Salary Structure (Read-Only)")
        print("11. Log Out")
        print("=========================================")
        
        choice = input("Select an option (1-11): ").strip()
        
        if choice == "1":
            employee_obj.view_profile()
        elif choice == "2":
            addr = input("Enter new address string: ")
            employee_obj.update_address(addr)
        elif choice == "3":
            ph = input("Enter new phone layout: ")
            employee_obj.update_phone(ph)
        elif choice == "4":
            dp_link = input("Enter new avatar file path/URL: ")
            employee_obj.update_dp(dp_link)
        elif choice == "5":
            employee_obj.check_in()
        elif choice == "6":
            employee_obj.check_out()
        elif choice == "7":
            employee_obj.view_daily_attendance()
        elif choice == "8":
            employee_obj.view_weekly_attendance()
        elif choice == "9":
            l_type = input("Enter leave classification type (Paid/Sick/Unpaid): ").strip()
            s_date = input("Enter departure start date (YYYY-MM-DD): ").strip()
            e_date = input("Enter return closure end date (YYYY-MM-DD): ").strip()
            employee_obj.apply_for_leave(l_type, s_date, e_date)
        elif choice == "10":
            employee_obj.view_salary()
        elif choice == "11":
            print("Session cleared. Logging out...")
            break
        else:
            print("Invalid input selection identifier.")


def admin_dashboard_loop(admin_obj):
    """Continuous operations override interface loop for HR Executives."""
    while True:
        print(f"\n=========================================")
        print(f"         ADMIN DASHBOARD: {admin_obj.name.upper()}         ")
        print(f"=========================================")
        print("1. Register New Corporate Employee")
        print("2. Permanently Remove Employee Account")
        print("3. View Total Registered Corporate Staff")
        print("4. Inspect Specific Staff Member Profile")
        print("5. Overwrite/Edit Employee Core Data Details")
        print("6. View Company Global Attendance Logs")
        print("7. Review Active Leave Request Pipeline")
        print("8. Process Decision on Pending Leave Request")
        print("9. Modify Employee Compensation Salary Structure")
        print("10. View Global Company Operational Payroll Sheet")
        print("11. Log Out")
        print("=========================================")
        
        choice = input("Select an option (1-11): ").strip()
        
        if choice == "1":
            try:
                emp_id = int(input("Assign New Employee User ID (Integer): "))
                name = input("Enter full name: ")
                email = input("Enter primary corporate email: ")
                password = input("Assign password credential: ")
                phone = input("Enter phone extension: ")
                address = input("Enter residential address layout: ")
                dept = input("Enter departmental group tag: ")
                desig = input("Enter job title classification string: ")
                salary = float(input("Enter initial base salary ($): "))
                dp = input("Enter profile avatar string path: ")
                
                new_emp = Employee(emp_id, name, email, password, "Employee", 
                                   phone, address, dept, desig, salary, dp)
                admin_obj.add_employee(new_emp)
            except ValueError:
                print("Data entry conversion typing validation mistake.")
                
        elif choice == "2":
            try:
                target_id = int(input("Enter target Employee User ID to completely erase: "))
                dummy_emp = Employee(target_id, "", "", "", "Employee", "", "", "", "", 0.0, "")
                admin_obj.remove_employee(dummy_emp)
            except ValueError:
                print("Identifier mismatch typing error.")
                
        elif choice == "3":
            admin_obj.view_employees()
            
        elif choice == "4":
            try:
                target_id = int(input("Enter target Employee User ID to visually map profile: "))
                dummy_emp = Employee(target_id, "", "", "", "Employee", "", "", "", "", 0.0, "")
                admin_obj.view_employee(dummy_emp)
            except ValueError:
                print("Invalid numerical input.")
                
        elif choice == "5":
            try:
                target_id = int(input("Enter target Employee User ID to alter fields: "))
                field = input("Identify column field name to modify: ").strip().lower()
                new_val = input("Provide the replacement value string: ")
                dummy_emp = Employee(target_id, "", "", "", "Employee", "", "", "", "", 0.0, "")
                admin_obj.edit_employee_details(dummy_emp, field, new_val)
            except ValueError:
                print("Conversion validation exception flag triggered.")
                
        elif choice == "6":
            admin_obj.view_all_attendance()
            
        elif choice == "7":
            admin_obj.view_all_leave_requests()
            
        elif choice == "8":
            try:
                l_id = int(input("Enter specific leave request row record ID: "))
                decision = input("Enter confirmation operational decision (Approved/Rejected): ").strip()
                note = input("Add processing administrative validation comment text: ")
                if decision in ["Approved", "Rejected"]:
                    if decision == "Approved":
                        admin_obj.accept_leave(l_id, note)
                    else:
                        admin_obj.reject_leave(l_id, note)
                else:
                    print("Decision variable input range validation failure.")
            except ValueError:
                print("ID input conversion crash.")
                
        elif choice == "9":
            try:
                target_id = int(input("Enter target Employee User ID to alter pay parameters: "))
                base = float(input("Enter updated base salary ($): "))
                allow = float(input("Enter calculated monthly allowance allowances ($): "))
                deduct = float(input("Enter calculated base monthly tracking deductions ($): "))
                admin_obj.modify_salary_structure(target_id, base, allow, deduct)
            except ValueError:
                print("Mathematical processing float conversion validation exception.")
                
        elif choice == "10":
            admin_obj.view_payroll()
            
        elif choice == "11":
            print("Administrative session terminated. Logging out...")
            break
        else:
            print("Invalid input selection option variant loop index identifier.")


def central_application_gateway():
    """Main execution portal handling core application lifecycle operations."""
    auth_portal = DBAuthManager()
    
    while True:
        print("\n=========================================")
        print("   HUMAN RESOURCE MANAGEMENT SYSTEM   ")
        print("=========================================")
        print("1. System Portal Login (Sign In)")
        print("2. Establish Profile Account (Sign Up)")
        print("3. Shutdown Application Engine")
        print("=========================================")
        
        choice = input("Select an option (1-3): ").strip()
        
        if choice == "1":
            email = input("Provide profile identification email: ").strip()
            password = input("Provide verification checking password: ").strip()
            
            session = auth_portal.sign_in_user(email, password)
            if session["status"]:
                user_instance = instantiate_logged_in_user(session)
                if user_instance:
                    if session["role"] == "HR":
                        admin_dashboard_loop(user_instance)
                    else:
                        employee_dashboard_loop(user_instance)
                else:
                    print("Critical runtime instantiation mismatch failure mapping table entities.")
                    
        elif choice == "2":
            name = input("Enter registration profile full name: ")
            email = input("Enter validation account tracking email: ")
            password = input("Establish structural account verification password: ")
            role = input("Specify target clearance authorization role (Employee/HR): ").strip()
            
            if role in ["Employee", "HR"]:
                auth_portal.sign_up_user(name, email, password, role)
            else:
                print("Security role entry assignment boundary constraint restriction error.")
                
        elif choice == "3":
            print("\nShutting down application framework execution pipeline... Goodbye.")
            sys.exit()
        else:
            print("Menu loop variable select range indexing out of operational bounds exception.")

if __name__ == "__main__":
    central_application_gateway()