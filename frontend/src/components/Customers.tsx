import { useState } from 'react';
import './Customers.css';

const MOCK_CUSTOMERS = [
  { id: 'CUST-8239', name: 'Acme Corp', clv: '$12,450', churnRisk: 'Düşük', status: 'Aktif' },
  { id: 'CUST-1042', name: 'Global Tech', clv: '$8,200', churnRisk: 'Yüksek', status: 'Riskli' },
  { id: 'CUST-5512', name: 'Nexus Industries', clv: '$45,100', churnRisk: 'Orta', status: 'Aktif' },
  { id: 'CUST-9921', name: 'Stark Logistics', clv: '$1,150', churnRisk: 'Yüksek', status: 'Kaybedildi' },
  { id: 'CUST-3310', name: 'Wayne Enterprises', clv: '$88,300', churnRisk: 'Düşük', status: 'Aktif' },
];

const Customers = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [riskFilter, setRiskFilter] = useState('Hepsi');

  const filteredCustomers = MOCK_CUSTOMERS.filter(c => {
    const matchesSearch = c.name.toLowerCase().includes(searchTerm.toLowerCase()) || c.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesRisk = riskFilter === 'Hepsi' || c.churnRisk === riskFilter;
    return matchesSearch && matchesRisk;
  });

  return (
    <div className="page-wrapper">
      <header className="page-header">
        <div>
          <h1>Müşteri Rehberi</h1>
          <p className="subtitle">Detaylı profiller ve öngörüsel metrikler</p>
        </div>
        <button className="primary-btn">Veriyi Dışa Aktar</button>
      </header>

      <div className="filters-bar">
        <input 
          type="text" 
          className="search-input mono" 
          placeholder="Müşteri ID veya İsim ile ara..." 
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <select 
          className="filter-select mono" 
          value={riskFilter}
          onChange={(e) => setRiskFilter(e.target.value)}
        >
          <option value="Hepsi">Tüm Risk Seviyeleri</option>
          <option value="Düşük">Düşük Risk</option>
          <option value="Orta">Orta Risk</option>
          <option value="Yüksek">Yüksek Risk</option>
        </select>
      </div>

      <div className="industrial-card table-container">
        <table className="data-table">
          <thead>
            <tr>
              <th>MÜŞTERİ ID</th>
              <th>ŞİRKET / İSİM</th>
              <th>ÖNGÖRÜLEN LBD</th>
              <th>KAYIP RİSKİ</th>
              <th>DURUM</th>
              <th>İŞLEMLER</th>
            </tr>
          </thead>
          <tbody>
            {filteredCustomers.length === 0 ? (
              <tr>
                <td colSpan={6} style={{textAlign: 'center', padding: '2rem', color: 'var(--text-muted)'}}>Sonuç bulunamadı.</td>
              </tr>
            ) : filteredCustomers.map(c => {
              const riskClass = c.churnRisk === 'Düşük' ? 'risk-low' : (c.churnRisk === 'Orta' ? 'risk-medium' : 'risk-high');
              return (
                <tr key={c.id}>
                  <td className="mono">{c.id}</td>
                  <td>{c.name}</td>
                  <td className="mono">{c.clv}</td>
                  <td>
                    <span className={`risk-badge ${riskClass}`}>{c.churnRisk}</span>
                  </td>
                  <td>{c.status}</td>
                  <td><button className="action-link">Profili Gör</button></td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Customers;
