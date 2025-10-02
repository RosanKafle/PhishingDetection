const mongoose = require('mongoose');

const contentSchema = new mongoose.Schema({
  type: { type: String, enum: ['quiz', 'article'], required: true },
  title: { type: String, required: true },
  content: { type: mongoose.Schema.Types.Mixed, required: true }
});

module.exports = mongoose.model('Content', contentSchema);