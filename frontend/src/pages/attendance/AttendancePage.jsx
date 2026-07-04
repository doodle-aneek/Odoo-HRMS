import { useState } from 'react';

const attendanceRecords = [
  { date: '2026-07-01', status: 'Present' },
  { date: '2026-07-02', status: 'Absent' },
  { date: '2026-07-03', status: 'Half-day' },
  { date: '2026-07-04', status: 'Present' },
];

export default function AttendancePage() {
  const [checkedIn, setCheckedIn] = useState(false);

  return (
    <div className="grid">
      <div className="card">
        <div className="row" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2>Attendance</h2>
            <p className="muted">Manage daily check-ins and view attendance history.</p>
          </div>
          <button className={`btn ${checkedIn ? 'btn-danger' : 'btn-success'}`} onClick={() => setCheckedIn((v) => !v)}>
            {checkedIn ? 'Check Out' : 'Check In'}
          </button>
        </div>
      </div>
      <div className="card">
        <h3>Recent Records</h3>
        <div className="grid">
          {attendanceRecords.map((record) => (
            <div key={record.date} className="row" style={{ justifyContent: 'space-between' }}>
              <span>{record.date}</span>
              <span className={`status ${record.status.toLowerCase().replace(/\s+/g, '')}`}>{record.status}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
