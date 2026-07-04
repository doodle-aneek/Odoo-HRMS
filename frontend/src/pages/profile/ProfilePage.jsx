import { useState } from 'react';
import { useAuth } from '../../context/AuthContext';

const profile = {
  name: 'Asha Rao',
  employeeId: 'EMP-1001',
  email: 'asha@example.com',
  phone: '+91 9876543210',
  address: 'Bengaluru, Karnataka',
  jobTitle: 'Software Engineer',
  salary: '₹1,20,000/month',
  documents: ['Offer Letter.pdf', 'ID Proof.pdf'],
};

export default function ProfilePage() {
  const { user } = useAuth();
  const [editMode, setEditMode] = useState(false);
  const [form, setForm] = useState(profile);

  const handleSave = () => {
    setEditMode(false);
  };

  return (
    <div className="grid">
      <div className="card">
        <div className="row" style={{ justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2>Employee Profile</h2>
            <p className="muted">{user?.role === 'admin' ? 'Admin view with full edit access' : 'Editable fields limited to contact details'}</p>
          </div>
          <button className="btn btn-primary" onClick={() => setEditMode((v) => !v)}>{editMode ? 'Cancel' : 'Edit'}</button>
        </div>
      </div>
      <div className="grid grid-2">
        <div className="card">
          <h3>Personal Details</h3>
          <p><strong>Name:</strong> {form.name}</p>
          <p><strong>Employee ID:</strong> {form.employeeId}</p>
          <p><strong>Email:</strong> {form.email}</p>
          {editMode ? (
            <>
              <label className="label">Phone</label>
              <input className="input" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
              <label className="label">Address</label>
              <input className="input" value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} />
            </>
          ) : (
            <>
              <p><strong>Phone:</strong> {form.phone}</p>
              <p><strong>Address:</strong> {form.address}</p>
            </>
          )}
          {editMode && <button className="btn btn-success" style={{ marginTop: 12 }} onClick={handleSave}>Save Changes</button>}
        </div>
        <div className="card">
          <h3>Job Details</h3>
          <p><strong>Role:</strong> {form.jobTitle}</p>
          <p><strong>Salary:</strong> {form.salary}</p>
          <p><strong>Documents:</strong> {form.documents.join(', ')}</p>
          {user?.role === 'admin' && editMode && (
            <div>
              <label className="label">Job Title</label>
              <input className="input" value={form.jobTitle} onChange={(e) => setForm({ ...form, jobTitle: e.target.value })} />
              <label className="label">Salary</label>
              <input className="input" value={form.salary} onChange={(e) => setForm({ ...form, salary: e.target.value })} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
