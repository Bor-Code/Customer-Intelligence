import './RawData.css';

const MOCK_RAW_DATA = [
  '{ "event_id": "e-1001", "timestamp": "2026-10-04T16:50:01Z", "type": "page_view", "user_id": "CUST-8239" }',
  '{ "event_id": "e-1002", "timestamp": "2026-10-04T16:50:04Z", "type": "add_to_cart", "item_id": "SKU-992", "price": 45.99 }',
  '{ "event_id": "e-1003", "timestamp": "2026-10-04T16:50:11Z", "type": "checkout", "user_id": "CUST-1042", "amount": 120.50 }',
  '{ "event_id": "e-1004", "timestamp": "2026-10-04T16:50:25Z", "type": "search", "query": "industrial servo" }',
  '{ "event_id": "e-1005", "timestamp": "2026-10-04T16:50:33Z", "type": "login", "user_id": "CUST-5512", "device": "mobile" }',
];

const RawData = () => (
  <div className="page-wrapper">
    <header className="page-header">
      <div>
        <h1>Raw Data Stream</h1>
        <p className="subtitle">Real-time incoming event payload logs (Kafka / Event Grid)</p>
      </div>
      <button className="primary-btn">Clear Logs</button>
    </header>

    <div className="industrial-card">
      <div className="terminal-window">
        {MOCK_RAW_DATA.map((log, index) => (
          <div key={index} className="log-line mono">
            <span className="log-prefix">&gt;_</span> {log}
          </div>
        ))}
        <div className="log-line mono blinking-cursor">
          <span className="log-prefix">&gt;_</span>
        </div>
      </div>
    </div>
  </div>
);

export default RawData;
