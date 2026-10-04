import './Customers.css';

const MOCK_CUSTOMERS = [
  { id: 'CUST-8239', name: 'Acme Corp', clv: '$12,450', churnRisk: 'Low', status: 'Active' },
  { id: 'CUST-1042', name: 'Global Tech', clv: '$8,200', churnRisk: 'High', status: 'At Risk' },
  { id: 'CUST-5512', name: 'Nexus Industries', clv: '$45,100', churnRisk: 'Medium', status: 'Active' },
  { id: 'CUST-9921', name: 'Stark Logistics', clv: '$1,150', churnRisk: 'High', status: 'Churned' },
  { id: 'CUST-3310', name: 'Wayne Enterprises', clv: '$88,300', churnRisk: 'Low', status: 'Active' },
];

const Customers = () => (
  <div className="page-wrapper">
    <header className="page-header">
      <div>
        <h1>Customer Directory</h1>
        <p className="subtitle">Detailed profiles and predictive metrics</p>
      </div>
      <button className="primary-btn">Export Data</button>
    </header>

    <div className="industrial-card table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th>CUSTOMER ID</th>
            <th>COMPANY / NAME</th>
            <th>PREDICTED CLV</th>
            <th>CHURN RISK</th>
            <th>STATUS</th>
            <th>ACTIONS</th>
          </tr>
        </thead>
        <tbody>
          {MOCK_CUSTOMERS.map(c => (
            <tr key={c.id}>
              <td className="mono">{c.id}</td>
              <td>{c.name}</td>
              <td className="mono">{c.clv}</td>
              <td>
                <span className={`risk-badge risk-${c.churnRisk.toLowerCase()}`}>{c.churnRisk}</span>
              </td>
              <td>{c.status}</td>
              <td><button className="action-link">View Profile</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

export default Customers;
