const express = require('express');
const router = express.Router();
const { spawnSync } = require('child_process');
const path = require('path');
const { readCache, writeCache } = require('../services/cache');

// 1. Comprehensive threat dashboard
router.get('/threat-intelligence', async (req, res) => {
  const cached = readCache('threat_dashboard', 1800);
  if (cached) return res.json({ fromCache: true, ...cached });
  
  try {
    const result = spawnSync('python3', ['demo_dashboard.py'], { 
      cwd: path.join(__dirname, '../..'), timeout: 60000 
    });
    const payload = { ok: result.status === 0, stdout: result.stdout?.toString() || '', ts: Date.now() };
    writeCache('threat_dashboard', payload);
    return res.json({ fromCache: false, ...payload });
  } catch (e) { return res.status(500).json({ error: e.message }); }
});

// 2. User behavior analytics
router.get('/user-behavior', async (req, res) => {
  const cached = readCache('user_behavior', 3600);
  if (cached) return res.json({ fromCache: true, ...cached });
  
  try {
    const result = spawnSync('python3', ['generate_user_behavior.py'], { 
      cwd: path.join(__dirname, '../..'), timeout: 30000 
    });
    const payload = { ok: result.status === 0, stdout: result.stdout?.toString() || '', ts: Date.now() };
    writeCache('user_behavior', payload);
    return res.json({ fromCache: false, ...payload });
  } catch (e) { return res.status(500).json({ error: e.message }); }
});

// 3. Model performance monitoring
router.get('/model-performance', async (req, res) => {
  const cached = readCache('model_performance', 1800);
  if (cached) return res.json({ fromCache: true, ...cached });
  
  try {
    const result = spawnSync('python3', ['analytics/model_monitoring/performance_logger.py'], { 
      cwd: path.join(__dirname, '../..'), timeout: 30000 
    });
    const payload = { ok: result.status === 0, stdout: result.stdout?.toString() || '', ts: Date.now() };
    writeCache('model_performance', payload);
    return res.json({ fromCache: false, ...payload });
  } catch (e) { return res.status(500).json({ error: e.message }); }
});

// 4. Real-time threat collection status
router.get('/realtime-threats', async (req, res) => {
  const cached = readCache('realtime_threats', 900); // 15 min cache
  if (cached) return res.json({ fromCache: true, ...cached });
  
  try {
    const result = spawnSync('python3', ['automated_threat_collector.py'], { 
      cwd: path.join(__dirname, '../..'), timeout: 120000 
    });
    const payload = { ok: result.status === 0, stdout: result.stdout?.toString() || '', ts: Date.now() };
    writeCache('realtime_threats', payload);
    return res.json({ fromCache: false, ...payload });
  } catch (e) { return res.status(500).json({ error: e.message }); }
});

module.exports = router;