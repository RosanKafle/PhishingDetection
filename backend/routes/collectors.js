const express = require('express');
const router = express.Router();
const { readCache } = require('../services/cache');
const { runThreatCollectors } = require('../services/scheduler');

// GET collector status
router.get('/status', (req, res) => {
  const cached = readCache('threat_collectors', 3600);
  if (cached) {
    return res.json({ fromCache: true, ...cached });
  }
  return res.json({ message: 'No recent collector runs found' });
});

// POST trigger collectors manually
router.post('/run', async (req, res) => {
  try {
    const result = runThreatCollectors();
    return res.json({ message: 'Collectors triggered', result });
  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
});

module.exports = router;