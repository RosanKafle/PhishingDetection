#!/usr/bin/env python3
"""Bulk debug inference helper.

Reads URLs from a file (one per line) passed as first arg, or from stdin if no arg.
For each URL it calls the local infer logic (by importing infer_phishing.extract_features and loading model)
and prints one JSON object per line with features, probs, and prediction to stdout.

This avoids repeated subprocess overhead and is useful to inspect many URLs quickly.
"""
import sys
import os
import json
import joblib
import pandas as pd

THIS_DIR = os.path.dirname(__file__)
PROJ = os.path.abspath(os.path.join(THIS_DIR, '..', '..'))
MODEL_PATH = os.path.join(PROJ, 'phishing_model.pkl')

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

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError('model not found at {}'.format(MODEL_PATH))
    return joblib.load(MODEL_PATH)

def infer_batch(urls):
    model = load_model()
    results = []
    for url in urls:
        url = url.strip()
        if not url:
            continue
        feats = extract_features(url)
        if feats is None:
            results.append({'url': url, 'error': 'feature extraction failed'})
            continue
        df = pd.DataFrame([feats])
        try:
            pred = int(model.predict(df)[0])
        except Exception:
            pred = int(model.predict(df.values)[0])
        class_probs = None
        phish_prob = None
        try:
            if hasattr(model, 'predict_proba'):
                probs = model.predict_proba(df)[0].tolist()
                class_probs = {str(c): float(p) for c, p in zip(model.classes_, probs)}
                phish_prob = class_probs.get('1') or class_probs.get(1) or None
        except Exception:
            class_probs = None
            phish_prob = None

        threshold = float(os.environ.get('PHISH_THRESHOLD', '0.5'))
        if phish_prob is not None:
            label = 'PHISHING' if phish_prob >= threshold else 'LEGIT'
        else:
            label = 'PHISHING' if pred == 1 else 'LEGIT'

        results.append({
            'url': url,
            'features': feats,
            'prediction_raw': pred,
            'prediction': label,
            'phish_prob': phish_prob,
            'class_probs': class_probs
        })
    return results

def main():
    # read from file if provided, else stdin
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        if not os.path.exists(path):
            print(json.dumps({'error': 'file not found', 'path': path}))
            return
        with open(path, 'r') as f:
            urls = [l.strip() for l in f.readlines() if l.strip()]
    else:
        urls = [l.strip() for l in sys.stdin.readlines() if l.strip()]

    res = infer_batch(urls)
    for r in res:
        print(json.dumps(r))

if __name__ == '__main__':
    main()
