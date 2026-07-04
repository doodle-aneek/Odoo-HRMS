import { useEffect, useState } from 'react';
import { leaveService } from '../../services/leaveService';

const leaveTypes = ['Paid', 'Sick', 'Unpaid'];

export default function LeavePage() {
  const [leaves, setLeaves] = useState([]);
  const [form, setForm] = useState({ type: 'Paid', startDate: '', endDate: '', remarks: '' });

  useEffect(() => {
    leaveService.getLeaves().then(setLeaves);
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLeaves([{ id: Date.now(), ...form, status: 'Pending' }, ...leaves]);
  };

  return (
    <div className="grid">
      <div className="card">
        <h2>Leave Management</h2>
        <p className="muted">Apply for leave and review your recent requests.</p>
      </div>
      <div className="grid grid-2">
        <div className="card">
          <h3>Leave Application</h3>
          <form className="grid" onSubmit={handleSubmit}>
            <div>
              <label className="label">Leave Type</label>
              <select className="select" value={form.type} onChange={(e) => setForm({ ...form, type: e.target.value })}>
                {leaveTypes.map((type) => <option key={type} value={type}>{type}</option>)}
              </select>
            </div>
            <div className="grid grid-2">
              <div>
                <label className="label">Start Date</label>
                <input className="input" type="date" value={form.startDate} onChange={(e) => setForm({ ...form, startDate: e.target.value })} required />
              </div>
              <div>
                <label className="label">End Date</label>
                <input className="input" type="date" value={form.endDate} onChange={(e) => setForm({ ...form, endDate: e.target.value })} required />
              </div>
            </div>
            <div>
              <label className="label">Remarks</label>
              <textarea className="textarea" rows="4" value={form.remarks} onChange={(e) => setForm({ ...form, remarks: e.target.value })} />
            </div>
            <button className="btn btn-primary">Submit Request</button>
          </form>
        </div>
        <div className="card">
          <h3>Calendar View</h3>
          <p className="muted">Monthly overview with present and absent markers.</p>
          <div className="card" style={{ background: '#f8fafc', marginTop: 12 }}>
            <strong>Jul 2026</strong>
            <div className="row" style={{ marginTop: 8 }}>
              <span className="status present">P</span>
              <span className="status absent">A</span>
              <span className="status present">P</span>
              <span className="status present">P</span>
            </div>
          </div>
        </div>
      </div>
      <div className="card">
        <h3>Past Requests</h3>
        <div className="grid">
          {leaves.map((leave) => (
            <div key={leave.id} className="row" style={{ justifyContent: 'space-between' }}>
              <div>
                <strong>{leave.type}</strong>
                <div className="muted">{leave.startDate} → {leave.endDate}</div>
              </div>
              <span className={`status ${leave.status.toLowerCase()}`}>{leave.status}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
