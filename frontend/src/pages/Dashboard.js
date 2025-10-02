import React, { useState } from 'react';
import DetectionResult from '../components/DetectionResult';
import { detectPhishing } from '../utils/phishingDetector';

const Dashboard = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);

  const handleDetect = (e) => {
    e.preventDefault();
    const outcome = detectPhishing(input);
    setResult({
      result: outcome.isPhishing ? 'phishing' : 'safe',
      details: outcome.reason
    });
  };

  return (
    <div>
      <h2>Phishing Detector</h2>
      <form onSubmit={handleDetect} className="form">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Paste an email body or URL to analyze"
          required
        />
        <button type="submit">Analyze</button>
      </form>
      {result && (
        <DetectionResult result={result.result} details={result.details} />
      )}
    </div>
  );
};

export default Dashboard;


