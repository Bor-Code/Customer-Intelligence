import StatCard from './StatCard';
import './Dashboard.css';

const Dashboard = () => {
  return (
    <div className="dashboard-wrapper">
      <header className="dashboard-header">
        <div>
          <h1>Customer Intelligence</h1>
          <p className="subtitle">Real-time insights and predictive analytics</p>
        </div>
      </header>

      <section className="grid-cards">
        <StatCard title="Total Customers" value="24,592" trend="+12%" type="positive" />
        <StatCard title="At-Risk (Churn)" value="1,240" trend="-3%" type="positive" />
        <StatCard title="Avg CLV" value="$1,840" trend="+5%" type="positive" />
        <StatCard title="Active Segments" value="6" trend="Stable" type="neutral" />
      </section>

      <section className="main-widgets">
        <div className="glass-card chart-widget">
          <h3>Revenue Forecast (30 Days)</h3>
          <div className="placeholder-chart">
            <div className="chart-line"></div>
          </div>
        </div>

        <div className="glass-card recommendations-widget">
          <h3>Top Product Recommendations</h3>
          <ul className="reco-list">
            <li><span>Premium Wireless Headphones</span> <span className="score">98% Match</span></li>
            <li><span>Ergonomic Office Chair</span> <span className="score">92% Match</span></li>
            <li><span>Mechanical Keyboard</span> <span className="score">85% Match</span></li>
          </ul>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
