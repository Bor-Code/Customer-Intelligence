import './Segments.css';

const Segments = () => (
  <div className="page-wrapper">
    <header className="page-header">
      <div>
        <h1>Behavioral Segments</h1>
        <p className="subtitle">RFM Clustering Analysis (Recency, Frequency, Monetary)</p>
      </div>
    </header>

    <div className="segments-grid">
      <div className="industrial-card segment-card">
        <h3 className="segment-title">Champions</h3>
        <p className="segment-desc">Bought recently, buy often, and spend the most.</p>
        <div className="segment-metrics">
          <div className="metric-box">
            <span className="metric-lbl">USERS</span>
            <span className="metric-val mono">1,240</span>
          </div>
          <div className="metric-box">
            <span className="metric-lbl">AVG SPEND</span>
            <span className="metric-val mono">$4,500</span>
          </div>
        </div>
      </div>
      
      <div className="industrial-card segment-card">
        <h3 className="segment-title">Loyal Customers</h3>
        <p className="segment-desc">Spend good money with us often. Responsive to promotions.</p>
        <div className="segment-metrics">
          <div className="metric-box">
            <span className="metric-lbl">USERS</span>
            <span className="metric-val mono">4,592</span>
          </div>
          <div className="metric-box">
            <span className="metric-lbl">AVG SPEND</span>
            <span className="metric-val mono">$1,200</span>
          </div>
        </div>
      </div>

      <div className="industrial-card segment-card">
        <h3 className="segment-title">At Risk</h3>
        <p className="segment-desc">Spent big money and purchased often. But long time ago.</p>
        <div className="segment-metrics">
          <div className="metric-box">
            <span className="metric-lbl">USERS</span>
            <span className="metric-val mono">890</span>
          </div>
          <div className="metric-box">
            <span className="metric-lbl">AVG SPEND</span>
            <span className="metric-val mono">$2,100</span>
          </div>
        </div>
      </div>
    </div>
  </div>
);

export default Segments;
