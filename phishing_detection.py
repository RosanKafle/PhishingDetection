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

# Step 2: Create larger, more realistic dataset
urls = [
    # Legitimate sites (20)
    "https://google.com", "https://facebook.com", "https://amazon.com", "https://microsoft.com",
    "https://apple.com", "https://twitter.com", "https://linkedin.com", "https://github.com",
    "https://stackoverflow.com", "https://wikipedia.org", "https://youtube.com", "https://gmail.com",
    "https://paypal.com", "https://ebay.com", "https://netflix.com", "https://spotify.com",
    "https://accounts.google.com", "https://login.facebook.com", "https://signin.amazon.com",
    "https://appleid.apple.com",
    
    # Phishing sites (15)
    "http://g00gle-login.com", "http://faceb00k-verify.net", "http://amaz0n-secure.org",
    "http://micr0soft-update.com", "http://apple-id-verify.net", "http://twitter-secure.org",
    "http://linkedin-account.com", "http://github-login.net", "http://paypal-verify.org",
    "http://ebay-secure.com", "http://netflix-account.net", "http://spotify-login.org",
    "http://secure-bank-login.suspicious.com", "https://verify-account.phishing.net",
    "http://update-now.malicious.com",
    
    # Borderline/sophisticated cases (10)
    "https://goog1e.com", "https://facebok.com", "https://arnazon.com",
    "http://microsoft-support.fake.com", "https://app1e.com", "https://twiter.com",
    "http://paypa1.com", "https://ebay-security.fake.net", "http://netf1ix.com",
    "http://192.168.1.1/login"
]

# More realistic labels with some classification challenges
labels = (
    [0] * 20 +  # Legitimate sites
    [1] * 15 +  # Clear phishing
    [1] * 10    # Sophisticated phishing
)

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

# Step 5: Split data: 70% train, 30% test (larger test set for better evaluation)
try:
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
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