const cron = require('node-cron');
const { spawnSync } = require('child_process');
const path = require('path');
const { writeCache } = require('./cache');

const projectRoot = path.join(__dirname, '..', '..');

function runMLWrapper() {
  const script = path.join(projectRoot, 'backend', 'scripts', 'run_ml_and_render.py');
  const result = spawnSync('python3', [script], { 
    cwd: projectRoot, 
    timeout: 180000, 
    maxBuffer: 10 * 1024 * 1024 
  });
  
  const stdout = result.stdout ? result.stdout.toString() : '';
  const stderr = result.stderr ? result.stderr.toString() : '';
  let payload = { ok: result.status === 0, stdout, stderr, ts: Date.now() };
  
  try {
    // wrapper prints JSON; parse if possible
    const j = JSON.parse(stdout);
    payload.metrics = j.metrics;
    payload.image = j.image;
  } catch (e) {}
  
  writeCache('ml_metrics', payload);
  return payload;
}

function runThreatCollectors() {
  console.log('[scheduler] running threat collectors');
  
  // Run PhishTank collector
  const phishtankScript = path.join(__dirname, '..', 'collectors', 'phishtank_fetcher.py');
  const phishtankResult = spawnSync('python3', [phishtankScript], { 
    cwd: projectRoot, 
    timeout: 120000, 
    maxBuffer: 10 * 1024 * 1024 
  });
  
  // Run URLHaus collector
  const urlhausScript = path.join(__dirname, '..', 'collectors', 'urlhaus_fetcher.py');
  const urlhausResult = spawnSync('python3', [urlhausScript], { 
    cwd: projectRoot, 
    timeout: 120000, 
    maxBuffer: 10 * 1024 * 1024 
  });
  
  const payload = {
    phishtank: {
      ok: phishtankResult.status === 0,
      stdout: phishtankResult.stdout ? phishtankResult.stdout.toString() : '',
      stderr: phishtankResult.stderr ? phishtankResult.stderr.toString() : ''
    },
    urlhaus: {
      ok: urlhausResult.status === 0,
      stdout: urlhausResult.stdout ? urlhausResult.stdout.toString() : '',
      stderr: urlhausResult.stderr ? urlhausResult.stderr.toString() : ''
    },
    ts: Date.now()
  };
  
  writeCache('threat_collectors', payload);
  return payload;
}

// schedule: ML wrapper every day at 03:00
cron.schedule('0 3 * * *', () => {
  console.log('[scheduler] running ML wrapper');
  runMLWrapper();
});

// schedule: threat collectors every 6 hours
cron.schedule('0 */6 * * *', () => {
  runThreatCollectors();
});

// schedule: real-time threat collection every 2 hours
cron.schedule('0 */2 * * *', () => {
  console.log('[scheduler] running real-time threat collector');
  const script = path.join(__dirname, '..', '..', 'automated_threat_collector.py');
  const result = spawnSync('python3', [script], { 
    cwd: projectRoot, 
    timeout: 300000, 
    maxBuffer: 20 * 1024 * 1024 
  });
  
  const payload = {
    ok: result.status === 0,
    stdout: result.stdout ? result.stdout.toString() : '',
    stderr: result.stderr ? result.stderr.toString() : '',
    ts: Date.now()
  };
  
  writeCache('realtime_threats', payload);
});

// export for manual triggers
module.exports = { runMLWrapper, runThreatCollectors };