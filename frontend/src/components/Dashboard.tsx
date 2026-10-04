import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import StatCard from './StatCard';
import './Dashboard.css';

interface Stats {
  total_customers: string;
  at_risk_churn: string;
  avg_clv: string;
  active_segments: string;
}

const MOCK_FORECAST_DATA = [
  { day: '01', revenue: 4000 },
  { day: '05', revenue: 3000 },
  { day: '10', revenue: 5500 },
  { day: '15', revenue: 4500 },
  { day: '20', revenue: 6000 },
  { day: '25', revenue: 7200 },
  { day: '30', revenue: 8500 },
];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip">
        <p className="label mono">Day {label}</p>
        <p className="value mono">${payload[0].value}</p>
      </div>
    );
  }
  return null;
};

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
          <div className="recharts-wrapper">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={MOCK_FORECAST_DATA} margin={{ top: 20, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                <XAxis dataKey="day" stroke="#a1a1aa" tick={{fill: '#a1a1aa', fontSize: 12, fontFamily: 'var(--font-mono)'}} />
                <YAxis stroke="#a1a1aa" tick={{fill: '#a1a1aa', fontSize: 12, fontFamily: 'var(--font-mono)'}} />
                <Tooltip content={<CustomTooltip />} />
                <Line type="monotone" dataKey="revenue" stroke="#fafafa" strokeWidth={2} dot={{ fill: '#fafafa', r: 4 }} activeDot={{ r: 6, fill: '#10b981' }} />
              </LineChart>
            </ResponsiveContainer>
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
