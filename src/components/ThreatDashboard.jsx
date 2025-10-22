import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ThreatDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await axios.get('http://localhost:5001/api/dashboard/threat-intelligence', {
          timeout: 30000
        });
        setData(res.data);
      } catch (e) {
        console.error(e);
        setData({ ok: false, error: e.message });
      } finally { setLoading(false); }
    }
    load();
  }, []);

  if (loading) return <div>Loading threat intelligence...</div>;
  
  return (
    <div className="card">
      <h3>Threat Intelligence Dashboard</h3>
      {data?.ok !== false ? (
        <div>
          <img 
            src={`http://localhost:5001/threat_intelligence_dashboard.png?t=${Date.now()}`}
            alt="Threat Dashboard" 
            style={{width: '100%'}} 
            onError={(e) => {
              e.target.style.display = 'none';
              e.target.nextSibling.style.display = 'block';
            }}
          />
          <div style={{display: 'none', padding: '2rem', textAlign: 'center', background: '#f8f9fa', border: '1px solid #dee2e6', borderRadius: '8px', color: '#6c757d'}}>
            📊 Threat Intelligence Dashboard<br/>
            <small>Chart not available - data processing in progress</small>
          </div>
        </div>
      ) : (
        <div style={{padding: '2rem', textAlign: 'center', background: '#f8f9fa', border: '1px solid #dee2e6', borderRadius: '8px', color: '#6c757d'}}>
          ⚠️ Threat Intelligence Unavailable<br/>
          <small>{data?.error || 'Service temporarily offline'}</small>
        </div>
      )}
    </div>
  );
};

export default ThreatDashboard;