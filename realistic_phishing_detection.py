#!/usr/bin/env python3
"""
Realistic phishing detector with larger, more diverse dataset
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import re
from urllib.parse import urlparse

def extract_features(url):
    """Extract security-relevant features from URL"""
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        url_lower = url.lower()
        
        # Precompute common values for performance
        domain_parts = domain.split('.')
        suspicious_keywords = ['login', 'verify', 'secure', 'account', 'update']
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf']
        url_shorteners = ['bit.ly', 'tinyurl', 't.co']
        
        features = {
            'url_length': len(url),
            'domain_length': len(domain),
            'path_length': len(path),
            'is_https': 1 if url_lower.startswith('https') else 0,
            'special_chars': sum(url.count(c) for c in '@%#&'),
            'digit_ratio': sum(c.isdigit() for c in url) / max(len(url), 1),
            'subdomain_count': max(0, len(domain_parts) - 2),
            'has_ip': 1 if re.match(r'\d+\.\d+\.\d+\.\d+', domain) else 0,
            'suspicious_tld': 1 if any(tld in domain for tld in suspicious_tlds) else 0,
            'url_shortener': 1 if any(short in domain for short in url_shorteners) else 0
        }
        
        # Add keyword features
        for keyword in suspicious_keywords:
            features[f'has_{keyword}'] = 1 if keyword in url_lower else 0
            
        return features
    except Exception:
        return None

# Larger, more realistic dataset
urls = [
    # Legitimate sites
    "https://google.com", "https://facebook.com", "https://amazon.com", "https://microsoft.com",
    "https://apple.com", "https://twitter.com", "https://linkedin.com", "https://github.com",
    "https://stackoverflow.com", "https://wikipedia.org", "https://youtube.com", "https://gmail.com",
    "https://paypal.com", "https://ebay.com", "https://netflix.com", "https://spotify.com",
    
    # Phishing sites (realistic examples)
    "http://g00gle-login.com", "http://faceb00k-verify.net", "http://amaz0n-secure.org",
    "http://micr0soft-update.com", "http://apple-id-verify.net", "http://twitter-secure.org",
    "http://linkedin-account.com", "http://github-login.net", "http://paypal-verify.org",
    "http://ebay-secure.com", "http://netflix-account.net", "http://spotify-login.org",
    
    # Borderline cases (some legitimate, some suspicious)
    "https://accounts.google.com", "https://login.facebook.com", "https://signin.amazon.com",
    "http://support.microsoft.com", "https://appleid.apple.com", "http://help.twitter.com",
    "http://secure-bank-login.suspicious.com", "https://verify-account.phishing.net",
    "http://192.168.1.1/login", "https://bit.ly/suspicious", "http://update-now.tk",
    
    # More sophisticated phishing
    "https://goog1e.com/login", "https://facebok.com/verify", "https://arnazon.com/secure",
    "http://microsoft-support.ml", "https://app1e.com/id", "https://twiter.com/login",
    "http://paypa1.com/verify", "https://ebay-security.ga", "http://netf1ix.com/account"
]

# More nuanced labels (some borderline cases)
labels = [
    # Legitimate (16)
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    # Clear phishing (12) 
    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    # Borderline cases (11) - mix of legitimate and suspicious
    0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1,
    # Sophisticated phishing (9)
    1, 1, 1, 1, 1, 1, 1, 1, 1
]

# Convert to features
data = []
valid_labels = []
for i, url in enumerate(urls):
    features = extract_features(url)
    if features is not None:
        data.append(features)
        valid_labels.append(labels[i])

df = pd.DataFrame(data)
df['is_phishing'] = valid_labels

# Split features and labels
X = df.drop('is_phishing', axis=1)
y = df['is_phishing']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Train model with optimized grid search
model = RandomForestClassifier(random_state=42)
param_grid = {
    'n_estimators': [50, 100],  # Reduced for performance
    'max_depth': [10, 20],
    'min_samples_leaf': [1, 2],
    'min_samples_split': [2, 5]
}

grid_search = GridSearchCV(
    model, param_grid, cv=3, scoring='f1', n_jobs=-1  # Reduced CV folds
)
grid_search.fit(X_train, y_train)

# Evaluate
best_model = grid_search.best_estimator_
predictions = best_model.predict(X_test)

# Calculate metrics
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, zero_division=0)
recall = recall_score(y_test, predictions, zero_division=0)
f1 = f1_score(y_test, predictions, zero_division=0)
conf_matrix = confusion_matrix(y_test, predictions)

print("Phishing Detector Results:")
print(f"Accuracy: {accuracy * 100:.1f}%")
print(f"Precision: {precision * 100:.1f}%")
print(f"Recall: {recall * 100:.1f}%")
print(f"F1-Score: {f1 * 100:.1f}%")
print(f"Best Hyperparameters: {grid_search.best_params_}")
print("Confusion Matrix:")
print(conf_matrix)

# Save model
joblib.dump(best_model, 'phishing_model.pkl')
print("Model saved as 'phishing_model.pkl' for platform integration.")

# Test prediction function
def predict_url(url, model):
    features = extract_features(url)
    if features is None:
        return "Error: Invalid URL"
    features_df = pd.DataFrame([features])
    prediction = model.predict(features_df)[0]
    probability = model.predict_proba(features_df)[0]
    confidence = max(probability)
    return f"{'Phishing (BAD!)' if prediction == 1 else 'Safe (Good!)'} (confidence: {confidence:.2f})"

# Test URLs
test_url = "http://secure-login-bank.com"
print(f"Testing URL: {test_url}")
print(f"Prediction: {predict_url(test_url, best_model)}")