import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { isAdmin } from '../utils/auth';
import './MLDashboard.css';

const MLDashboard = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  useEffect(() => {
    let cancelled = false;
    const controller = new AbortController();
    
    async function load() {
      setLoading(true);
      try {
        const res = await axios.get('http://localhost:5000/api/analytics/ml/metrics', {
          signal: controller.signal,
          timeout: 30000
        });
        if (cancelled) return;
        setData(res.data);
      } catch (e) {
        if (cancelled || e.name === 'AbortError') return;
        setError(e.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    
    load();
    return () => { 
      cancelled = true;
      controller.abort();
    };
  }, []);

  if (loading) return <div className="ml-panel-loading">Loading ML dashboard…</div>;
  if (error) return <div className="ml-panel-error">Error: {error}</div>;
  
  const metrics = data?.metrics || {};
  const imgUrl = data?.image ? `http://localhost:5000/backend/data/ml_dashboard.png?t=${Date.now()}` : null;
  
  return (
    <div className="ml-dashboard">
      {isAdmin() ? (
        <div style={{ display: 'flex', gap: '2rem', alignItems: 'flex-start' }}>
          <div className="ml-dashboard-image" style={{ flex: '1' }}>
            {imgUrl ? (
              <img src={imgUrl} alt="ML dashboard" style={{ width: '100%', borderRadius: 8 }} />
            ) : (
              <div className="no-image">No dashboard image available</div>
            )}
          </div>
          <div className="ml-dashboard-metrics" style={{ minWidth: '200px' }}>
            {Object.keys(metrics).length > 0 ? (
              Object.entries(metrics).map(([k, v]) => {
                const displayValue = typeof v === 'number' ? v.toFixed(3) : String(v);
                return (
                  <div key={k} className="kpi-card">
                    <div className="kpi-label">{k}</div>
                    <div className="kpi-value">{displayValue}</div>
                  </div>
                );
              })
            ) : (
              <div>No metrics available</div>
            )}
          </div>
        </div>
      ) : (
        <div className="ml-dashboard-metrics">
          {Object.keys(metrics).length > 0 ? (
            Object.entries(metrics).map(([k, v]) => {
              const displayValue = typeof v === 'number' ? v.toFixed(3) : String(v);
              return (
                <div key={k} className="kpi-card">
                  <div className="kpi-label">{k}</div>
                  <div className="kpi-value">{displayValue}</div>
                </div>
              );
            })
          ) : (
            <div>No metrics available</div>
          )}
        </div>
      )}
    </div>
  );
};

export default MLDashboard;
