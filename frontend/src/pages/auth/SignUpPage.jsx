import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export default function SignUpPage() {
  const navigate = useNavigate();
  const { signup } = useAuth();
  const [form, setForm] = useState({ employeeId: '', email: '', password: '', role: 'employee' });
  const [message, setMessage] = useState('');

  const validatePassword = (password) => password.length >= 8 && /[A-Z]/.test(password) && /[0-9]/.test(password);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!validatePassword(form.password)) {
      setMessage('Password must be at least 8 characters with one uppercase and one number.');
      return;
    }

    signup(form);
    setMessage('Verification email sent. Please verify your email to continue.');
    navigate('/dashboard');
  };

  return (
    <div className="container" style={{ maxWidth: 520, marginTop: 48 }}>
      <div className="card">
        <h2>Create Account</h2>
        <p className="muted">Register as an employee or HR officer</p>
        <form onSubmit={handleSubmit} className="grid">
          <div>
            <label className="label">Employee ID</label>
            <input className="input" value={form.employeeId} onChange={(e) => setForm({ ...form, employeeId: e.target.value })} required />
          </div>
          <div>
            <label className="label">Email</label>
            <input className="input" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
          </div>
          <div>
            <label className="label">Password</label>
            <input className="input" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required />
          </div>
          <div>
            <label className="label">Role</label>
            <select className="select" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
              <option value="employee">Employee</option>
              <option value="hr">HR</option>
            </select>
          </div>
          {message && <div className="status pending">{message}</div>}
          <button className="btn btn-primary">Sign Up</button>
        </form>
        <p style={{ marginTop: 12 }}>
          Already registered? <Link to="/signin">Sign in</Link>
        </p>
      </div>
    </div>
  );
}
