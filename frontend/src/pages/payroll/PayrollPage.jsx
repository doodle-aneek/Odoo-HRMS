const payrolls = [
  { employee: 'Asha Rao', salary: '₹1,20,000', payslip: 'June Payslip.pdf' },
  { employee: 'Kiran Das', salary: '₹85,000', payslip: 'June Payslip.pdf' },
];

export default function PayrollPage() {
  return (
    <div className="grid">
      <div className="card">
        <h2>Payroll</h2>
        <p className="muted">View salary structures and payslips.</p>
      </div>
      <div className="grid grid-2">
        <div className="card">
          <h3>Current Salary Structure</h3>
          <p><strong>Base Salary:</strong> ₹1,00,000</p>
          <p><strong>Allowances:</strong> ₹20,000</p>
          <p><strong>Deductions:</strong> ₹0</p>
        </div>
        <div className="card">
          <h3>Payslips</h3>
          <ul>
            {payrolls.map((item) => (
              <li key={item.employee}>{item.employee} — {item.payslip}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
