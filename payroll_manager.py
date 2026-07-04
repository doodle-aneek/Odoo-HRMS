import sqlite3

def calculate_net_salary(base_salary, allowances, deductions):
    return base_salary + allowances - deductions


class DBPayrollManager:
    def __init__(self):
        self.db_name = "hrms.db"

    def update_structure(self, user_id, new_base, new_allowances, new_deductions):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Replaces: self.payroll_registry[user_id] = {...}
        # Uses an INSERT OR REPLACE to update existing rows or add a new record smoothly
        cursor.execute("""
            INSERT OR REPLACE INTO payroll (user_id, base_salary, allowances, deductions)
            VALUES (?, ?, ?, ?)
        """, (user_id, new_base, new_allowances, new_deductions))
        
        # We also want to sync the base_salary over to the general employee profile column
        cursor.execute("""
            UPDATE employee_profiles 
            SET salary = ? 
            WHERE user_id = ?
        """, (new_base, user_id))
        
        conn.commit()
        conn.close()
        print("Payroll structure successfully updated in database.")

    def get_employee_payroll_view(self, user_id):
        """
        Fetches full salary calculation metrics for an employee's profile view[cite: 1].
        """
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT base_salary, allowances, deductions FROM payroll WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            base, allow, deduct = row
            net = calculate_net_salary(base, allow, deduct)
            return {"base": base, "allowances": allow, "deductions": deduct, "net_salary": net}
        return {"base": 0.0, "allowances": 0.0, "deductions": 0.0, "net_salary": 0.0}