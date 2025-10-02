const jwt = require('jsonwebtoken');

// Verifies JWT and attaches user payload to req.user
module.exports = {
  protect: (req, res, next) => {
    try {
      const authHeader = req.headers.authorization || '';
      const token = authHeader.startsWith('Bearer ') ? authHeader.slice(7) : null;
      if (!token) {
        return res.status(401).json({ error: 'Not authorized, token missing' });
      }
      const decoded = jwt.verify(token, process.env.JWT_SECRET);
      req.user = { id: decoded.id, isAdmin: !!decoded.isAdmin };
      next();
    } catch (err) {
      return res.status(401).json({ error: 'Not authorized, token invalid' });
    }
  },

  adminOnly: (req, res, next) => {
    if (!req.user?.isAdmin) {
      return res.status(403).json({ error: 'Admin access required' });
    }
    next();
  }
};



