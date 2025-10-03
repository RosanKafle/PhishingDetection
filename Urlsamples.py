import random

base_domains = ['banksecure', 'loginservice', 'apple-support', 'paypal-account', 'microsoft-support']
keywords = ['secure', 'verify', 'update', 'login', 'reset', 'confirm']
tlds = ['com', 'net', 'org', 'info', 'biz']

def generate_phishing_url():
    return f"http://{random.choice(keywords)}-{random.choice(base_domains)}.{random.choice(tlds)}"

# Generate 10 phishing URLs and print
for _ in range(10):
    print(generate_phishing_url())
