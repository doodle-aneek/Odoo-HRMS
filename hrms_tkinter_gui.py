"""hrms_tkinter_gui.py

Desktop GUI (tkinter) for the HRMS.

This is a *frontend replacement* for your web UI.
It uses `requests` to call your backend REST APIs.

IMPORTANT:
- Your backend currently exists as Python console/SQLite code in this repo.
- This GUI expects a REST backend (recommended). Update the placeholder API URLs
  to match your actual backend REST endpoints.

How to run:
1) Install dependency:
   pip install requests
2) Run:
   python hrms_tkinter_gui.py

Notes:
- The app uses a single `Tk()` root and swaps `Frame` pages.
- Role-based access control (Employee vs HR) is handled by checking `user['role']`.
- If your backend is not REST yet, you can still adapt the placeholder request
  functions to call your backend logic directly.
"""

from __future__ import annotations

import threading
import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


# -----------------------------
# Configuration / API Endpoints
# -----------------------------

API_BASE_URL = "http://localhost:8000"  # TODO: replace with your backend REST base URL

# Auth
API_LOGIN_URL = f"{API_BASE_URL}/auth/sign-in"  # expects {email, password}
API_LOGOUT_URL = f"{API_BASE_URL}/auth/logout"  # optional
API_SIGNUP_URL = f"{API_BASE_URL}/auth/sign-up"  # optional

# Employee data
API_EMPLOYEE_PROFILE_URL = f"{API_BASE_URL}/employee/profile"  # GET/PUT
API_EMPLOYEE_ATTENDANCE_URL = f"{API_BASE_URL}/employee/attendance"  # GET recent
API_EMPLOYEE_CLOCK_URL = f"{API_BASE_URL}/employee/attendance/check"  # POST check-in/out
API_EMPLOYEE_LEAVES_URL = f"{API_BASE_URL}/employee/leaves"  # POST apply, GET mine

# HR/Admin data
API_EMPLOYEE_LIST_URL = f"{API_BASE_URL}/hr/employees"  # GET all employees
API_PENDING_LEAVES_URL = f"{API_BASE_URL}/hr/leaves/pending"  # GET pending
API_APPROVE_LEAVE_URL = f"{API_BASE_URL}/hr/leaves/approve"  # POST
API_REJECT_LEAVE_URL = f"{API_BASE_URL}/hr/leaves/reject"  # POST


# -----------------------------
# Simple data models
# -----------------------------


@dataclass
class Session:
    token: str
    role: str  # "Employee" or "HR"
    user_id: int
    name: str
    email: str


# -----------------------------
# API Client (placeholder)
# -----------------------------


class HRMSApiClient:
    """Thin API client.

    Replace endpoint paths/payload shapes to match your actual backend.
    """

    def __init__(self, base_headers: Optional[Dict[str, str]] = None):
        self.base_headers = base_headers or {}

    @staticmethod
    def _handle_response(resp: requests.Response) -> Any:
        # Try JSON; fallback to text
        try:
            data = resp.json()
        except Exception:
            data = resp.text

        if resp.status_code >= 400:
            # Surface message if present
            msg = None
            if isinstance(data, dict):
                msg = data.get("detail") or data.get("message") or data.get("error")
            raise RuntimeError(msg or f"Request failed (HTTP {resp.status_code})")
        return data

    def login(self, email: str, password: str) -> Session:
        payload = {"email": email, "password": password}
        resp = requests.post(API_LOGIN_URL, json=payload, headers=self.base_headers, timeout=10)
        data = self._handle_response(resp)

        # Expected shape (example):
        # {"token": "...", "role": "Employee", "user_id": 1, "name": "...", "email": "..."}
        return Session(
            token=data.get("token", ""),
            role=data.get("role", "Employee"),
            user_id=int(data.get("user_id", 0)),
            name=data.get("name", ""),
            email=data.get("email", email),
        )

    def get_employee_profile(self, session: Session) -> Dict[str, Any]:
        headers = {**self.base_headers, "Authorization": f"Bearer {session.token}"}
        resp = requests.get(API_EMPLOYEE_PROFILE_URL, headers=headers, timeout=10)
        data = self._handle_response(resp)
        return data

    def update_employee_profile(self, session: Session, address: str, phone: str, dp: str) -> None:
        headers = {**self.base_headers, "Authorization": f"Bearer {session.token}"}
        payload = {"address": address, "phone": phone, "dp": dp}
        resp = requests.put(API_EMPLOYEE_PROFILE_URL, json=payload, headers=headers, timeout=10)
        _ = self._handle_response(resp)

    def get_recent_attendance(self, session: Session, limit: int = 10) -> List[Dict[str, Any]]:
        headers = {**self.base_headers, "Authorization": f"Bearer {session.token}"}
        params = {"limit": limit}
        resp = requests.get(API_EMPLOYEE_ATTENDANCE_URL, headers=headers, params=params, timeout=10)
        data = self._handle_response(resp)
        return data.get("records", []) if isinstance(data, dict) else data

    def check_in_out(self, session: Session, action: str) -> None:
        """action: 'check_in' or 'check_out'"""
        headers = {**self.base_headers, "Authorization": f"Bearer {session.token}"}
        payload = {"action": action}
        resp = requests.post(API_EMPLOYEE_CLOCK_URL, json=payload, headers=headers, timeout=10)
        _ = self._handle_response(resp)

    def apply_leave(self, session: Session, leave_type: str, start_date: str, end_date: str) -> None:
        headers = {**self.base_headers, "Authorization": f"Bearer {session.token}"}
        payload = {
            "leave_type": leave_type,
            "start_date": start_date,
            "end_date": end_date,
        }
        resp = requests.post(API_EMPLOYEE_LEAVES_URL, json=payload, headers=headers, timeout=10)
        _ = self._handle_response(resp)

    def get_all_employees(self, session: Session) -> List[Dict[str, Any]]:
        headers = {**self.base_headers, "Authorization": f"Bearer {session.token}"}
        resp = requests.get(API_EMPLOYEE_LIST_URL, headers=headers, timeout=10)
        data = self._handle_response(resp)
        return data.get("employees", []) if isinstance(data, dict) else data

    def get_pending_leave_requests(self, session: Session) -> List[Dict[str, Any]]:
        headers = {**self.base_headers, "Authorization": f"Bearer {session.token}"}
        resp = requests.get(API_PENDING_LEAVES_URL, headers=headers, timeout=10)
        data = self._handle_response(resp)
        return data.get("requests", []) if isinstance(data, dict) else data

    def decide_leave(self, session: Session, leave_id: int, action: str, comment: str) -> None:
        headers = {**self.base_headers, "Authorization": f"Bearer {session.token}"}
        payload = {"leave_id": leave_id, "comment": comment}
        url = API_APPROVE_LEAVE_URL if action == "approve" else API_REJECT_LEAVE_URL
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        _ = self._handle_response(resp)


# -----------------------------
# GUI Pages
# -----------------------------


class HRMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Odoo-HRMS Desktop (tkinter)")
        self.geometry("1100x700")

        self.api = HRMSApiClient()
        self.session: Optional[Session] = None

        # shared app state
        self._busy = False

        # layout
        self.container = ttk.Frame(self)
        self.container.pack(fill=tk.BOTH, expand=True)

        # Pages
        self.login_page = LoginPage(self, self.container, self.on_login_success)
        self.sidebar_shell = SidebarShell(self, self.container)

        self.current_page: Optional[tk.Frame] = None
        self.show_login()

    def show_page(self, frame: tk.Frame):
        if self.current_page is not None:
            self.current_page.pack_forget()
        self.current_page = frame
        frame.pack(fill=tk.BOTH, expand=True)

    def show_login(self):
        self.show_page(self.login_page)

    def show_dashboard(self):
        # SidebarShell always has its own internal pages
        self.sidebar_shell.build_for_role(self.session.role if self.session else "Employee")
        self.sidebar_shell.show_page("dashboard")
        self.show_page(self.sidebar_shell)

    def on_login_success(self, session: Session):
        self.session = session
        self.show_dashboard()

    # --------------
    # Background calls
    # --------------

    def run_in_thread(self, target, on_success=None, on_error=None):
        if self._busy:
            return
        self._busy = True

        def worker():
            try:
                result = target()
                if on_success:
                    self.after(0, lambda: on_success(result))
            except Exception as e:
                if on_error:
                    self.after(0, lambda: on_error(e))
                else:
                    self.after(0, lambda: messagebox.showerror("Error", str(e)))
            finally:
                self._busy = False

        threading.Thread(target=worker, daemon=True).start()


class LoginPage(ttk.Frame):
    def __init__(self, app: HRMSApp, parent, on_success):
        super().__init__(parent)
        self.app = app
        self.on_success = on_success

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # centered content
        wrap = ttk.Frame(self)
        wrap.pack(expand=True)

        title = ttk.Label(wrap, text="HRMS Login", font=("Segoe UI", 18, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(10, 18))

        ttk.Label(wrap, text="Email:").grid(row=1, column=0, sticky="e", padx=10, pady=6)
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(wrap, textvariable=self.email_var, width=32)
        email_entry.grid(row=1, column=1, sticky="w", padx=10, pady=6)

        ttk.Label(wrap, text="Password:").grid(row=2, column=0, sticky="e", padx=10, pady=6)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(wrap, textvariable=self.password_var, width=32, show="*")
        password_entry.grid(row=2, column=1, sticky="w", padx=10, pady=6)

        self.status_label = ttk.Label(wrap, text="", foreground="#b91c1c")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=(10, 4))

        self.login_btn = ttk.Button(wrap, text="Login", command=self._login)
        self.login_btn.grid(row=4, column=0, columnspan=2, pady=(14, 6), sticky="we")
        wrap.columnconfigure(0, weight=1)
        wrap.columnconfigure(1, weight=1)

        # allow Enter
        password_entry.bind("<Return>", lambda _e: self._login())

    def _login(self):
        email = self.email_var.get().strip()
        password = self.password_var.get().strip()
        if not email or not password:
            self.status_label.configure(text="Email and password are required.")
            return

        self.status_label.configure(text="Logging in...", foreground="#374151")
        self.login_btn.configure(state=tk.DISABLED)

        def do_login():
            return self.app.api.login(email, password)

        def success(sess: Session):
            self.login_btn.configure(state=tk.NORMAL)
            self.status_label.configure(text="Login successful!", foreground="#16a34a")
            self.on_success(sess)

        def error(e: Exception):
            self.login_btn.configure(state=tk.NORMAL)
            self.status_label.configure(text=str(e) or "Invalid credentials", foreground="#b91c1c")

        self.app.run_in_thread(do_login, on_success=success, on_error=error)


class SidebarShell(ttk.Frame):
    """Persistent navigation + dynamic page switching."""

    def __init__(self, app: HRMSApp, parent):
        super().__init__(parent)
        self.app = app

        self.sidebar = ttk.Frame(self, width=240)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.content = ttk.Frame(self)
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Store role-specific pages
        self.pages: Dict[str, ttk.Frame] = {}

        # Sidebar controls
        ttk.Label(self.sidebar, text="Navigation", font=("Segoe UI", 12, "bold")).pack(pady=(20, 10))

        self.btn_dashboard = ttk.Button(self.sidebar, text="Dashboard", command=lambda: self.show_page("dashboard"))
        self.btn_profile = ttk.Button(self.sidebar, text="Profile", command=lambda: self.show_page("profile"))
        self.btn_attendance = ttk.Button(self.sidebar, text="Attendance", command=lambda: self.show_page("attendance"))
        self.btn_leaves = ttk.Button(self.sidebar, text="Leaves", command=lambda: self.show_page("leaves"))
        self.btn_logout = ttk.Button(self.sidebar, text="Logout", command=self._logout)

        for b in [self.btn_dashboard, self.btn_profile, self.btn_attendance, self.btn_leaves, self.btn_logout]:
            b.pack(fill=tk.X, padx=18, pady=6)

        self.hr_extra_sep = ttk.Separator(self.sidebar)
        self.hr_extra_sep.pack(fill=tk.X, padx=18, pady=(18, 6))

        # HR-only buttons
        self.btn_hr_employees = ttk.Button(
            self.sidebar,
            text="Employee Management",
            command=lambda: self.show_page("hr_employees"),
        )
        self.btn_hr_leaves = ttk.Button(
            self.sidebar,
            text="Leave Approvals",
            command=lambda: self.show_page("hr_leaves"),
        )
        self.btn_hr_payroll = ttk.Button(
            self.sidebar,
            text="Payroll",
            command=lambda: self.show_page("hr_payroll"),
        )

        self.hr_buttons = [self.btn_hr_employees, self.btn_hr_leaves, self.btn_hr_payroll]
        for b in self.hr_buttons:
            b.pack_forget()

        self.current_key: Optional[str] = None

    def build_for_role(self, role: str):
        # Cleanup old pages
        for _k, page in list(self.pages.items()):
            page.destroy()
        self.pages.clear()

        # Ensure correct sidebar visibility
        if role == "HR":
            for b in self.hr_buttons:
                b.pack(fill=tk.X, padx=18, pady=6)
        else:
            for b in self.hr_buttons:
                b.pack_forget()

        # Create pages (role-dependent)
        self.pages["dashboard"] = DashboardPage(self.app, self.content)
        self.pages["profile"] = ProfilePage(self.app, self.content)
        self.pages["attendance"] = AttendancePage(self.app, self.content)
        self.pages["leaves"] = LeavePage(self.app, self.content)

        # HR pages
        self.pages["hr_employees"] = HREmployeeManagementPage(self.app, self.content)
        self.pages["hr_leaves"] = HRLeaveApprovalsPage(self.app, self.content)
        self.pages["hr_payroll"] = HRPayrollPlaceholderPage(self.app, self.content)

        # Load dashboard based on role
        dash = self.pages["dashboard"]
        dash.load_role(role)
        self.pages["profile"].load_role(role)
        self.pages["attendance"].load_role(role)
        self.pages["leaves"].load_role(role)

        self.pages["hr_employees"].load_role(role)
        self.pages["hr_leaves"].load_role(role)
        self.pages["hr_payroll"].load_role(role)

    def show_page(self, key: str):
        # Lazy show: ensure role page exists
        page = self.pages.get(key)
        if not page:
            return

        if self.current_key:
            self.pages[self.current_key].pack_forget()
        self.current_key = key
        page.pack(fill=tk.BOTH, expand=True)

    def _logout(self):
        # Return to login
        self.app.session = None
        # Optionally call logout endpoint
        self.show_page(self.app.login_page)


class DashboardPage(ttk.Frame):
    def __init__(self, app: HRMSApp, parent):
        super().__init__(parent)
        self.app = app
        self.role: str = "Employee"

        # layout
        self.header = ttk.Label(self, text="Dashboard", font=("Segoe UI", 18, "bold"))
        self.header.pack(anchor="w", pady=(18, 10), padx=20)

        self.main = ttk.Frame(self)
        self.main.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.load_role("Employee")

    def load_role(self, role: str):
        self.role = role

        # rebuild content area
        for w in self.main.winfo_children():
            w.destroy()

        if self.role == "Employee":
            self._build_employee_view()
        else:
            self._build_hr_view()

        # fetch data if logged in
        self.refresh()

    def _build_employee_view(self):
        # summary frames
        lf = ttk.LabelFrame(self.main, text="Your Summary", padding=14)
        lf.pack(fill=tk.X, pady=10)

        self.attendance_var = tk.StringVar(value="-")
        self.pending_leave_var = tk.StringVar(value="-")

        ttk.Label(lf, text="Attendance:").grid(row=0, column=0, sticky="w")
        ttk.Label(lf, textvariable=self.attendance_var, font=("Segoe UI", 12, "bold")).grid(
            row=0, column=1, sticky="w", padx=10
        )

        ttk.Label(lf, text="Pending Leave:").grid(row=1, column=0, sticky="w", pady=8)
        ttk.Label(lf, textvariable=self.pending_leave_var, font=("Segoe UI", 12, "bold")).grid(
            row=1, column=1, sticky="w", padx=10, pady=8
        )

        # Quick action
        action = ttk.LabelFrame(self.main, text="Quick Actions", padding=14)
        action.pack(fill=tk.X, pady=10)

        self.quick_check_state = tk.StringVar(value="Ready")
        ttk.Label(action, textvariable=self.quick_check_state).pack(anchor="w")

        btn_row = ttk.Frame(action)
        btn_row.pack(fill=tk.X, pady=10)

        self.btn_checkin = ttk.Button(btn_row, text="Check-in", command=lambda: self._quick_action("check_in"))
        self.btn_checkout = ttk.Button(btn_row, text="Check-out", command=lambda: self._quick_action("check_out"))
        self.btn_checkin.pack(side=tk.LEFT, padx=6)
        self.btn_checkout.pack(side=tk.LEFT, padx=6)

        # Placeholder chart/table
        ttk.Label(self.main, text="Tip: Go to Attendance page for detailed logs.").pack(anchor="w", pady=10)

    def _build_hr_view(self):
        # HR summary
        lf = ttk.LabelFrame(self.main, text="HR Summary", padding=14)
        lf.pack(fill=tk.X, pady=10)

        self.hr_pending_leaves_var = tk.StringVar(value="-")
        ttk.Label(lf, text="Pending approvals requiring action:").grid(row=0, column=0, sticky="w")
        ttk.Label(lf, textvariable=self.hr_pending_leaves_var, font=("Segoe UI", 12, "bold")).grid(
            row=0, column=1, sticky="w", padx=10
        )

        # Tree summary quick peek
        tree_frame = ttk.LabelFrame(self.main, text="Pending Leave Requests (Preview)", padding=14)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        columns = ("leave_id", "employee", "type", "start", "end", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=8)
        for c in columns:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=120, anchor="w")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # make it switchable to approval page
        ttk.Button(tree_frame, text="Open Approvals", command=lambda: self.app.sidebar_shell.show_page("hr_leaves")).pack(
            anchor="e", pady=10
        )

    def _quick_action(self, action: str):
        if not self.app.session:
            return
        session = self.app.session

        def do():
            self.app.api.check_in_out(session, action)

        def ok(_=None):
            self.quick_check_state.set("Updated. Refreshing...")
            self.refresh()
            self.quick_check_state.set("Done")

        def err(e: Exception):
            messagebox.showerror("Attendance Error", str(e))

        self.app.run_in_thread(do, on_success=ok, on_error=err)

    def refresh(self):
        if not self.app.session:
            return
        session = self.app.session

        if self.role == "Employee":
            # For now: show placeholder summary; Attendance/Leaves pages fetch real data.
            self.attendance_var.set("(mock) Recent records available in Attendance")
            self.pending_leave_var.set("(mock) Check Leaves page")
        else:
            # Fetch pending leave preview
            def do():
                return self.app.api.get_pending_leave_requests(session)

            def ok(requests: List[Dict[str, Any]]):
                self.tree.delete(*self.tree.get_children())
                self.hr_pending_leaves_var.set(str(len(requests)))

                for r in requests[:10]:
                    self.tree.insert(
                        "",
                        tk.END,
                        values=(
                            r.get("leave_id"),
                            r.get("user_name") or r.get("employee") or r.get("name"),
                            r.get("leave_type"),
                            r.get("start_date"),
                            r.get("end_date"),
                            r.get("status"),
                        ),
                    )

            def err(e: Exception):
                messagebox.showerror("HR Error", str(e))

            self.app.run_in_thread(do, on_success=ok, on_error=err)


class ProfilePage(ttk.Frame):
    def __init__(self, app: HRMSApp, parent):
        super().__init__(parent)
        self.app = app
        self.role: str = "Employee"

        self.title = ttk.Label(self, text="Profile", font=("Segoe UI", 18, "bold"))
        self.title.pack(anchor="w", pady=(18, 10), padx=20)

        form = ttk.LabelFrame(self, text="Edit Profile", padding=14)
        form.pack(fill=tk.X, padx=20, pady=10)

        self.address_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.dp_var = tk.StringVar()

        ttk.Label(form, text="Address:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        ttk.Entry(form, textvariable=self.address_var, width=60).grid(row=0, column=1, sticky="w", padx=6, pady=6)

        ttk.Label(form, text="Phone:").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        ttk.Entry(form, textvariable=self.phone_var, width=60).grid(row=1, column=1, sticky="w", padx=6, pady=6)

        ttk.Label(form, text="Profile Picture URL:").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        ttk.Entry(form, textvariable=self.dp_var, width=60).grid(row=2, column=1, sticky="w", padx=6, pady=6)

        self.btn_save = ttk.Button(form, text="Save", command=self._save)
        self.btn_save.grid(row=3, column=1, sticky="e", pady=(10, 0))

    def load_role(self, role: str):
        self.role = role
        # Employee should only edit address/phone/dp. HR full editing could be added later.
        # For now, lock same fields regardless.

        self.refresh()

    def refresh(self):
        if not self.app.session:
            return

        session = self.app.session

        def do():
            return self.app.api.get_employee_profile(session)

        def ok(data: Dict[str, Any]):
            self.address_var.set(str(data.get("address", "")))
            self.phone_var.set(str(data.get("phone", "")))
            self.dp_var.set(str(data.get("dp", data.get("avatar", ""))))

        def err(e: Exception):
            # keep existing fields
            messagebox.showerror("Profile Error", str(e))

        self.app.run_in_thread(do, on_success=ok, on_error=err)

    def _save(self):
        if not self.app.session:
            return

        address = self.address_var.get().strip()
        phone = self.phone_var.get().strip()
        dp = self.dp_var.get().strip()

        session = self.app.session

        def do():
            return self.app.api.update_employee_profile(session, address=address, phone=phone, dp=dp)

        def ok(_=None):
            messagebox.showinfo("Saved", "Profile updated successfully.")

        def err(e: Exception):
            messagebox.showerror("Save Error", str(e))

        self.app.run_in_thread(do, on_success=ok, on_error=err)


class AttendancePage(ttk.Frame):
    def __init__(self, app: HRMSApp, parent):
        super().__init__(parent)
        self.app = app
        self.role: str = "Employee"

        self.title = ttk.Label(self, text="Attendance Tracking", font=("Segoe UI", 18, "bold"))
        self.title.pack(anchor="w", pady=(18, 10), padx=20)

        # Toggle block
        top = ttk.LabelFrame(self, text="Check-in / Check-out", padding=14)
        top.pack(fill=tk.X, padx=20, pady=10)

        self.toggle_state = tk.StringVar(value="Ready")
        ttk.Label(top, textvariable=self.toggle_state).pack(anchor="w")

        btn_row = ttk.Frame(top)
        btn_row.pack(fill=tk.X, pady=10)

        self.btn_checkin = ttk.Button(btn_row, text="Check-in", command=lambda: self._toggle("check_in"))
        self.btn_checkout = ttk.Button(btn_row, text="Check-out", command=lambda: self._toggle("check_out"))
        self.btn_checkin.pack(side=tk.LEFT, padx=6)
        self.btn_checkout.pack(side=tk.LEFT, padx=6)

        # Tree logs
        logs = ttk.LabelFrame(self, text="Recent Attendance Records", padding=14)
        logs.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("date", "check_in", "check_out", "status")
        self.tree = ttk.Treeview(logs, columns=columns, show="headings", height=10)
        for c in columns:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=160, anchor="w")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_role(self, role: str):
        self.role = role
        self.refresh()

    def refresh(self):
        if not self.app.session:
            return
        session = self.app.session

        def do():
            return self.app.api.get_recent_attendance(session, limit=15)

        def ok(records: List[Dict[str, Any]]):
            self.tree.delete(*self.tree.get_children())
            for r in records:
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        r.get("date"),
                        r.get("check_in"),
                        r.get("check_out"),
                        r.get("status"),
                    ),
                )

        def err(e: Exception):
            messagebox.showerror("Attendance Error", str(e))

        self.app.run_in_thread(do, on_success=ok, on_error=err)

    def _toggle(self, action: str):
        if not self.app.session:
            return
        session = self.app.session

        self.toggle_state.set("Updating...")

        def do():
            return self.app.api.check_in_out(session, action)

        def ok(_=None):
            self.toggle_state.set("Done. Refreshing...")
            self.refresh()
            self.toggle_state.set("Ready")

        def err(e: Exception):
            self.toggle_state.set("Ready")
            messagebox.showerror("Attendance Error", str(e))

        self.app.run_in_thread(do, on_success=ok, on_error=err)


class LeavePage(ttk.Frame):
    """Employee leave form (for Employee role). HR uses separate page."""

    def __init__(self, app: HRMSApp, parent):
        super().__init__(parent)
        self.app = app
        self.role: str = "Employee"

        self.title = ttk.Label(self, text="Leave Management", font=("Segoe UI", 18, "bold"))
        self.title.pack(anchor="w", pady=(18, 10), padx=20)

        form = ttk.LabelFrame(self, text="Apply for Leave", padding=14)
        form.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(form, text="Leave Type:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.leave_types = ["Paid", "Sick", "Unpaid"]
        self.leave_type_var = tk.StringVar(value=self.leave_types[0])
        self.leave_type_combo = ttk.Combobox(form, values=self.leave_types, textvariable=self.leave_type_var, state="readonly", width=30)
        self.leave_type_combo.grid(row=0, column=1, sticky="w", padx=6, pady=6)

        ttk.Label(form, text="Start Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="e", padx=6, pady=6)
        self.start_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.start_var, width=32).grid(row=1, column=1, sticky="w", padx=6, pady=6)

        ttk.Label(form, text="End Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="e", padx=6, pady=6)
        self.end_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.end_var, width=32).grid(row=2, column=1, sticky="w", padx=6, pady=6)

        self.btn_submit = ttk.Button(form, text="Submit", command=self._submit_leave)
        self.btn_submit.grid(row=3, column=1, sticky="e", pady=(12, 0))

        self.help = ttk.Label(self, text="For HR approval, use the Leave Approvals page.")
        self.help.pack(anchor="w", padx=20, pady=8)

    def load_role(self, role: str):
        self.role = role
        self.btn_submit.configure(state=tk.NORMAL if role == "Employee" else tk.DISABLED)

    def _submit_leave(self):
        if not self.app.session:
            return

        leave_type = self.leave_type_var.get()
        start_date = self.start_var.get().strip()
        end_date = self.end_var.get().strip()

        if not start_date or not end_date:
            messagebox.showerror("Validation", "Please enter start and end dates.")
            return

        session = self.app.session

        def do():
            return self.app.api.apply_leave(session, leave_type=leave_type, start_date=start_date, end_date=end_date)

        def ok(_=None):
            messagebox.showinfo("Submitted", "Leave request submitted for approval.")
            self.start_var.set("")
            self.end_var.set("")

        def err(e: Exception):
            messagebox.showerror("Leave Error", str(e))

        self.app.run_in_thread(do, on_success=ok, on_error=err)


class HREmployeeManagementPage(ttk.Frame):
    def __init__(self, app: HRMSApp, parent):
        super().__init__(parent)
        self.app = app
        self.role: str = "HR"

        ttk.Label(self, text="Employee Management (HR)", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(18, 10), padx=20)

        frame = ttk.LabelFrame(self, text="All Employees", padding=14)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("user_id", "name", "dept", "designation")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=16)
        for c in columns:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=160, anchor="w")

        self.tree.pack(fill=tk.BOTH, expand=True)

    def load_role(self, role: str):
        self.role = role
        self.refresh()

    def refresh(self):
        if not self.app.session:
            return
        if self.role != "HR":
            return

        session = self.app.session

        def do():
            return self.app.api.get_all_employees(session)

        def ok(employees: List[Dict[str, Any]]):
            self.tree.delete(*self.tree.get_children())
            for e in employees:
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        e.get("user_id"),
                        e.get("name"),
                        e.get("dept"),
                        e.get("designation"),
                    ),
                )

        def err(ex: Exception):
            messagebox.showerror("HR Error", str(ex))

        self.app.run_in_thread(do, on_success=ok, on_error=err)


class HRLeaveApprovalsPage(ttk.Frame):
    def __init__(self, app: HRMSApp, parent):
        super().__init__(parent)
        self.app = app
        self.role: str = "HR"
        self.selected_leave_id: Optional[int] = None

        ttk.Label(self, text="Leave Approvals (HR)", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(18, 10), padx=20)

        top = ttk.Frame(self)
        top.pack(fill=tk.X, padx=20, pady=10)

        self.btn_refresh = ttk.Button(top, text="Refresh", command=self.refresh)
        self.btn_refresh.pack(side=tk.RIGHT)

        main = ttk.LabelFrame(self, text="Pending Requests", padding=14)
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("leave_id", "employee", "leave_type", "start_date", "end_date", "status")
        self.tree = ttk.Treeview(main, columns=columns, show="headings", height=12)
        for c in columns:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140, anchor="w")

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_select)

        decide = ttk.LabelFrame(self, text="Decision", padding=14)
        decide.pack(fill=tk.X, padx=20, pady=(0, 20))

        ttk.Label(decide, text="HR Comment:").grid(row=0, column=0, sticky="e", padx=6, pady=6)
        self.comment_var = tk.StringVar()
        ttk.Entry(decide, textvariable=self.comment_var, width=60).grid(row=0, column=1, sticky="w", padx=6, pady=6)

        btns = ttk.Frame(decide)
        btns.grid(row=1, column=1, sticky="e", pady=(8, 0))

        self.btn_approve = ttk.Button(btns, text="Approve", command=lambda: self._decide("approve"))
        self.btn_reject = ttk.Button(btns, text="Reject", command=lambda: self._decide("reject"))
        self.btn_approve.pack(side=tk.LEFT, padx=6)
        self.btn_reject.pack(side=tk.LEFT, padx=6)

    def load_role(self, role: str):
        self.role = role
        # Restrict if not HR
        if role != "HR":
            self.btn_refresh.configure(state=tk.DISABLED)
            self.btn_approve.configure(state=tk.DISABLED)
            self.btn_reject.configure(state=tk.DISABLED)
        else:
            self.btn_refresh.configure(state=tk.NORMAL)

        self.refresh()

    def refresh(self):
        if not self.app.session:
            return
        if self.role != "HR":
            return

        session = self.app.session

        def do():
            return self.app.api.get_pending_leave_requests(session)

        def ok(requests: List[Dict[str, Any]]):
            self.tree.delete(*self.tree.get_children())
            self.selected_leave_id = None
            for r in requests:
                self.tree.insert(
                    "",
                    tk.END,
                    values=(
                        r.get("leave_id"),
                        r.get("user_name") or r.get("employee") or r.get("name"),
                        r.get("leave_type"),
                        r.get("start_date"),
                        r.get("end_date"),
                        r.get("status"),
                    ),
                )

        def err(e: Exception):
            messagebox.showerror("HR Error", str(e))

        self.app.run_in_thread(do, on_success=ok, on_error=err)

    def _on_select(self, _evt=None):
        sel = self.tree.selection()
        if not sel:
            self.selected_leave_id = None
            return
        values = self.tree.item(sel[0], "values")
        try:
            self.selected_leave_id = int(values[0])
        except Exception:
            self.selected_leave_id = None

    def _decide(self, action: str):
        if not self.app.session:
            return
        if self.role != "HR":
            return
        if self.selected_leave_id is None:
            messagebox.showwarning("Select", "Select a leave request first.")
            return

        comment = self.comment_var.get().strip()
        leave_id = self.selected_leave_id
        session = self.app.session

        def do():
            return self.app.api.decide_leave(session, leave_id=leave_id, action=action, comment=comment)

        def ok(_=None):
            messagebox.showinfo("Done", f"Leave {action}d successfully.")
            self.comment_var.set("")
            self.refresh()

        def err(e: Exception):
            messagebox.showerror("Decision Error", str(e))

        self.app.run_in_thread(do, on_success=ok, on_error=err)


class HRPayrollPlaceholderPage(ttk.Frame):
    def __init__(self, app: HRMSApp, parent):
        super().__init__(parent)
        self.app = app
        ttk.Label(self, text="Payroll (HR)", font=("Segoe UI", 18, "bold")).pack(anchor="w", pady=(18, 10), padx=20)
        ttk.Label(
            self,
            text="Payroll UI placeholder. Wire this to your backend payroll endpoints and salary structure update forms.",
        ).pack(anchor="w", padx=20, pady=10)

    def load_role(self, role: str):
        # nothing
        pass


# -----------------------------
# Main
# -----------------------------


def main():
    app = HRMSApp()
    # Use ttk theme defaults; can customize further.
    style = ttk.Style(app)
    try:
        style.theme_use("clam")
    except Exception:
        pass
    app.mainloop()


if __name__ == "__main__":
    main()

