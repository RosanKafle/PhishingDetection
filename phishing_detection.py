# Import libraries for our phishing detector
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import re

# Step 1: Function to extract features from a URL (like in report)
def extract_features(url):
    try:
        # Features from report: URL length, suspicious keywords, HTTPS, special chars
        features = {
            'url_length': len(url),
            'has_login': 1 if 'login' in url.lower() else 0,
            'has_verify': 1 if 'verify' in url.lower() else 0,
            'is_https': 1 if url.lower().startswith('https') else 0,
            'special_chars': sum(url.count(c) for c in '@%#&'),
            'digit_ratio': sum(c.isdigit() for c in url) / max(len(url), 1)  # Avoid division by zero
        }
        return features
    except Exception as e:
        print(f"Error processing URL {url}: {e}")
        return None

# Step 2: Create sample dataset (mimics report's open-source threat feeds)
urls = [
    "https://google.com",           # Safe
    "http://g00gle-login.com",      # Phishing
    "https://paypal.com",           # Safe
    "http://secure-verify.net",     # Phishing
    "https://facebook.com",         # Safe
    "http://faceb00k-login.org",    # Phishing
    "http://bank-secure.com",       # Phishing
    "https://amazon.com",           # Safe
    "http://amaz0n-verify.com",     # Phishing
    "https://twitter.com"           # Safe
]
labels = [0, 1, 0, 1, 0, 1, 1, 0, 1, 0]  # 0=safe, 1=phishing

# Convert URLs to features
data = [extract_features(url) for url in urls]
data = [d for d in data if d is not None]  # Remove any failed extractions
df = pd.DataFrame(data)
df['is_phishing'] = labels[:len(data)]  # Match labels to valid data

# Step 3: Check if we have enough data
if df.empty:
    print("Error: No valid data after preprocessing. Check URLs.")
    exit()

# Step 4: Split features (X) and labels (y)
X = df.drop('is_phishing', axis=1)
y = df['is_phishing']

# Step 5: Split data: 80% train, 20% test
try:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
except ValueError as e:
    print(f"Error splitting data: {e}. Need more data points.")
    exit()

# Step 6: Train Random Forest with grid search (like report's tuning)
model = RandomForestClassifier(random_state=42)
param_grid = {
    'n_estimators': [10, 50, 100],  # Number of trees
    'max_depth': [None, 5, 10],     # Tree depth
    'min_samples_leaf': [1, 2]      # Min samples per leaf
}
grid_search = GridSearchCV(model, param_grid, cv=3, n_jobs=-1)
try:
    grid_search.fit(X_train, y_train)
except Exception as e:
    print(f"Error training model: {e}")
    exit()

# Step 7: Get best model and evaluate
best_model = grid_search.best_estimator_
predictions = best_model.predict(X_test)

# Step 8: Calculate and print metrics (like report)
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
print("Confusion Matrix:\n", conf_matrix)

# Step 9: Save model for deployment (like report's API)
joblib.dump(best_model, 'phishing_model.pkl')
print("Model saved as 'phishing_model.pkl' for platform integration.")

# Step 10: Function to predict new URLs
def predict_url(url, model):
    features = extract_features(url)
    if features is None:
        return "Error: Invalid URL"
    features_df = pd.DataFrame([features])
    prediction = model.predict(features_df)[0]
    return "Phishing (BAD!)" if prediction == 1 else "Safe (Good!)"

# Test a new URL
test_url = "http://secure-login-bank.com"
print(f"Testing URL: {test_url}")
print(f"Prediction: {predict_url(test_url, best_model)}")