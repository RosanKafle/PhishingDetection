const express = require('express');
const router = express.Router();


const { spawn } = require('child_process');

// Example: Use static test cases for now, replace with DB or real-time data later
const testCases = [
  {
    url: 'http://paypal-secure.tk/login',
    sources_count: 3,
    api_results: { virustotal_malicious: 5, urlvoid_failed: false }
  },
  {
    url: 'http://google-support12345.ga/security',
    sources_count: 1,
    api_results: { virustotal_malicious: 0, urlvoid_failed: true }
  },
  {
    url: 'https://example.com/home',
    sources_count: 0,
    api_results: { virustotal_malicious: 0, urlvoid_failed: false }
  }
];

router.get('/kpi', (req, res) => {
  // Call the Python script with test cases as input
  const py = spawn('python3', ['threat_scoring.py']);
  let output = '';
  let error = '';
  py.stdout.on('data', (data) => { output += data; });
  py.stderr.on('data', (data) => { error += data; });
  py.on('close', (code) => {
    if (code !== 0 || error) {
      return res.status(500).json({ error: error || 'Python script failed' });
    }
    try {
      const results = JSON.parse(output);
      // Example KPI aggregation from results
      const detectionRate = (results.filter(r => r.threat_level !== 'INFORMATIONAL').length / results.length * 100).toFixed(1) + '%';
      const falsePositiveRate = (results.filter(r => r.threat_level === 'INFORMATIONAL').length / results.length * 100).toFixed(1) + '%';
      const responseTime = '2.3s'; // Placeholder
      const threatsProcessed = results.length;
      const uptime = '99.99%'; // Placeholder
      const userSatisfaction = '4.8/5'; // Placeholder
      const compliance = 'OWASP Top 10: 9/10'; // Placeholder
      res.json({ detectionRate, falsePositiveRate, responseTime, threatsProcessed, uptime, userSatisfaction, compliance });
    } catch (e) {
      res.status(500).json({ error: 'Failed to parse Python output' });
    }
  });
  py.stdin.write(JSON.stringify(testCases));
  py.stdin.end();
});

module.exports = router;
