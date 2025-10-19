const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const ModelSchema = new Schema({
  version: String,
  path: String,
  trained_at: Date,
  metrics: Schema.Types.Mixed,
  notes: String
});

module.exports = mongoose.model('MLModel', ModelSchema);