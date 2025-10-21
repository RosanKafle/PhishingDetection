const express = require('express');
const router = express.Router();
const mongoose = require('mongoose');

// Get admin statistics
router.get('/stats', async (req, res) => {
  try {
    let stats = {
      totalUsers: 0,
      totalDetections: 0,
      totalArticles: 2, // Fixed number as requested
      totalQuizzes: 0
    };

    // Count users from database or dev store
    if (mongoose.connection.readyState === 1) {
      try {
        const User = require('../models/user');
        stats.totalUsers = await User.countDocuments();
        
        // Count detections if model exists
        try {
          const Detection = mongoose.model('Detection');
          stats.totalDetections = await Detection.countDocuments();
        } catch (e) {
          // Detection model might not exist
        }
      } catch (e) {
        console.warn('Database query failed:', e.message);
      }
    } else {
      // Fallback to dev user store
      try {
        const { getDevUsers } = require('../services/devUserStore');
        const devUsers = getDevUsers();
        stats.totalUsers = devUsers.length;
      } catch (e) {
        console.warn('Dev user store failed:', e.message);
      }
    }

    res.json(stats);
  } catch (error) {
    console.error('Admin stats error:', error);
    res.status(500).json({ error: 'Failed to fetch statistics' });
  }
});

module.exports = router;