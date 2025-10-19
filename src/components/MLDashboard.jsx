import React, { useEffect, useState } from 'react';
import axios from 'axios';

const MLDashboard = () => {
  const [metrics, setMetrics] = useState(null);
  const [imgUrl, setImgUrl] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const res = await axios.get('http://localhost:5000/api/analytics/ml/metrics');
        setMetrics(res.data.metrics || {});
        if (res.data.dashboardImage) setImgUrl(`http://localhost:5000${res.data.dashboardImage}`);
      } catch (e) {
        console.error(e);
      } finally { setLoading(false); }
    }
    load();
  }, []);

  if (loading) return <div className="card">Loading ML dashboard...</div>;
  return (
    <div className="card" style={{ padding: '1rem' }}>
      <h3 className="card-title">ML Phishing Detector Dashboard</h3>
      <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
        <div style={{ flex: 1 }}>
          {imgUrl ? <img src={imgUrl} alt="ML Dashboard" style={{ width: '100%', borderRadius: 8 }} /> : <div>No image</div>}
        </div>
        <div style={{ width: 260 }}>
          <h4>Metrics</h4>
          <ul>
            <li>Accuracy: {metrics.accuracy || 'n/a'}</li>
            <li>Precision: {metrics.precision || 'n/a'}</li>
            <li>Recall: {metrics.recall || 'n/a'}</li>
            <li>F1: {metrics.f1 || 'n/a'}</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default MLDashboard;
