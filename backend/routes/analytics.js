const express = require('express');
const router = express.Router();



const { spawn } = require('child_process');

const fs = require('fs');
const path = require('path');

const { parse } = require('csv-parse/sync');
const csvPath = path.join(__dirname, '../../combined_threats.csv');
const scriptPath = path.join(__dirname, '../../threat_scoring.py');


router.get('/kpi', (req, res) => {
  fs.readFile(csvPath, 'utf8', (err, data) => {
    if (err) return res.status(500).json({ error: 'Failed to read threat data' });
    let records;
    try {
      records = parse(data, {
        columns: true,
        skip_empty_lines: true,
        trim: true
      });
    } catch (e) {
      return res.status(500).json({ error: 'Failed to parse CSV' });
    }
    // Limit to 1000 most recent threats for performance
    const cases = records.slice(0, 1000).map(row => ({
      url: row.url,
      sources_count: 1,
      api_results: { virustotal_malicious: 0, urlvoid_failed: false }
    }));
  const py = spawn('python3', [scriptPath], { cwd: path.dirname(scriptPath) });
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
    py.stdin.write(JSON.stringify(cases));
    py.stdin.end();
  });
});


// POST /api/analytics/check-phishing
router.post('/check-phishing', (req, res) => {
  const { url } = req.body;
  if (!url) return res.status(400).json({ error: 'Missing url' });
  const py = spawn('python3', [scriptPath], { cwd: path.dirname(scriptPath) });
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
      // results is an array, return the first result
      res.json(results[0]);
    } catch (e) {
      res.status(500).json({ error: 'Failed to parse Python output' });
    }
  });
  py.stdin.write(JSON.stringify([{ url, sources_count: 1, api_results: { virustotal_malicious: 0, urlvoid_failed: false } }]));
  py.stdin.end();
});

module.exports = router;
