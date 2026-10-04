import './StatCard.css';

interface StatCardProps {
  title: string;
  value: string;
  trend: string;
  type: 'positive' | 'negative' | 'neutral';
}

const StatCard = ({ title, value, trend, type }: StatCardProps) => {
  return (
    <div className="industrial-card stat-card">
      <h4 className="stat-title">{title}</h4>
      <div className="stat-body">
        <span className="stat-value">{value}</span>
      </div>
      <div className="stat-footer">
        <span className={`stat-trend trend-${type}`}>{trend}</span>
        <span className="stat-period">vs last month</span>
      </div>
    </div>
  );
};

export default StatCard;
