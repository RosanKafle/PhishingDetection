const express = require('express');
const cors = require('cors');
const dotenv = require('dotenv');
const path = require('path');
const fs = require('fs');

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

// Initialize scheduler lazily
setImmediate(() => {
  try {
    require('./services/scheduler');
  } catch (err) {
    console.warn('Scheduler initialization warning:', err.message);
  }
});

// Health endpoint
app.get('/api/health', (req, res) => {
    const mongooseReady = mongoose && mongoose.connection ? mongoose.connection.readyState : 0;
    const dbStatus = mongooseReady === 1 ? 'connected' : (mongooseReady === 2 ? 'connecting' : 'disconnected');
    const devStore = process.env.DEV_USER_STORE === 'true';
    res.json({
      status: 'ok',
      db: dbStatus,
      devUserStore: devStore,
      pythonWrapper: fs.existsSync(path.join(__dirname, 'data/ml_dashboard.png')) ? 'ok' : 'unknown'
    });
});

// Routes - cache loaded modules for performance
const routeCache = {};
const loadRoute = (routePath) => {
  if (!routeCache[routePath]) {
    routeCache[routePath] = require(routePath);
  }
  return routeCache[routePath];
};

app.use('/api/analytics', (req, res, next) => loadRoute('./routes/analytics')(req, res, next));
app.use('/api/dashboard', (req, res, next) => loadRoute('./routes/dashboard')(req, res, next));
app.use('/api/ingest', (req, res, next) => loadRoute('./routes/ingest')(req, res, next));
app.use('/api/pentest', (req, res, next) => loadRoute('./routes/pentest')(req, res, next));
app.use('/api/collectors', (req, res, next) => loadRoute('./routes/collectors')(req, res, next));
app.use('/api/auth', (req, res, next) => loadRoute('./routes/auth')(req, res, next));

// Serve static backend data (including generated ML dashboard image)
app.use('/backend/data', express.static(path.join(__dirname, 'data')));
// Serve static files from project root (for dashboard images)
app.use(express.static(path.join(__dirname, '..')));

const PORT = process.env.PORT || 5000;
const server = app.listen(PORT, () => console.log(`Backend server listening on port ${PORT}`));
server.timeout = 30000;

module.exports = app;
