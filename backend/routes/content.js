const express = require('express');
const router = express.Router();
const Content = require('../models/content');

// Add new content (article or quiz)
router.post('/add', async (req, res) => {
  try {
    const { type, title, content } = req.body;
    
    if (!type || !title || !content) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    const newContent = new Content({
      type,
      title,
      content
    });
    
    const savedContent = await newContent.save();
    
    res.json({ 
      success: true, 
      message: `${type === 'quiz' ? 'Quiz' : 'Article'} added successfully`,
      id: savedContent._id
    });
    
  } catch (error) {
    console.error('Content add error:', error);
    res.status(500).json({ error: 'Failed to add content' });
  }
});

module.exports = router;