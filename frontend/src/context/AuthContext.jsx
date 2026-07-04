import { createContext, useContext, useMemo, useState } from 'react';

const AuthContext = createContext();

// Mock authentication state that can later be replaced with real API calls.
const initialUser = {
  id: 'EMP-1001',
  name: 'Asha Rao',
  email: 'asha@example.com',
  role: 'employee',
};

export function AuthProvider({ children }) {
  const [user, setUser] = useState(initialUser);
  const [isAuthenticated, setIsAuthenticated] = useState(true);

  const login = (email, password, role) => {
    if (!email || !password) {
      throw new Error('Please enter your email and password.');
    }

    setUser({
      id: role === 'admin' ? 'HR-001' : 'EMP-1001',
      name: role === 'admin' ? 'Mina Patel' : 'Asha Rao',
      email,
      role: role === 'admin' ? 'admin' : 'employee',
    });
    setIsAuthenticated(true);
  };

  const signup = (payload) => {
    setUser({
      id: payload.employeeId,
      name: payload.email.split('@')[0],
      email: payload.email,
      role: payload.role === 'hr' ? 'admin' : 'employee',
    });
    setIsAuthenticated(true);
  };

  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
  };

  const value = useMemo(() => ({ user, isAuthenticated, login, signup, logout }), [user, isAuthenticated]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
