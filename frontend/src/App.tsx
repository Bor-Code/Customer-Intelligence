import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="app-container">
      <Sidebar />
      <main className="main-content animate-fade-in">
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
