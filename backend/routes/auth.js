const express = require('express');
const router = express.Router();
const jwt = require('jsonwebtoken');
const User = require('../models/user');

const JWT_SECRET = process.env.JWT_SECRET || 'dev-secret-token';

// POST /api/auth/register
router.post('/register', async (req, res) => {
	try {
		const { username, email, password } = req.body;
		if (!username || !email || !password) return res.status(400).json({ error: 'Missing fields' });
		if (require('mongoose').connection.readyState === 1) {
			const existing = await User.findOne({ $or: [{ email }, { username }] });
			if (existing) return res.status(400).json({ error: 'User already exists' });
			const user = new User({ username, email, password });
			await user.save();
			return res.status(201).json({ message: 'User created' });
		}
		// Fallback to dev file store when MongoDB isn't available
		const devStore = require('../services/devUserStore');
		try {
			await devStore.createUser({ username, email, password });
			return res.status(201).json({ message: 'User created (dev store)' });
		} catch (e) {
			return res.status(400).json({ error: e.message });
		}
	} catch (err) {
		console.error('Register error:', err);
		return res.status(500).json({ error: 'Server error' });
	}
});

// POST /api/auth/login
router.post('/login', async (req, res) => {
	try {
		const { email, password } = req.body;
		if (!email || !password) return res.status(400).json({ error: 'Missing fields' });
		if (require('mongoose').connection.readyState === 1) {
			const user = await User.findOne({ email });
			if (!user) return res.status(400).json({ error: 'Invalid credentials' });
			const match = await user.comparePassword(password);
			if (!match) return res.status(400).json({ error: 'Invalid credentials' });
			const token = jwt.sign({ id: user._id, username: user.username }, JWT_SECRET, { expiresIn: '7d' });
			return res.json({ token });
		}
		// Fallback to dev file store
		const devStore = require('../services/devUserStore');
		const found = await devStore.findByEmail(email);
		if (!found) return res.status(400).json({ error: 'Invalid credentials' });
		const valid = await devStore.comparePassword(email, password);
		if (!valid) return res.status(400).json({ error: 'Invalid credentials' });
		// create a JWT with a dummy id
		const token = jwt.sign({ id: found.id || found.email, username: found.username }, JWT_SECRET, { expiresIn: '7d' });
		return res.json({ token });
	} catch (err) {
		console.error('Login error:', err);
		return res.status(500).json({ error: 'Server error' });
	}
});

module.exports = router;
