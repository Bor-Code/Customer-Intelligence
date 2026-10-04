import './Settings.css';

const Settings = () => {
  return (
    <div className="page-wrapper">
      <header className="page-header">
        <div>
          <h1>Sistem Yapılandırması</h1>
          <p className="subtitle">Platform ayarları ve API entegrasyonları</p>
        </div>
      </header>

      <div className="settings-grid">
        <div className="industrial-card">
          <h3>Model Uç Noktaları</h3>
          <div className="form-group">
            <label>FASTAPI TEMEL URL</label>
            <input type="text" className="industrial-input mono" defaultValue="http://localhost:8000" />
          </div>
          <div className="form-group">
            <label>MLFLOW İZLEME URI</label>
            <input type="text" className="industrial-input mono" defaultValue="http://localhost:5000" />
          </div>
        </div>

        <div className="industrial-card">
          <h3>Kafka Akış Ayarları</h3>
          <div className="form-group">
            <label>KAFKA BROKER'LARI</label>
            <input type="text" className="industrial-input mono" defaultValue="localhost:9092" />
          </div>
          <div className="form-group">
            <label>TÜKETİCİ GRUP ID</label>
            <input type="text" className="industrial-input mono" defaultValue="ci-analytics-group" />
          </div>
        </div>

        <div className="industrial-card">
          <h3>Özellik Deposu (DuckDB)</h3>
          <div className="form-group">
            <label>GÜMÜŞ KATMAN DB YOLU</label>
            <input type="text" className="industrial-input mono" defaultValue="data/silver/customers.db" />
          </div>
          <div className="form-group">
            <label>ALTIN KATMAN DB YOLU</label>
            <input type="text" className="industrial-input mono" defaultValue="data/gold/features.db" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
