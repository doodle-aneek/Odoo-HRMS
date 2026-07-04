import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export default function SignInPage() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [form, setForm] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      login(form.email, form.password, form.role || 'employee');
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ maxWidth: 480, marginTop: 48 }}>
      <div className="card">
        <h2>Sign In</h2>
        <p className="muted">Access your HRMS workspace</p>
        <form onSubmit={handleSubmit} className="grid">
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
            <select className="select" value={form.role || 'employee'} onChange={(e) => setForm({ ...form, role: e.target.value })}>
              <option value="employee">Employee</option>
              <option value="admin">HR Officer</option>
            </select>
          </div>
          {error && <div className="status rejected">{error}</div>}
          <button className="btn btn-primary" disabled={loading}>{loading ? 'Signing in…' : 'Sign In'}</button>
        </form>
        <p style={{ marginTop: 12 }}>
          Don’t have an account? <Link to="/signup">Create one</Link>
        </p>
      </div>
    </div>
  );
}
