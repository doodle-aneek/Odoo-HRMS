import { Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const quickLinks = [
  { title: 'Profile', path: '/profile', description: 'View or update your profile details' },
  { title: 'Attendance', path: '/attendance', description: 'Track your daily check-ins and attendance' },
  { title: 'Leave Requests', path: '/leave', description: 'Apply for time off and monitor requests' },
];

export default function EmployeeDashboard() {
  const { user } = useAuth();

  return (
    <div className="grid">
      <div className="card">
        <h2>Welcome back, {user?.name}</h2>
        <p className="muted">Here’s a quick summary of your HRMS workspace.</p>
      </div>
      <div className="grid grid-3">
        {quickLinks.map((link) => (
          <Link key={link.title} to={link.path} className="card">
            <h3>{link.title}</h3>
            <p className="muted">{link.description}</p>
          </Link>
        ))}
      </div>
      <div className="card">
        <h3>Recent Activity</h3>
        <ul>
          <li>Leave request submitted for Jul 10–12</li>
          <li>Attendance marked for today</li>
          <li>Profile picture updated successfully</li>
        </ul>
      </div>
    </div>
  );
}
