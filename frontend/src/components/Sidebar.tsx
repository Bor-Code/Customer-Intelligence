import { NavLink } from 'react-router-dom';
import './Sidebar.css';

const Sidebar = () => {
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
    </aside>
  );
};

export default Sidebar;
