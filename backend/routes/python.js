const express = require('express');
const axios = require('axios');
const router = express.Router();

// POST /api/python/run
// { script: 'threat_scoring.py', args: ['arg1', 'arg2'] }
router.post('/run', async (req, res) => {
  try {
    const { script, args } = req.body;
    const response = await axios.post('http://localhost:8000/api/run_script', {
      script,
      args: args || []
    });
    res.json(response.data);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
