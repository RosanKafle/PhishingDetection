const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const path = require('path');

dotenv.config();
const app = express();
app.use(express.json({ limit: '2mb' }));
app.use(cors());

// Connect to MongoDB if URI provided (safe default to localhost)
const mongoose = require('mongoose');
const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/phishing';
mongoose.set('bufferTimeoutMS', 5000);
mongoose.connect(MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true, serverSelectionTimeoutMS: 5000 })
	.then(() => console.log('Connected to MongoDB'))
	.catch((err) => console.warn('MongoDB connection warning:', err.message, '\nTo run locally, start MongoDB (see backend/.env.example or run `docker compose up -d mongodb`)'));

// Routes
app.use('/api/analytics', require('./routes/analytics'));
app.use('/api/ingest', require('./routes/ingest'));
app.use('/api/pentest', require('./routes/pentest'));
// Auth route (may be empty initially)
app.use('/api/auth', require('./routes/auth'));

// Serve static backend data (including generated ML dashboard image)
app.use('/backend/data', express.static(path.join(__dirname, 'data')));

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Backend server listening on port ${PORT}`));

module.exports = app;
