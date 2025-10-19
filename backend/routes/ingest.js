const express = require('express');
const router = express.Router();
const Threat = require('../models/threat');

router.post('/threat', async (req, res) => {
  try {
    const { url, source, collected_at, meta } = req.body;
    const t = new Threat({ url, source, collected_at, meta });
    await t.save();
    res.status(201).json({ id: t._id, status: 'stored' });
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
});

module.exports = router;
