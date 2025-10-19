const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const ThreatSchema = new Schema({
  url: { 
    type: String, 
    required: true, 
    index: true,
    trim: true
  },
  source: { 
    type: String, 
    default: 'manual',
    enum: ['manual', 'openphish', 'urlhaus', 'virustotal']
  },
  timestamp: { 
    type: Date, 
    default: Date.now,
    index: true
  },
  status: { 
    type: String, 
    enum: ['new', 'scored', 'archived'], 
    default: 'new',
    index: true
  },
  features: { type: Schema.Types.Mixed },
  score: { 
    type: Number, 
    default: 0,
    min: 0,
    max: 100
  }
});

module.exports = mongoose.model('Threat', ThreatSchema);