const express = require('express');
const router = express.Router();
const Content = require('../models/Content');
const { protect, adminOnly } = require('../middleware/auth');

router.get('/', async (req, res) => {
  const contents = await Content.find();
  res.json(contents);
});

router.post('/add', protect, adminOnly, async (req, res) => {
  const { type, title, content } = req.body;
  try {
    const newContent = new Content({ type, title, content });
    await newContent.save();
    res.status(201).json(newContent);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

module.exports = router;