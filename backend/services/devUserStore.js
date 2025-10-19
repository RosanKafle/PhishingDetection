const fs = require('fs').promises;
const path = require('path');
const bcrypt = require('bcryptjs');

const FILE = path.join(__dirname, '..', 'data', 'dev_users.json');

async function ensureFile() {
  try {
    await fs.mkdir(path.dirname(FILE), { recursive: true });
    await fs.access(FILE);
  } catch (err) {
    // create empty array file
    await fs.writeFile(FILE, '[]', 'utf8');
  }
}

async function readAll() {
  await ensureFile();
  const raw = await fs.readFile(FILE, 'utf8');
  try {
    return JSON.parse(raw || '[]');
  } catch (err) {
    return [];
  }
}

async function writeAll(users) {
  await ensureFile();
  await fs.writeFile(FILE, JSON.stringify(users, null, 2), 'utf8');
}

async function findByEmail(email) {
  const users = await readAll();
  return users.find(u => u.email === email) || null;
}

async function findByUsername(username) {
  const users = await readAll();
  return users.find(u => u.username === username) || null;
}

async function createUser({ username, email, password }) {
  const existingEmail = await findByEmail(email);
  const existingUsername = await findByUsername(username);
  if (existingEmail || existingUsername) throw new Error('User already exists');
  const salt = await bcrypt.genSalt(10);
  const hash = await bcrypt.hash(password, salt);
  const users = await readAll();
  const user = { id: Date.now().toString(36), username, email, password: hash, createdAt: new Date().toISOString() };
  users.push(user);
  await writeAll(users);
  return user;
}

async function comparePassword(email, candidate) {
  const user = await findByEmail(email);
  if (!user) return false;
  return bcrypt.compare(candidate, user.password);
}

module.exports = { findByEmail, findByUsername, createUser, comparePassword };
