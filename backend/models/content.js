const mongoose = require('mongoose');

const contentSchema = new mongoose.Schema({
  type: {
    type: String,
    required: true,
    enum: ['article', 'quiz']
  },
  title: {
    type: String,
    required: true
  },
  content: {
    type: String,
    required: true
  },
  createdAt: {
    type: Date,
    default: Date.now
  }
});

module.exports = mongoose.model('Content', contentSchema);