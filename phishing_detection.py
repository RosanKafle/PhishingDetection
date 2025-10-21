# Import libraries for our phishing detector
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import joblib
import re

# Step 1: Enhanced function to extract features from a URL
def extract_features(url):
    try:
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
    
    # Phishing sites with Kaggle patterns (25)
    "http://g00gle-login.com", "http://faceb00k-verify.net", "http://amaz0n-secure.org",
    "http://micr0soft-update.com", "http://apple-id-verify.net", "http://twitter-secure.org",
    "http://linkedin-account.com", "http://github-login.net", "http://paypal-verify.org",
    "http://ebay-secure.com", "http://netflix-account.net", "http://spotify-login.org",
    "http://secure-bank-login.suspicious.com", "https://verify-account.phishing.net",
    "http://update-now.malicious.com",
    "premierpaymentprocessing.com/includes/boleto-2via-07-2012.php",
    "serviciosbys.com/paypal.cgi.bin.get-into.herf.secure.dispatch35463256rzr321654641dsf654321874/href/href/href/secure/center/update/limit/seccure/4d7a1ff5c55825a2e632a679c2fd5353/",
    "mail.printakid.com/www.online.americanexpress.com/index.html",
    "www.dghjdgf.com/paypal.co.uk/cycgi-bin/webscrcmd=_home-customer&nav=1/loading.php",
    "myxxxcollection.com/v1/js/jih321/bpd.com.do/do/l.popular.php",
    "docs.google.com/spreadsheet/viewform?formkey=dE5rVEdSV2pBdkpSRy11V3o2eDdwbnc6MQ",
    "www.coincoele.com.br/Scripts/smiles/?pt-br/Paginas/default.aspx",
    "lingshc.com/old_aol.1.3/?Login=&Lis=10&LigertID=1993745&us=1",
    "www.avedeoiro.com/site/plugins/chase/",
    "asladconcentration.com/paplkuk1/webscrcmd=_home-customer&nav=1/",
    
    # Sophisticated cases (15)
    "https://goog1e.com", "https://facebok.com", "https://arnazon.com",
    "http://microsoft-support.fake.com", "https://app1e.com", "https://twiter.com",
    "http://paypa1.com", "https://ebay-security.fake.net", "http://netf1ix.com",
    "http://192.168.1.1/login", "https://accounts-google.com", "https://login-facebook.com",
    "https://signin-amazon.com", "https://appleid-apple.com", "https://secure-paypal.com"
]

labels = (
    [0] * 20 +  # Legitimate sites
    [1] * 25 +  # Phishing with Kaggle patterns
    [1] * 15    # Sophisticated phishing
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

# Step 6: Train Random Forest optimized for high recall
model = RandomForestClassifier(random_state=42, class_weight='balanced')
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 15],
    'min_samples_leaf': [1, 2],
    'min_samples_split': [2, 5]
}
grid_search = GridSearchCV(model, param_grid, cv=3, n_jobs=-1, scoring='recall')
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