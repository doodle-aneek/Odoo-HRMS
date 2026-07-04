import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';

// Role-based routing shell for the HRMS frontend.
import SignInPage from './pages/auth/SignInPage';
import SignUpPage from './pages/auth/SignUpPage';
import EmployeeDashboard from './pages/dashboard/EmployeeDashboard';
import AdminDashboard from './pages/dashboard/AdminDashboard';
import ProfilePage from './pages/profile/ProfilePage';
import AttendancePage from './pages/attendance/AttendancePage';
import LeavePage from './pages/leaves/LeavePage';
import PayrollPage from './pages/payroll/PayrollPage';
import Layout from './components/Layout';

function ProtectedRoute({ children, requiredRole }) {
  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/signin" replace />;
  }

  if (requiredRole && user?.role !== requiredRole) {
    return <Navigate to="/dashboard" replace />;
  }

  return <Layout>{children}</Layout>;
}

function AppRoutes() {
  const { user, isAuthenticated } = useAuth();

  return (
    <Routes>
      <Route path="/signin" element={<SignInPage />} />
      <Route path="/signup" element={<SignUpPage />} />
      <Route
        path="/dashboard"
        element={
          isAuthenticated ? (
            user?.role === 'admin' ? <Navigate to="/admin-dashboard" replace /> : <Navigate to="/employee-dashboard" replace />
          ) : (
            <Navigate to="/signin" replace />
          )
        }
      />
      <Route
        path="/employee-dashboard"
        element={
          <ProtectedRoute>
            <EmployeeDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/admin-dashboard"
        element={
          <ProtectedRoute requiredRole="admin">
            <AdminDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <ProfilePage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/attendance"
        element={
          <ProtectedRoute>
            <AttendancePage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/leave"
        element={
          <ProtectedRoute>
            <LeavePage />
          </ProtectedRoute>
        }
      />
      <Route
        path="/payroll"
        element={
          <ProtectedRoute>
            <PayrollPage />
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/signin" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}
