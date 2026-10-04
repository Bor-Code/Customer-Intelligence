import { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
  const [theme, setTheme] = useState('dark');

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);

  return (
    <aside className="sidebar industrial-panel">
      <div className="logo-container">
        <div className="logo-icon"></div>
        <h2>RETAIL AI</h2>
      </div>
      <nav className="nav-menu">
        <NavLink to="/" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>Özet</NavLink>
        <NavLink to="/customers" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>Müşteriler</NavLink>
        <NavLink to="/segments" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>Segmentler</NavLink>
        <NavLink to="/recommendations" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>Tavsiyeler</NavLink>
        <NavLink to="/raw-data" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>Ham Veri</NavLink>
        <NavLink to="/settings" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>Ayarlar</NavLink>
      </nav>

      <div className="theme-switcher">
        <label className="theme-lbl">TEMA SEÇİMİ</label>
        <select 
          className="theme-select mono" 
          value={theme}
          onChange={(e) => setTheme(e.target.value)}
        >
          <option value="dark">Karanlık (Endüstriyel)</option>
          <option value="light">Aydınlık (Kurumsal)</option>
          <option value="cyberpunk">Cyberpunk (Neon)</option>
        </select>
      </div>
    </aside>
  );
};

export default Sidebar;
