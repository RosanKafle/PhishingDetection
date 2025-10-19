## PhishingDetection — Integration Guide (roles: Threat Intel, Full-Stack, Security Data Scientist, PenTest)

This document lists the APIs, database schemas, code artifacts, and example snippets required to integrate components developed by Threat Intelligence (Pabin), Full-Stack (Bishal), Security Data Scientist (you), and Penetration Tester (Roshan).

Notes:
- The ML Engineer role is intentionally excluded from implementation details here; integration points (db tables / API contracts) are included so their outputs can be consumed.
- Where the repo already contains files, references are provided. New files or code snippets below are suggestions to add to the project.

---

## 1) Quick inventory

- Data ingestion / collectors:
  - `automated_threat_collector.py` (present)
  - `threat_api.py` (present)
  - `python_api_server.py` (present, exposes `/api/run_script` to run Python scripts)

- Analytics / scoring:
  - `threat_scoring.py` (present)
  - `score_combined_threats.py`, `ml_data_pipeline.py`, `score_combined_threats.py` (present)

- Data files:
  - `combined_threats.csv`, `combined_threats_scored.csv` (present)

- Frontend / Dashboard:
  - React app under top-level `src/` and `public/` (present)
  - KPI panel and detection UI (present)

If you added new files recently, list them here and confirm paths so I can wire them in code snippets.

---

## 2) Missing / recommended files to add

- `backend/` (Express app) — if your repo doesn't have a persistent backend folder, create one with routes, models and middleware.
  - `backend/routes/analytics.js` — endpoints for KPI, trends, check-phishing
  - `backend/routes/ingest.js` — endpoint for threat collectors to POST normalized rows
  - `backend/routes/pentest.js` — upload pentest results
  - `backend/models/threat.js`, `backend/models/pentestReport.js`, `backend/models/analyticsKPI.js` — Mongoose models
  - `backend/services/pythonRunner.js` — helper to call `python_api_server.py` or spawn Python scripts safely

- `integration/` documentation (this file)

---

## 3) API contracts (JSON) — canonical endpoints

1) Threat ingest (Threat Intelligence → Backend)

POST /api/ingest/threat
Request body (application/json):

{
  "source": "openphish",
  "url": "https://example-phish.test/login",
  "collected_at": "2025-10-01T12:34:56Z",
  "meta": { "ip": "1.2.3.4", "asn": "AS12345", "collector_id": "pabin-scraper-1" }
}

Response: 201 Created
{
  "id": "6423...",
  "status": "stored"
}

2) Check single link (Dashboard user check)

POST /api/analytics/check-phishing
Request:
{
  "url": "https://suspicious.example/"
}

Response (success):
{
  "url": "https://...",
  "threat_score": 67,
  "threat_level": "HIGH",
  "explain": "url contains brand name + suspicious tld"
}

3) KPI (Dashboard)

GET /api/analytics/kpi
Response:
{
  "detectionRate": "72.3%",
  "falsePositiveRate": "3.1%",
  "responseTime": "2.4s",
  "threatsProcessed": 12034,
  "uptime": "99.99%",
  "userSatisfaction": "4.7/5",
  "compliance": "OWASP Top 10: 9/10"
}

4) Pentest upload (from pentest systems)

POST /api/pentest/upload
Request (multipart JSON/attach):
{
  "campaign_id": "pentest-2025-09",
  "findings": [ { "url": "...", "severity": "HIGH", "notes": "clickjackable" } ],
  "reported_at": "2025-10-03T11:00:00Z"
}

Response: 201 Created + saved id

5) Python-run service (internal helper)

POST /api/python/run
Request to local `python_api_server.py` (internal only):
{
  "script": "threat_scoring.py",
  "args": []
}

Response:
{
  "stdout": "...",
  "stderr": "",
  "returncode": 0
}

---

## 4) Database schemas (MongoDB / Mongoose examples)

1) `threats` collection (file: `backend/models/threat.js`)

```js
const mongoose = require('mongoose');
const ThreatSchema = new mongoose.Schema({
  url: { type: String, required: true, index: true },
  source: String,
  collected_at: { type: Date, default: Date.now },
  normalized: Object,
  score: Number,
  level: String,
  meta: Object
}, { timestamps: true });
module.exports = mongoose.model('Threat', ThreatSchema);
```

2) `pentest_reports` collection (`backend/models/pentestReport.js`)

```js
const mongoose = require('mongoose');
const PentestSchema = new mongoose.Schema({
  campaign_id: String,
  findings: Array,
  reported_at: Date,
  meta: Object
}, { timestamps: true });
module.exports = mongoose.model('PentestReport', PentestSchema);
```

3) `analytics_kpis` (optional persisted KPIs)

```js
const AnalyticsKPISchema = new mongoose.Schema({
  date: { type: Date, default: Date.now },
  detectionRate: String,
  falsePositiveRate: String,
  threatsProcessed: Number,
  notes: String
});
module.exports = mongoose.model('AnalyticsKPI', AnalyticsKPISchema);
```

Note: `ml_predictions` schema is omitted by request, but include a pointer column `ml_prediction_id` on `threats` if linking predictions.

---

## 5) Example integration snippets

A) Node.js route calling the Python API (safe, HTTP to local Flask runner)

```js
// backend/services/pythonRunner.js
const axios = require('axios');
const PY_API = process.env.PY_API || 'http://localhost:8000/api/run_script';

async function runScript(script, args=[]) {
  const resp = await axios.post(PY_API, { script, args });
  if (resp.data.returncode !== 0) throw new Error('Script failed: ' + resp.data.stderr);
  return resp.data.stdout;
}

module.exports = { runScript };
```

Usage in route:

```js
const { runScript } = require('../services/pythonRunner');
router.post('/check-phishing', async (req, res) => {
  const { url } = req.body;
  try {
    const stdout = await runScript('threat_scoring.py', []);
    // if script reads stdin, use child_process instead — shown below
    res.json(JSON.parse(stdout)[0]);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});
```

B) Direct spawn to send JSON to a Python script that reads stdin

```js
const { spawn } = require('child_process');
function runScoring(cases) {
  return new Promise((resolve, reject) => {
    const py = spawn('python3', [path.join(__dirname, '../../threat_scoring.py')], { cwd: path.resolve(__dirname, '../../') });
    let out = '';
    let err = '';
    py.stdout.on('data', d => out += d);
    py.stderr.on('data', d => err += d);
    py.on('close', code => {
      if (code !== 0 || err) return reject(new Error(err || 'non-zero exit'));
      try { resolve(JSON.parse(out)); } catch(e) { reject(e); }
    });
    py.stdin.write(JSON.stringify(cases));
    py.stdin.end();
  });
}
```

---

## 6) Data quality / validation rules (Security Data Scientist responsibilities)

- Threat ingest validators:
  - Enforce URL canonicalization, reject blank/invalid URLs.
  - Normalize timestamps to UTC.
  - Add source provenance and minor fingerprint fields (host, path, query hash).

- Analytics scripts must handle empty arrays gracefully and return predictable JSON structures with error fields when needed.

---

## 7) Quick-test checklist

1. Start local Python runner (if using `python_api_server.py`):

```bash
python3 python_api_server.py
```

2. Start backend (Express) in `backend/`:

```bash
export NODE_ENV=development
node backend/server.js
```

3. Start frontend (from repo root if CRA):

```bash
npm start
```

4. Exercise endpoints with `curl` or Postman:

```bash
curl -X POST localhost:5000/api/analytics/check-phishing -H 'Content-Type: application/json' -d '{"url":"https://example.com"}'
curl localhost:5000/api/analytics/kpi
```

---

## 8) Next steps (I can implement these for you)

- Add `backend/` scaffolding (routes, models, service) and wire to existing Python scripts.
- Add unit and integration test skeletons for the endpoints above.
- Draft security/deployment checklist including Docker Compose and CI examples.

If you want, I can create the `backend/` skeleton files next and wire `/api/analytics/kpi` and `/api/analytics/check-phishing` to your existing `threat_scoring.py` and `combined_threats.csv`.

---

Document created: integration/INTEGRATION.md
