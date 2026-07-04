import sqlite3

def calculate_daily_status(check_in_time, check_out_time):
    if not check_in_time or check_in_time == "":
        return 'Absent'
    if not check_out_time or check_out_time == "":
        return 'Present' 

    in_hours, in_mins = map(int, check_in_time.split(":"))
    out_hours, out_mins = map(int, check_out_time.split(":"))

    total_in_hours = in_hours + (in_mins / 60)
    total_out_hours = out_hours + (out_mins / 60)
    hours_worked = total_out_hours - total_in_hours

    if hours_worked < 4:
        return 'Half-day'
    else:
        return 'Present'

def format_weekly_summary_db(user_id):
    conn = sqlite3.connect("hrms.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT status, COUNT(*) FROM attendance 
        WHERE user_id = ? 
        GROUP BY status
    """, (user_id,))
    rows = cursor.fetchall()
    conn.close()

    summary = {"Absent": 0, "Half-day": 0, "Present": 0, "Leave": 0}
    for row in rows:
        status_name, count = row[0], row[1]
        if status_name in summary:
            summary[status_name] = count
            
    return summary

class DBAttendanceTracker:
    def __init__(self):
        self.db_name = "hrms.db"

    def add_record(self, user_id, date, check_in, check_out):
        status = calculate_daily_status(check_in, check_out)
        
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO attendance (user_id, date, check_in, check_out, status)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id, date) DO UPDATE SET
                    check_in = excluded.check_in,
                    check_out = excluded.check_out,
                    status = excluded.status
            """, (user_id, date, check_in, check_out, status))
            conn.commit()
            print(f"Attendance recorded into database for User {user_id}: {status}")
        except sqlite3.Error as e:
            print(f"Database Error: {e}")
        finally:
            conn.close()