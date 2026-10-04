import './Segments.css';

const Segments = () => (
  <div className="page-wrapper">
    <header className="page-header">
      <div>
        <h1>Davranışsal Segmentler</h1>
        <p className="subtitle">RFM Kümeleme Analizi (Yenilik, Sıklık, Parasal Değer)</p>
      </div>
    </header>

    <div className="segments-grid">
      <div className="industrial-card segment-card">
        <h3 className="segment-title">Şampiyonlar</h3>
        <p className="segment-desc">Yakın zamanda alışveriş yaptılar, sık alırlar ve en çok harcarlar.</p>
        <div className="segment-metrics">
          <div className="metric-box">
            <span className="metric-lbl">KULLANICILAR</span>
            <span className="metric-val mono">1,240</span>
          </div>
          <div className="metric-box">
            <span className="metric-lbl">ORT. HARCAMA</span>
            <span className="metric-val mono">$4,500</span>
          </div>
        </div>
      </div>
      
      <div className="industrial-card segment-card">
        <h3 className="segment-title">Sadık Müşteriler</h3>
        <p className="segment-desc">Sık sık yüksek harcama yaparlar. Kampanyalara duyarlıdırlar.</p>
        <div className="segment-metrics">
          <div className="metric-box">
            <span className="metric-lbl">KULLANICILAR</span>
            <span className="metric-val mono">4,592</span>
          </div>
          <div className="metric-box">
            <span className="metric-lbl">ORT. HARCAMA</span>
            <span className="metric-val mono">$1,200</span>
          </div>
        </div>
      </div>

      <div className="industrial-card segment-card">
        <h3 className="segment-title">Risk Altında</h3>
        <p className="segment-desc">Önceden yüksek harcama yaptılar ama uzun süredir aktif değiller.</p>
        <div className="segment-metrics">
          <div className="metric-box">
            <span className="metric-lbl">KULLANICILAR</span>
            <span className="metric-val mono">890</span>
          </div>
          <div className="metric-box">
            <span className="metric-lbl">ORT. HARCAMA</span>
            <span className="metric-val mono">$2,100</span>
          </div>
        </div>
      </div>
    </div>
  </div>
);

export default Segments;
