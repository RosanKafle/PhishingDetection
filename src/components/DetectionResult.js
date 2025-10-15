import React from 'react';

const DetectionResult = ({ result, details }) => {
  const isPhishing = result === 'phishing';
  
  return (
    <div className={`result ${isPhishing ? 'phishing' : 'safe'}`}>
      <div className="result-title">
        {isPhishing ? (
          <>
            🚨 Phishing Detected!
          </>
        ) : (
          <>
            ✅ Safe Content
          </>
        )}
      </div>
      <p className="result-details">{details}</p>
      
      {isPhishing && (
        <div className="mt-3">
          <h4>⚠️ Recommended Actions:</h4>
          <ul>
            <li>Do not click on any links in this content</li>
            <li>Do not provide any personal information</li>
            <li>Delete the email or close the website</li>
            <li>Report the incident to your IT department</li>
            <li>If you already clicked a link, change your passwords immediately</li>
          </ul>
        </div>
      )}
      
      {!isPhishing && (
        <div className="mt-3">
          <h4>✅ Safety Confirmed:</h4>
          <ul>
            <li>This content appears to be legitimate</li>
            <li>No suspicious patterns were detected</li>
            <li>You can proceed with caution</li>
            <li>Always verify sender identity when possible</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default DetectionResult;