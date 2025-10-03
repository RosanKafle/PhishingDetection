

import React, { useEffect, useState } from 'react';
import './KPIDashboardPanel.css';
import { FaCheckCircle, FaExclamationTriangle, FaClock, FaShieldAlt, FaSmile, FaChartLine, FaAward } from 'react-icons/fa';


const KPIDashboardPanel = () => {
  const [kpi, setKpi] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // For phishing check
  const [url, setUrl] = useState("");
  const [phishingResult, setPhishingResult] = useState(null);
  const [phishingLoading, setPhishingLoading] = useState(false);
  const [phishingError, setPhishingError] = useState(null);

  useEffect(() => {
    fetch('/api/analytics/kpi')
      .then(res => {
        if (!res.ok) throw new Error('Failed to fetch KPI data');
        return res.json();
      })
      .then(data => {
        setKpi(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const handlePhishingCheck = async (e) => {
    e.preventDefault();
    setPhishingResult(null);
    setPhishingError(null);
    setPhishingLoading(true);
    try {
      const res = await fetch('/api/analytics/check-phishing', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      });
      if (!res.ok) throw new Error('Failed to check link');
      const data = await res.json();
      setPhishingResult(data);
    } catch (err) {
      setPhishingError(err.message);
    } finally {
      setPhishingLoading(false);
    }
  };

  return (
    <div className="kpi-dashboard-panel">
      <h2>Security KPI Dashboard</h2>
      {/* Phishing check input */}
      <form className="phishing-check-form" onSubmit={handlePhishingCheck} style={{marginBottom: 32}}>
        <input
          type="text"
          placeholder="Enter a link to check for phishing..."
          value={url}
          onChange={e => setUrl(e.target.value)}
          className="phishing-input"
        />
        <button type="submit" className="phishing-btn" disabled={phishingLoading || !url.trim()}>
          {phishingLoading ? 'Checking...' : 'Check Link'}
        </button>
      </form>
      {phishingError && <div style={{color:'red', marginBottom: 12}}>Error: {phishingError}</div>}
      {phishingResult && (
        <div className={`phishing-result ${phishingResult.threat_level && phishingResult.threat_level !== 'INFORMATIONAL' ? 'phishing' : 'safe'}`}
             style={{marginBottom: 24}}>
          <strong>Result:</strong> {phishingResult.threat_level ? phishingResult.threat_level : phishingResult.error}
          {phishingResult.threat_score !== undefined && (
            <span style={{marginLeft: 12}}>Score: {phishingResult.threat_score}</span>
          )}
        </div>
      )}
      {loading && <div>Loading...</div>}
      {error && <div style={{color:'red'}}>Error: {error}</div>}
      {kpi && (
        <div className="kpi-cards">
          <div className="kpi-card kpi-detection"><FaCheckCircle className="kpi-icon" /><span>Detection Rate</span><strong>{kpi.detectionRate}</strong></div>
          <div className="kpi-card kpi-fpr"><FaExclamationTriangle className="kpi-icon" /><span>False Positive Rate</span><strong>{kpi.falsePositiveRate}</strong></div>
          <div className="kpi-card kpi-response"><FaClock className="kpi-icon" /><span>Response Time</span><strong>{kpi.responseTime}</strong></div>
          <div className="kpi-card kpi-threats"><FaShieldAlt className="kpi-icon" /><span>Threats Processed</span><strong>{kpi.threatsProcessed}</strong></div>
          <div className="kpi-card kpi-uptime"><FaChartLine className="kpi-icon" /><span>System Uptime</span><strong>{kpi.uptime}</strong></div>
          <div className="kpi-card kpi-satisfaction"><FaSmile className="kpi-icon" /><span>User Satisfaction</span><strong>{kpi.userSatisfaction}</strong></div>
          <div className="kpi-card kpi-compliance"><FaAward className="kpi-icon" /><span>Compliance</span><strong>{kpi.compliance}</strong></div>
        </div>
      )}
    </div>
  );
};

export default KPIDashboardPanel;
