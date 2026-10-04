import { useEffect, useState } from 'react';
import StatCard from './StatCard';
import './Dashboard.css';

interface Stats {
  total_customers: string;
  at_risk_churn: string;
  avg_clv: string;
  active_segments: string;
}

const Dashboard = () => {
  const [stats, setStats] = useState<Stats | null>(null);

  useEffect(() => {
    fetch('http://localhost:8000/stats')
      .then(res => res.json())
      .then(data => setStats(data))
      .catch(err => console.error("API Fetch Error:", err));
  }, []);

  return (
    <div className="dashboard-wrapper">
      <header className="dashboard-header">
        <div>
          <h1>System Overview</h1>
          <p className="subtitle">Real-time metrics and predictive indicators</p>
        </div>
      </header>

      <section className="grid-cards">
        <StatCard title="TOTAL CUSTOMERS" value={stats?.total_customers || "---"} trend="+12.4%" type="positive" />
        <StatCard title="AT-RISK (CHURN)" value={stats?.at_risk_churn || "---"} trend="-3.2%" type="positive" />
        <StatCard title="AVERAGE CLV" value={stats?.avg_clv || "---"} trend="+5.1%" type="positive" />
        <StatCard title="ACTIVE SEGMENTS" value={stats?.active_segments || "---"} trend="Stable" type="neutral" />
      </section>

      <section className="main-widgets">
        <div className="industrial-card chart-widget">
          <h3>Revenue Forecast (30D)</h3>
          <div className="placeholder-chart">
            <div className="chart-grid"></div>
            <div className="chart-line"></div>
          </div>
        </div>

        <div className="industrial-card recommendations-widget">
          <h3>Top Recommendations</h3>
          <ul className="reco-list">
            <li>
              <span className="item-name">Wireless Headphones</span>
              <span className="score">0.98</span>
            </li>
            <li>
              <span className="item-name">Ergonomic Chair</span>
              <span className="score">0.92</span>
            </li>
            <li>
              <span className="item-name">Mechanical Keyboard</span>
              <span className="score">0.85</span>
            </li>
          </ul>
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
