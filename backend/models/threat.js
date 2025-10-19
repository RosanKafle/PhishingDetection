const mongoose = require('mongoose');
const ThreatSchema = new mongoose.Schema({
  url: { type: String, required: true, index: true },
  source: String,
  collected_at: { type: Date, default: Date.now },
  normalized: Object,
  score: Number,
  level: String,
  meta: Object
}, { timestamps: true });
module.exports = mongoose.model('Threat', ThreatSchema);
