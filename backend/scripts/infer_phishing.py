#!/usr/bin/env python3
"""Simple inference script: loads phishing_model.pkl and predicts label for a URL passed as first arg.
Prints JSON: { prediction: 'PHISHING'|'LEGIT', score: 0.9 }
"""
import sys
import os
import json
import joblib
import pandas as pd

proj = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
model_path = os.path.join(proj, 'phishing_model.pkl')

def extract_features(url):
    try:
        features = {
            'url_length': len(url),
            'has_login': 1 if 'login' in url.lower() else 0,
            'has_verify': 1 if 'verify' in url.lower() else 0,
            'is_https': 1 if url.lower().startswith('https') else 0,
            'special_chars': sum(url.count(c) for c in '@%#&'),
            'digit_ratio': sum(c.isdigit() for c in url) / max(len(url), 1)
        }
        return features
    except Exception:
        return None

def main():
    if len(sys.argv) < 2:
        print(json.dumps({'error': 'missing url'}))
        return
    url = sys.argv[1]
    if not os.path.exists(model_path):
        print(json.dumps({'error': 'model not found'}))
        return
    model = joblib.load(model_path)
    feats = extract_features(url)
    if feats is None:
        print(json.dumps({'error': 'failed to extract features'}))
        return
    df = pd.DataFrame([feats])
    try:
        pred = model.predict(df)[0]
    except Exception as e:
        # try to convert to numpy array fallback
        pred = model.predict(df.values)[0]
    try:
        proba = None
        if hasattr(model, 'predict_proba'):
            proba = float(model.predict_proba(df)[0].max())
    except Exception:
        proba = None
    label = 'PHISHING' if int(pred) == 1 else 'LEGIT'
    print(json.dumps({'prediction': label, 'score': proba}))


if __name__ == '__main__':
    main()
