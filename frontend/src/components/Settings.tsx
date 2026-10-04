import { useState } from 'react';
import './Settings.css';

const Settings = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState<string>('');
  const [isUploading, setIsUploading] = useState<boolean>(false);

  const handleUpload = async () => {
    if (!file) {
      setUploadStatus('Lütfen önce bir CSV veri seti seçin!');
      return;
    }
    
    setIsUploading(true);
    setUploadStatus('Veri seti yükleniyor ve model yeni kalıpları ezberliyor (Öğrenme Aşaması)...');
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
      const res = await fetch('http://localhost:8000/upload-dataset', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      setUploadStatus(data.message || 'Model başarıyla eğitildi ve veritabanı güncellendi!');
    } catch (err) {
      console.error(err);
      setUploadStatus('Hata: Model eğitimi başarısız oldu.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="page-wrapper">
      <header className="page-header">
        <div>
          <h1>Sistem Yapılandırması</h1>
          <p className="subtitle">Platform ayarları, veri yükleme ve API entegrasyonları</p>
        </div>
      </header>

      <div className="settings-grid">
        <div className="industrial-card" style={{gridColumn: '1 / -1', borderColor: 'var(--primary-color)'}}>
          <h3>Yapay Zeka Modeli Eğitimi (Veri Seti Yükle)</h3>
          <p className="subtitle" style={{marginBottom: '1rem'}}>
            Kendi veri setinizi yükleyin. Sistem veriyi okuyacak, analiz edecek ve özellikleri öğrenip veritabanını güncelleyecektir.
          </p>
          <div className="form-group" style={{display: 'flex', gap: '1rem', alignItems: 'center'}}>
            <input 
              type="file" 
              accept=".csv"
              onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
              className="industrial-input mono"
              style={{flex: 1}}
            />
            <button 
              className="primary-btn" 
              onClick={handleUpload} 
              disabled={isUploading}
              style={{padding: '0.75rem 1.5rem'}}
            >
              {isUploading ? 'Eğitiliyor...' : 'Yükle & Öğren'}
            </button>
          </div>
          {uploadStatus && (
            <p className="mono" style={{marginTop: '1rem', color: isUploading ? 'var(--warning-color)' : 'var(--success-color)'}}>
              &gt;_ {uploadStatus}
            </p>
          )}
        </div>

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
