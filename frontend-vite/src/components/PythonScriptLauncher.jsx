import React, { useState } from 'react';
import { runPythonScript } from '../utils/pythonApi';

const SCRIPTS = [
  { name: 'Threat Scoring', file: 'threat_scoring.py' },
  { name: 'ML Data Pipeline', file: 'ml_data_pipeline.py' },
  { name: 'Demo Dashboard', file: 'demo_dashboard.py' },
  { name: 'Threat API', file: 'threat_api.py' },
  { name: 'Automated Threat Collector', file: 'automated_threat_collector.py' },
  { name: 'Score Combined Threats', file: 'score_combined_threats.py' },
  { name: 'Complete System Test', file: 'complete_system_test.py' }
];

export default function PythonScriptLauncher() {
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleRun = async (file) => {
    setLoading(true);
    setOutput('Running...');
    const result = await runPythonScript(file);
    setOutput(result.stdout || result.stderr || JSON.stringify(result));
    setLoading(false);
  };

  return (
    <div style={{ padding: 24 }}>
      <h2>Python Script Launcher</h2>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 16, marginBottom: 24 }}>
        {SCRIPTS.map(script => (
          <button
            key={script.file}
            onClick={() => handleRun(script.file)}
            disabled={loading}
            style={{ padding: '12px 24px', fontSize: 16, borderRadius: 8, cursor: 'pointer' }}
          >
            {script.name}
          </button>
        ))}
      </div>
      <pre style={{ background: '#222', color: '#0f0', padding: 16, borderRadius: 8, minHeight: 120 }}>
        {output}
      </pre>
    </div>
  );
}
