import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { getAuthToken } from '../utils/auth';
import DetectionResult from '../components/DetectionResult';
import UserBehavior from '../components/UserBehavior';
import { detectPhishing } from '../utils/phishingDetector';

const Dashboard = () => {
  const [content, setContent] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [detectionHistory, setDetectionHistory] = useState([]);
  const [stats, setStats] = useState({
    totalDetections: 0,
    phishingDetected: 0,
    safeContent: 0,
    accuracyRate: 0
  });
  const [mlMetrics, setMlMetrics] = useState(null);

  useEffect(() => {
    // Fetch history once on mount
    fetchDetectionHistory();
    fetchMLMetrics();
  }, []);

  // Recalculate stats whenever detectionHistory changes
  const calculateStats = useCallback(() => {
    const total = detectionHistory.length;
    const phishing = detectionHistory.filter(d => d.result === 'phishing').length;
    const safe = detectionHistory.filter(d => d.result === 'safe').length;
    const mlAccuracy = mlMetrics?.accuracy ? parseFloat(mlMetrics.accuracy.replace('%', '')) : 0;
    
    setStats({
      totalDetections: total,
      phishingDetected: phishing,
      safeContent: safe,
      accuracyRate: mlAccuracy
    });
  }, [detectionHistory, mlMetrics]);

  useEffect(() => {
    calculateStats();
  }, [calculateStats]);

  const fetchDetectionHistory = async () => {
    try {
      const response = await axios.get('http://localhost:5001/api/detections', {
        headers: { Authorization: `Bearer ${getAuthToken()}` }
      });
      // Handle the paginated response structure
      const detections = response.data.detections || response.data || [];
      setDetectionHistory(Array.isArray(detections) ? detections : []);
    } catch (error) {
      // Fallback to empty array if backend is not available
      setDetectionHistory([]);
    }
  };

  const fetchMLMetrics = async () => {
    try {
      const response = await axios.get('http://localhost:5001/api/analytics/ml/metrics');
      setMlMetrics(response.data.metrics);
    } catch (error) {
      setMlMetrics(null);
    }
  };

  // ...calculateStats is defined above using useCallback

  const handleAnalyze = async () => {
    if (!content.trim()) {
      alert('Please enter some content to analyze');
      return;
    }

    setLoading(true);
    
    try {
      // Use local phishing detection
      const detection = detectPhishing(content);
      setResult(detection.isPhishing ? 'phishing' : 'safe');
      
      // Try to save to backend
      try {
        await axios.post('http://localhost:5001/api/detections', {
          content: content.substring(0, 500), // Limit content length
          result: detection.isPhishing ? 'phishing' : 'safe',
          reason: detection.reason
        }, {
          headers: { Authorization: `Bearer ${getAuthToken()}` }
        });
        fetchDetectionHistory(); // Refresh history
        calculateStats(); // Update stats
      } catch (backendError) {
        console.log('Backend not available, using local detection only');
      }
    } catch (error) {
      alert('Error analyzing content: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setContent('');
    setResult(null);
  };

  return (
    <div className="container">
      {/* Welcome Header */}
      <div className="card mb-5 hover-lift">
        <div className="text-center">
          <h1 className="card-title gradient-text">🔍 Phishing Detection Dashboard</h1>
          <p className="card-subtitle">
            Analyze emails, URLs, and text content for potential phishing attempts
          </p>
          <div className="mt-4">
            <div className="badge badge-primary">Real-time Analysis</div>

            <div className="badge badge-info">Instant Results</div>

          </div>
        </div>
      </div>

      {/* Statistics Cards */}
      <div className="grid grid-cols-4 mb-5">
        <div className="card hover-lift">
          <div className="text-center">
            <div className="text-4xl mb-2">📊</div>
            <div className="text-3xl font-bold text-primary">{stats.totalDetections}</div>
            <div className="text-secondary">Total Detections</div>
          </div>
        </div>
        
        <div className="card hover-lift">
          <div className="text-center">
            <div className="text-4xl mb-2">🚨</div>
            <div className="text-3xl font-bold text-danger">{stats.phishingDetected}</div>
            <div className="text-secondary">Phishing Detected</div>
          </div>
        </div>
        
        <div className="card hover-lift">
          <div className="text-center">
            <div className="text-4xl mb-2">✅</div>
            <div className="text-3xl font-bold text-success">{stats.safeContent}</div>
            <div className="text-secondary">Safe Content</div>
          </div>
        </div>
        
        <div className="card hover-lift">
          <div className="text-center">
            <div className="text-4xl mb-2">🎯</div>
            <div className="text-3xl font-bold text-warning">{stats.accuracyRate}%</div>
            <div className="text-secondary">Accuracy Rate</div>
          </div>
        </div>
      </div>

      {/* Detection Form */}
      <div className="card mb-5 hover-lift">
        <div className="card-header">
          <h2 className="card-title">📝 Content Analysis</h2>
          <p className="card-subtitle">Enter suspicious content to analyze</p>
        </div>
        
        <div className="form">
          <div className="form-group">
            <label htmlFor="content" className="form-label">Content to Analyze</label>
            <textarea 
              id="content"
              value={content} 
              onChange={(e) => setContent(e.target.value)} 
              className="form-textarea"
              placeholder="Paste suspicious email content, URL, or text here..."
              rows="8"
            />
            <div className="mt-2 text-sm text-secondary">
              Character count: {content.length} / 5000
            </div>
          </div>
          
          <div className="flex gap-3">
            <button 
              onClick={handleAnalyze} 
              className="btn btn-primary"
              disabled={loading || !content.trim()}
            >
              {loading ? (
                <span className="loading">
                  <span className="spinner"></span>
                  Analyzing...
                </span>
              ) : (
                <>
                  🔍 Analyze Content
                </>
              )}
            </button>
            
            <button 
              onClick={handleClear} 
              className="btn btn-secondary"
              disabled={loading}
            >
              🗑️ Clear
            </button>
          </div>
        </div>
      </div>

      {/* Detection Result */}
      {result && (
        <div className="card mb-5">
          <DetectionResult 
            result={result} 
            details={result === 'phishing' ? 'Suspicious patterns detected in the content' : 'No suspicious patterns found'}
          />
        </div>
      )}


      {/* Detection History */}
      <div className="card mb-5">
        <div className="card-header">
          <h2 className="card-title">📊 Detection History</h2>
          <p className="card-subtitle">Your recent phishing detection results</p>
        </div>
        
        {!Array.isArray(detectionHistory) || detectionHistory.length === 0 ? (
          <div className="text-center p-4">
            <div className="text-6xl mb-4">📈</div>
            <p className="text-secondary mb-2">No detection history available</p>
            <p className="text-secondary">Start analyzing content to build your history</p>
          </div>
        ) : (
          <div className="detection-history">
            {detectionHistory.slice(0, 5).map((detection, index) => (
              <div key={index} className="detection-item hover-lift">
                <div className="detection-header">
                  <span className={`detection-badge ${detection.result}`}>
                    {detection.result === 'phishing' ? '🚨 Phishing' : '✅ Safe'}
                  </span>
                  <span className="detection-date">
                    {new Date(detection.createdAt).toLocaleDateString()}
                  </span>
                </div>
                <div className="detection-content">
                  {detection.content.substring(0, 100)}
                  {detection.content.length > 100 && '...'}
                </div>
                {detection.reason && (
                  <div className="detection-reason">
                    <strong>Reason:</strong> {detection.reason}
                  </div>
                )}
              </div>
            ))}
            {detectionHistory.length > 5 && (
              <div className="text-center mt-4">
                <button className="btn btn-secondary">View All History</button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Quick Tips */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">💡 Quick Tips</h2>
          <p className="card-subtitle">What to look for when analyzing content</p>
        </div>
        
        <div className="grid grid-cols-3">
          <div className="content hover-lift">
            <div className="text-center mb-4">
              <div className="text-4xl">📧</div>
              <h3>Email Analysis</h3>
            </div>
            <ul>
              <li>Check sender email address carefully</li>
              <li>Look for urgent or threatening language</li>
              <li>Verify links before clicking</li>
              <li>Check for spelling and grammar errors</li>
            </ul>
          </div>
          
          <div className="content hover-lift">
            <div className="text-center mb-4">
              <div className="text-4xl">🔗</div>
              <h3>URL Analysis</h3>
            </div>
            <ul>
              <li>Look for misspelled domain names</li>
              <li>Check for suspicious subdomains</li>
              <li>Verify HTTPS certificates</li>
              <li>Avoid shortened URLs from unknown sources</li>
            </ul>
          </div>
          
          <div className="content hover-lift">
            <div className="text-center mb-4">
              <div className="text-4xl">📝</div>
              <h3>Text Analysis</h3>
            </div>
            <ul>
              <li>Watch for generic greetings</li>
              <li>Look for requests for personal information</li>
              <li>Check for suspicious attachments</li>
              <li>Verify company branding and logos</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;