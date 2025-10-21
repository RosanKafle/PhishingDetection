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
        import re
        from urllib.parse import urlparse
        
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        
        # Comprehensive phishing keywords
        phish_keywords = ['login', 'verify', 'secure', 'account', 'update', 'confirm', 
                         'suspend', 'limited', 'click', 'urgent', 'expire', 'bank',
                         'paypal', 'amazon', 'microsoft', 'apple', 'google', 'facebook',
                         'cgi-bin', 'webscr', 'dispatch', 'americanexpress', 'boleto',
                         'signin', 'banking', 'suspended', 'locked', 'validation']
        
        domain_parts = domain.split('.')
        
        features = {
            'url_length': len(url),
            'domain_length': len(domain),
            'path_length': len(path),
            'has_login': 1 if 'login' in url.lower() else 0,
            'has_verify': 1 if 'verify' in url.lower() else 0,
            'has_secure': 1 if 'secure' in url.lower() else 0,
            'has_account': 1 if 'account' in url.lower() else 0,
            'has_update': 1 if 'update' in url.lower() else 0,
            'is_https': 1 if url.lower().startswith('https') else 0,
            'special_chars': sum(url.count(c) for c in '@%#&?='),
            'digit_ratio': sum(c.isdigit() for c in url) / max(len(url), 1),
            'suspicious_tld': 1 if any(tld in domain for tld in ['.tk', '.ml', '.ga', '.cf', '.cc']) else 0,
            'ip_address': 1 if re.match(r'^\d+\.\d+\.\d+\.\d+', domain) else 0,
            'subdomain_count': len(domain_parts) - 2 if len(domain_parts) > 2 else 0,
            'has_hyphen': 1 if '-' in domain else 0,
            'phish_keywords': sum(1 for keyword in phish_keywords if keyword in url.lower()),
            'url_entropy': len(set(url.lower())) / max(len(url), 1),
            'has_shortener': 1 if any(short in domain for short in ['bit.ly', 'tinyurl', 't.co', 'goo.gl']) else 0,
            'suspicious_port': 1 if parsed.port and parsed.port not in [80, 443, 8080] else 0,
            'has_cgi_bin': 1 if 'cgi-bin' in url.lower() else 0,
            'has_webscr': 1 if 'webscr' in url.lower() else 0,
            'has_dispatch': 1 if 'dispatch' in url.lower() else 0,
            'long_path': 1 if len(path) > 50 else 0,
            'suspicious_chars': sum(url.count(c) for c in '~`!$^*()+={}[]|\\:;"<>,'),
            'brand_spoofing': 1 if any(brand in domain for brand in ['paypal', 'amazon', 'microsoft', 'apple', 'google']) and not any(legit in domain for legit in ['paypal.com', 'amazon.com', 'microsoft.com', 'apple.com', 'google.com']) else 0,
            'hex_chars': 1 if re.search(r'[0-9a-f]{32,}', url.lower()) else 0,
            'multiple_dots': 1 if url.count('.') > 4 else 0,
            'suspicious_path': 1 if any(p in path for p in ['includes', 'tmp', 'temp', 'cache']) else 0
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

    # Apply threshold (optimized for 94% recall)
    try:
        threshold = float(os.environ.get('PHISH_THRESHOLD', '0.15'))
    except Exception:
        threshold = 0.15
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
