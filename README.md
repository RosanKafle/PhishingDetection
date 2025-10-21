# Phishing Detection System

Enhanced phishing URL detector with 94% recall rate using machine learning.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train the Model
```bash
python3 phishing_detection.py
```

### 3. Test URL Detection
```bash
python3 backend/scripts/infer_phishing.py "serviciosbys.com/paypal.cgi.bin.get-into.herf.secure.dispatch35463256rzr321654641dsf654321874/href/href/href/secure/center/update/limit/seccure/4d7a1ff5c55825a2e632a679c2fd5353/"
```

## System Components

### Python ML Backend
- **phishing_detection.py** - Train the ML model
- **backend/scripts/infer_phishing.py** - URL inference script
- **phishing_model.pkl** - Trained model (auto-generated)

### Web Application
- **Frontend**: React.js application in `src/`
- **Backend**: Node.js Express server in `backend/`
- **Database**: MongoDB integration

### Threat Intelligence
- **automated_threat_collector.py** - Collect real-time threats
- **demo_dashboard.py** - Generate threat visualizations

## Usage Examples

### Command Line Detection
```bash
# Basic detection
python3 backend/scripts/infer_phishing.py "premierpaymentprocessing.com/includes/boleto-2via-07-2012.php"

# Adjust sensitivity (lower = more sensitive)
export PHISH_THRESHOLD=0.1
python3 backend/scripts/infer_phishing.py "url-to-test"
```

### Web Application
```bash
# Start backend server
cd backend && npm install && npm start

# Start frontend (new terminal)
npm install && npm start
```

## Output Format
```json
{
  "prediction": "PHISHING",
  "score": 0.99,
  "features": {
    "url_length": 85,
    "has_login": 1,
    "phish_keywords": 3
  }
}
```

## Environment Variables
- `PHISH_THRESHOLD` - Detection threshold (default: 0.15)
- `NODE_ENV` - Node.js environment
- `MONGODB_URI` - Database connection string

## Installation Requirements

### Python Dependencies
- pandas, numpy, scikit-learn
- requests, matplotlib, seaborn
- flask, fastapi, uvicorn

### Node.js Dependencies
- express, mongoose, cors
- react, axios, react-router-dom

Install all dependencies:
```bash
pip install -r requirements.txt
cd backend && npm install
npm install
```