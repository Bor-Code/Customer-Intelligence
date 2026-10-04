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
        <p className="label mono">Gün {label}</p>
        <p className="value mono">${payload[0].value}</p>
      </div>
    );
  }
  return null;
};

const Dashboard = () => {
  const [stats, setStats] = useState<Stats | null>(null);
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
      // Refresh stats after successful upload
      fetch('http://localhost:8000/stats')
        .then(r => r.json())
        .then(d => setStats(d));
    } catch (err) {
      console.error(err);
      setUploadStatus('Hata: Model eğitimi başarısız oldu.');
    } finally {
      setIsUploading(false);
    }
  };

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
          <h1>Sistem Genel Bakış</h1>
          <p className="subtitle">Gerçek zamanlı metrikler ve öngörüsel göstergeler</p>
        </div>
      </header>

      <div className="industrial-card" style={{marginTop: '2rem', borderColor: 'var(--primary-color)'}}>
        <h3>Yapay Zeka Modeli Eğitimi (Veri Seti Yükle)</h3>
        <p className="subtitle" style={{marginBottom: '1rem'}}>
          Kendi veri setinizi yükleyin. Sistem veriyi okuyacak, analiz edecek ve özellikleri öğrenip analizleri güncelleyecektir.
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

      <section className="grid-cards">
        <StatCard title="TOPLAM MÜŞTERİ" value={stats?.total_customers || "---"} trend="+12.4%" type="positive" />
        <StatCard title="RİSKLİ (KAYIP)" value={stats?.at_risk_churn || "---"} trend="-3.2%" type="positive" />
        <StatCard title="ORT. MÜŞTERİ DEĞERİ" value={stats?.avg_clv || "---"} trend="+5.1%" type="positive" />
        <StatCard title="AKTİF SEGMENTLER" value={stats?.active_segments || "---"} trend="Sabit" type="neutral" />
      </section>

      <section className="main-widgets">
        <div className="industrial-card chart-widget">
          <h3>Gelir Tahmini (30 Gün)</h3>
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
          <h3>Öne Çıkan Tavsiyeler</h3>
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
