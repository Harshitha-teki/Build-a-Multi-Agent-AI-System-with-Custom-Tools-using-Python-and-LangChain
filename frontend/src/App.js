import React, { useState, useEffect, useRef } from 'react';

export default function App() {
  const [events, setEvents] = useState([]);
  const [query, setQuery] = useState('Summarize the state of AI in healthcare');
  const wsRef = useRef(null);
  const [runId, setRunId] = useState(null);

  const start = async () => {
    const res = await fetch('http://localhost:8000/api/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: 'demo', query }),
    });
    const j = await res.json();
    // create a run id locally (server logs one) - in this scaffold we won't get run id back
    const rid = Math.random().toString(36).slice(2);
    setRunId(rid);
    connectWS(rid);
  };

  const connectWS = (rid) => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${rid}`);
    ws.onopen = () => console.log('ws open');
    ws.onmessage = (e) => {
      const data = JSON.parse(e.data);
      setEvents((s) => [...s, data]);
    };
    wsRef.current = ws;
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Multi-Agent Orchestrator - Demo</h2>
      <div>
        <textarea value={query} onChange={(e) => setQuery(e.target.value)} rows={3} cols={80} />
      </div>
      <div style={{ marginTop: 10 }}>
        <button onClick={start}>Start Run</button>
      </div>

      <div style={{ marginTop: 20 }}>
        <h3>Events</h3>
        <div>
          {events.map((ev, i) => (
            <pre key={i} style={{ background: '#f5f5f5', padding: 10 }}>{JSON.stringify(ev, null, 2)}</pre>
          ))}
        </div>
      </div>
    </div>
  );
}
