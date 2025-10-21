const express = require('express');
const router = express.Router();

// In-memory storage for detections (replace with DB if needed)
let detections = [];

// GET /api/detections - Get user's detection history
router.get('/', (req, res) => {
  res.json({ detections });
});

// POST /api/detections - Save detection result
router.post('/', (req, res) => {
  const { content, result, reason } = req.body;
  
  const detection = {
    id: Date.now().toString(),
    content: content || '',
    result: result || 'unknown',
    reason: reason || '',
    createdAt: new Date().toISOString()
  };
  
  detections.unshift(detection);
  
  // Keep only last 100 detections
  if (detections.length > 100) {
    detections = detections.slice(0, 100);
  }
  
  res.json({ success: true, detection });
});

module.exports = router;