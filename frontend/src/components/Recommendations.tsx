const MOCK_RECOS = [
  { customer: 'CUST-8239', product: 'Industrial Servo Motor X-2', score: '0.982', lift: '+14%' },
  { customer: 'CUST-1042', product: 'Steel Fasteners 5mm', score: '0.951', lift: '+8%' },
  { customer: 'CUST-5512', product: 'Pneumatic Actuator', score: '0.910', lift: '+22%' },
  { customer: 'CUST-9921', product: 'Thermal Sensor Hub', score: '0.887', lift: '+11%' },
];

const Recommendations = () => (
  <div className="page-wrapper">
    <header className="page-header">
      <div>
        <h1>Recommendation Engine</h1>
        <p className="subtitle">Collaborative filtering product affinities</p>
      </div>
      <button className="primary-btn">Run Engine</button>
    </header>

    <div className="industrial-card table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th>TARGET CUSTOMER</th>
            <th>RECOMMENDED PRODUCT</th>
            <th>AFFINITY SCORE</th>
            <th>EXPECTED LIFT</th>
            <th>ACTION</th>
          </tr>
        </thead>
        <tbody>
          {MOCK_RECOS.map((r, i) => (
            <tr key={i}>
              <td className="mono">{r.customer}</td>
              <td>{r.product}</td>
              <td className="mono risk-low">{r.score}</td>
              <td className="mono risk-low">{r.lift}</td>
              <td><button className="action-link">Push Offer</button></td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

export default Recommendations;
