#!/usr/bin/env python3
"""Inference script: loads phishing_model.pkl, extracts features, returns JSON with
features, per-class probabilities, and a thresholded label.

Usage:
  python3 infer_phishing.py <url>
Environment:
  PHISH_THRESHOLD - probability threshold for phishing class (default 0.5)
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
    # Predict
    try:
        preds = model.predict(df)
    except Exception:
        preds = model.predict(df.values)
    phish_pred = int(preds[0])

    proba = None
    proba_phish = None
    class_probs = None
    try:
        if hasattr(model, 'predict_proba'):
            probs = model.predict_proba(df)
            # sklearn returns columns in the training class order; map to labels
            class_probs = {str(c): float(p) for c, p in zip(model.classes_, probs[0].tolist())}
            # phishing class probability (assume label '1' indicates phishing)
            phish_prob = class_probs.get('1') or class_probs.get(1) or None
            proba_phish = float(phish_prob) if phish_prob is not None else None
            proba = max(class_probs.values()) if class_probs else None
    except Exception:
        proba = None
        proba_phish = None

    # Apply threshold
    try:
        threshold = float(os.environ.get('PHISH_THRESHOLD', '0.5'))
    except Exception:
        threshold = 0.5
    if proba_phish is not None:
        label = 'PHISHING' if proba_phish >= threshold else 'LEGIT'
    else:
        label = 'PHISHING' if phish_pred == 1 else 'LEGIT'

    out = {
        'url': url,
        'features': feats,
        'prediction_raw': int(phish_pred),
        'prediction': label,
        'score': proba_phish,
        'class_probs': class_probs
    }
    print(json.dumps(out))


if __name__ == '__main__':
    main()
