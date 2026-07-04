export const authService = {
  async login(credentials) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (credentials.email === 'admin@example.com' && credentials.password === 'admin123') {
          resolve({ success: true, user: { id: 'HR-001', name: 'Mina Patel', email: credentials.email, role: 'admin' } });
          return;
        }
        if (credentials.email === 'employee@example.com' && credentials.password === 'employee123') {
          resolve({ success: true, user: { id: 'EMP-1001', name: 'Asha Rao', email: credentials.email, role: 'employee' } });
          return;
        }
        reject(new Error('Invalid credentials'));
      }, 300);
    });
  },

  async signup(payload) {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ success: true, user: { id: payload.employeeId, email: payload.email, role: payload.role === 'hr' ? 'admin' : 'employee' } });
      }, 300);
    });
  },
};
