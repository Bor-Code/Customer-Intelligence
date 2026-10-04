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
        <NavLink to="/" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>Dashboard</NavLink>
        <NavLink to="/customers" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>Customers</NavLink>
        <NavLink to="/segments" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>Segments</NavLink>
        <NavLink to="/recommendations" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>Recommendations</NavLink>
        <NavLink to="/raw-data" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>Raw Data</NavLink>
        <NavLink to="/settings" className={({isActive}) => isActive ? "nav-item active" : "nav-item"}>Settings</NavLink>
      </nav>
    </aside>
  );
};

export default Sidebar;
