import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ThreatDashboard = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await axios.get('http://localhost:5000/api/dashboard/threat-intelligence');
        setData(res.data);
      } catch (e) {
        console.error(e);
      } finally { setLoading(false); }
    }
    load();
  }, []);

  if (loading) return <div>Loading threat intelligence...</div>;
  
  return (
    <div className="card">
      <h3>Threat Intelligence Dashboard</h3>
      {data?.ok ? (
        <div>
          <img src="http://localhost:5000/threat_intelligence_dashboard.png" alt="Threat Dashboard" style={{width: '100%'}} />
          <pre style={{fontSize: '12px', background: '#f5f5f5', padding: '1rem'}}>{data.stdout}</pre>
        </div>
      ) : (
        <div>Error loading threat dashboard</div>
      )}
    </div>
  );
};

export default ThreatDashboard;