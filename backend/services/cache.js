const fs = require('fs');
const path = require('path');

const CACHE_DIR = path.join(__dirname, '..', 'data', 'cache');
if (!fs.existsSync(CACHE_DIR)) fs.mkdirSync(CACHE_DIR, { recursive: true });

function readCache(name, ttlSeconds = 300) {
  const file = path.join(CACHE_DIR, name + '.json');
  if (!fs.existsSync(file)) return null;
  const st = fs.statSync(file);
  if ((Date.now() - st.mtimeMs) > ttlSeconds * 1000) return null;
  try { 
    return JSON.parse(fs.readFileSync(file, 'utf8')); 
  } catch (e) { 
    return null; 
  }
}

function writeCache(name, obj) {
  const file = path.join(CACHE_DIR, name + '.json');
  fs.writeFileSync(file, JSON.stringify(obj), 'utf8');
}

module.exports = { readCache, writeCache, CACHE_DIR };