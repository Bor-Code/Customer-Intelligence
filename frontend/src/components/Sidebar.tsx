import './Sidebar.css';

const Sidebar = () => {
  return (
    <aside className="sidebar industrial-panel">
      <div className="logo-container">
        <div className="logo-icon"></div>
        <h2>RETAIL AI</h2>
      </div>
      <nav className="nav-menu">
        <a href="#" className="nav-item active">Dashboard</a>
        <a href="#" className="nav-item">Customers</a>
        <a href="#" className="nav-item">Segments</a>
        <a href="#" className="nav-item">Recommendations</a>
        <a href="#" className="nav-item">Settings</a>
      </nav>
    </aside>
  );
};

export default Sidebar;
