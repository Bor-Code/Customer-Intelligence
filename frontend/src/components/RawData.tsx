import { useEffect, useState, useRef } from 'react';
import './RawData.css';

const RawData = () => {
  const [logs, setLogs] = useState<string[]>([]);
  const ws = useRef<WebSocket | null>(null);
  const endRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    ws.current = new WebSocket('ws://localhost:8000/ws/events');
    ws.current.onmessage = (event) => {
      setLogs(prev => [...prev, event.data].slice(-50)); // keep last 50 logs max
    };
    return () => {
      ws.current?.close();
    };
  }, []);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div className="page-wrapper">
      <header className="page-header">
        <div>
          <h1>Raw Data Stream</h1>
          <p className="subtitle">Real-time incoming event payload logs (Kafka / Event Grid)</p>
        </div>
        <button className="primary-btn" onClick={() => setLogs([])}>Clear Logs</button>
      </header>

      <div className="industrial-card">
        <div className="terminal-window">
          {logs.length === 0 && <div className="log-line mono" style={{color: '#52525b'}}>Connecting to live event stream...</div>}
          {logs.map((log, index) => (
            <div key={index} className="log-line mono">
              <span className="log-prefix">&gt;_</span> {log}
            </div>
          ))}
          <div className="log-line mono blinking-cursor" ref={endRef}>
            <span className="log-prefix">&gt;_</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RawData;
