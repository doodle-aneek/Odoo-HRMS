import { useState } from 'react';

const employees = [
  { id: 1, name: 'Asha Rao', department: 'Engineering', status: 'Active' },
  { id: 2, name: 'Kiran Das', department: 'Support', status: 'Active' },
  { id: 3, name: 'Nisha Jain', department: 'Finance', status: 'Inactive' },
];

const attendance = [
  { employee: 'Asha Rao', date: '2026-07-04', status: 'Present' },
  { employee: 'Kiran Das', date: '2026-07-04', status: 'Half-day' },
  { employee: 'Nisha Jain', date: '2026-07-04', status: 'Absent' },
];

const leaves = [
  { id: 1, employee: 'Asha Rao', type: 'Sick', status: 'Pending' },
  { id: 2, employee: 'Kiran Das', type: 'Paid', status: 'Pending' },
];

export default function AdminDashboard() {
  const [activeEmployee, setActiveEmployee] = useState(employees[0]);

  return (
    <div className="grid">
      <div className="card">
        <h2>HR Administration</h2>
        <p className="muted">Monitor staff, attendance, and leave approvals.</p>
      </div>
      <div className="grid grid-2">
        <div className="card">
          <h3>Employee List</h3>
          <div className="grid">
            {employees.map((employee) => (
              <button key={employee.id} className="btn" style={{ textAlign: 'left', background: '#f8fafc' }} onClick={() => setActiveEmployee(employee)}>
                <strong>{employee.name}</strong>
                <div className="muted">{employee.department}</div>
              </button>
            ))}
          </div>
        </div>
        <div className="card">
          <h3>Selected Employee</h3>
          <p><strong>{activeEmployee.name}</strong></p>
          <p className="muted">Department: {activeEmployee.department}</p>
          <p className="muted">Status: {activeEmployee.status}</p>
        </div>
      </div>
      <div className="grid grid-2">
        <div className="card">
          <h3>Attendance Overview</h3>
          <div className="grid">
            {attendance.map((item) => (
              <div key={item.employee + item.date} className="row" style={{ justifyContent: 'space-between' }}>
                <span>{item.employee}</span>
                <span className={`status ${item.status.toLowerCase().replace(/\s+/g, '')}`}>{item.status}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="card">
          <h3>Pending Leave Approvals</h3>
          <div className="grid">
            {leaves.map((leave) => (
              <div key={leave.id} className="row" style={{ justifyContent: 'space-between' }}>
                <div>
                  <strong>{leave.employee}</strong>
                  <div className="muted">{leave.type}</div>
                </div>
                <span className="status pending">{leave.status}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
