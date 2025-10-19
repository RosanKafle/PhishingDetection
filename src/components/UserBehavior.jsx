import React, { useEffect, useState } from 'react';
import axios from 'axios';

const UserBehavior = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await axios.get('http://localhost:5000/api/dashboard/user-behavior');
        setData(res.data);
      } catch (e) {
        console.error(e);
      } finally { setLoading(false); }
    }
    load();
  }, []);

  if (loading) return <div>Loading user behavior analytics...</div>;
  
  return (
    <div className="card" style={{ padding: '1rem' }}>
      <h3 style={{ marginBottom: '1rem' }}>📊 User Behavior Analytics</h3>
      {data?.ok ? (
        <div>
          <img src="http://localhost:5000/user_behavior_dashboard.png" alt="User Behavior" style={{width: '100%', borderRadius: '8px', marginBottom: '1rem'}} />
          <div style={{ background: '#f8f9fa', padding: '0.75rem', borderRadius: '4px', fontSize: '13px' }}>
            <pre style={{ margin: 0, whiteSpace: 'pre-wrap', lineHeight: '1.4' }}>{data.stdout}</pre>
          </div>
        </div>
      ) : (
        <div style={{ textAlign: 'center', padding: '1.5rem', color: '#666' }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>📈</div>
          <div>Loading user behavior analytics...</div>
        </div>
      )}
    </div>
  );
};

export default UserBehavior;