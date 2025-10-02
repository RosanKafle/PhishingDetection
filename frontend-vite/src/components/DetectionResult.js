import React from 'react';

const DetectionResult = ({ result, details }) => {
  return (
    <div className="result">
      <h3>Detection Result: {result === 'phishing' ? 'Phishing Detected!' : 'Safe'}</h3>
      <p>Details: {details}</p>
    </div>
  );
};

export default DetectionResult;