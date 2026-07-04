import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/signin');
  };

  return (
    <div>
      <nav>
        <div className="container">
          <strong>HRMS Portal</strong>
          <div className="sidebar">
            {user?.role === 'admin' ? (
              <>
                <NavLink to="/admin-dashboard">Overview</NavLink>
                <NavLink to="/profile">Profiles</NavLink>
                <NavLink to="/attendance">Attendance</NavLink>
                <NavLink to="/leave">Leaves</NavLink>
                <NavLink to="/payroll">Payroll</NavLink>
              </>
            ) : (
              <>
                <NavLink to="/employee-dashboard">Dashboard</NavLink>
                <NavLink to="/profile">Profile</NavLink>
                <NavLink to="/attendance">Attendance</NavLink>
                <NavLink to="/leave">Leave</NavLink>
                <NavLink to="/payroll">Payroll</NavLink>
              </>
            )}
          </div>
          <button className="btn btn-danger" onClick={handleLogout}>Logout</button>
        </div>
      </nav>
      <main className="container">{children}</main>
    </div>
  );
}
