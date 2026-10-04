import './StatCard.css';

interface StatCardProps {
  title: string;
  value: string;
  trend: string;
  type: 'positive' | 'negative' | 'neutral';
}

const StatCard = ({ title, value, trend, type }: StatCardProps) => {
  return (
    <div className="glass-card stat-card">
      <h4 className="stat-title">{title}</h4>
      <div className="stat-body">
        <span className="stat-value">{value}</span>
        <span className={`stat-trend trend-${type}`}>{trend}</span>
      </div>
    </div>
  );
};

export default StatCard;
