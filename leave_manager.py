import sqlite3

class DBLeaveManager:
    def __init__(self):
        self.db_name = "hrms.db"

    def submit_request(self, user_id, leave_type, start_date, end_date):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Replaces: self.global_leaves.append(request)
        # SQLite autoincrements the leave_id automatically!
        cursor.execute("""
            INSERT INTO leave_requests (user_id, leave_type, start_date, end_date, status, admin_comment)
            VALUES (?, ?, ?, ?, 'Pending', '')
        """, (user_id, leave_type, start_date, end_date))
        
        conn.commit()
        conn.close()
        print(f"Leave submitted successfully into database.")

    def process_request_decision(self, leave_id, action_decision, manager_comment):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # Replaces your entire 'for' loop lookup with a single target update step!
        cursor.execute("""
            UPDATE leave_requests 
            SET status = ?, admin_comment = ? 
            WHERE leave_id = ?
        """, (action_decision, manager_comment, leave_id))
        
        conn.commit()
        
        # cursor.rowcount tells us exactly how many rows matched our WHERE check
        if cursor.rowcount > 0:
            print(f"Leave Request ID {leave_id} updated to: {action_decision}")
        else:
            print("Leave Request Not Found")
            
        conn.close()