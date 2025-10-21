const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const dotenv = require('dotenv');
const path = require('path');
const fs = require('fs');

dotenv.config();
const app = express();

// Security middleware
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      scriptSrc: ["'self'"],
      imgSrc: ["'self'", "data:", "http://localhost:*"]
    }
  }
}));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // limit each IP to 100 requests per windowMs
  message: { error: 'Too many requests' }
});
app.use('/api/', limiter);

// Stricter rate limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 50,
  message: { error: 'Too many auth attempts' }
});
app.use('/api/auth/', authLimiter);

app.use(express.json({ limit: '2mb' }));
app.use(cors({
  origin: process.env.NODE_ENV === 'production' 
    ? process.env.FRONTEND_URL 
    : ['http://localhost:3000', 'http://localhost:5000'],
  credentials: true
}));

// Connect to MongoDB if URI provided (safe default to localhost)
const mongoose = require('mongoose');
const MONGO_URI = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/phishing';
mongoose.set('bufferTimeoutMS', 5000);
mongoose.connect(MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true, serverSelectionTimeoutMS: 5000 })
	.then(() => console.log('Connected to MongoDB'))
	.catch((err) => console.warn('MongoDB connection warning:', err.message, '\nTo run locally, start MongoDB (see backend/.env.example or run `docker compose up -d mongodb`)'));

// Initialize scheduler and run startup initialization
setImmediate(() => {
  try {
    require('./services/scheduler');
    
    // Run startup initialization script
    console.log('Running startup initialization...');
    const { spawnSync } = require('child_process');
    const projectRoot = path.join(__dirname, '..');
    
    const initResult = spawnSync('python3', ['backend/scripts/startup_init.py'], {
      cwd: projectRoot,
      timeout: 180000, // 3 minutes for full initialization
      stdio: 'inherit' // Show output in console
    });
    
    if (initResult.status === 0) {
      console.log('✓ Startup initialization completed successfully');
    } else {
      console.warn('⚠ Startup initialization completed with warnings');
    }
    
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
app.use('/api/detections', (req, res, next) => loadRoute('./routes/detections')(req, res, next));
app.use('/api/ingest', (req, res, next) => loadRoute('./routes/ingest')(req, res, next));
app.use('/api/pentest', (req, res, next) => loadRoute('./routes/pentest')(req, res, next));
app.use('/api/collectors', (req, res, next) => loadRoute('./routes/collectors')(req, res, next));
app.use('/api/auth', (req, res, next) => loadRoute('./routes/auth')(req, res, next));
app.use('/api/admin', (req, res, next) => loadRoute('./routes/admin')(req, res, next));

// Serve static backend data (including generated ML dashboard image)
app.use('/backend/data', express.static(path.join(__dirname, 'data')));
// Serve static files from project root (for dashboard images)
app.use(express.static(path.join(__dirname, '..')));

// Global error handler
app.use((err, req, res, next) => {
  console.error('Error:', err.message);
  if (err.name === 'ValidationError') {
    return res.status(400).json({ error: 'Validation error', details: err.message });
  }
  if (err.name === 'CastError') {
    return res.status(400).json({ error: 'Invalid ID format' });
  }
  if (err.code === 11000) {
    return res.status(400).json({ error: 'Duplicate entry' });
  }
  res.status(500).json({ error: 'Internal server error' });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

const PORT = process.env.PORT || 5000;
const server = app.listen(PORT, () => {
  console.log(`Backend server listening on port ${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || 'development'}`);
});
server.timeout = 30000;

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');
  server.close(() => {
    console.log('Process terminated');
  });
});

module.exports = app;
