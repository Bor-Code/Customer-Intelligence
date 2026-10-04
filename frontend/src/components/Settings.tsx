import './Settings.css';

const Settings = () => (
  <div className="page-wrapper">
    <header className="page-header">
      <div>
        <h1>System Configuration</h1>
        <p className="subtitle">Platform settings, API integrations and environment variables</p>
      </div>
      <button className="primary-btn">Save Changes</button>
    </header>

    <div className="settings-grid">
      <div className="industrial-card">
        <h3>Model Endpoints</h3>
        <div className="form-group">
          <label>FASTAPI BASE URL</label>
          <input type="text" className="industrial-input mono" defaultValue="http://localhost:8000" />
        </div>
        <div className="form-group">
          <label>MLFLOW TRACKING URI</label>
          <input type="text" className="industrial-input mono" defaultValue="http://localhost:5000" />
        </div>
      </div>

      <div className="industrial-card">
        <h3>Kafka Stream Settings</h3>
        <div className="form-group">
          <label>KAFKA BROKERS</label>
          <input type="text" className="industrial-input mono" defaultValue="localhost:9092" />
        </div>
        <div className="form-group">
          <label>CONSUMER GROUP ID</label>
          <input type="text" className="industrial-input mono" defaultValue="ci-analytics-group" />
        </div>
      </div>

      <div className="industrial-card">
        <h3>Feature Store (DuckDB)</h3>
        <div className="form-group">
          <label>SILVER LAYER DB PATH</label>
          <input type="text" className="industrial-input mono" defaultValue="data/silver/customers.db" />
        </div>
        <div className="form-group">
          <label>GOLD LAYER DB PATH</label>
          <input type="text" className="industrial-input mono" defaultValue="data/gold/features.db" />
        </div>
      </div>
    </div>
  </div>
);

export default Settings;
