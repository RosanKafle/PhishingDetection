

import React, { useEffect, useState } from 'react';
import './KPIDashboardPanel.css';
import { FaCheckCircle, FaExclamationTriangle, FaClock, FaShieldAlt, FaSmile, FaChartLine, FaAward } from 'react-icons/fa';

const KPIDashboardPanel = () => {
  const [kpi, setKpi] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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

  return (
    <div className="kpi-dashboard-panel">
      <h2>Security KPI Dashboard</h2>
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
