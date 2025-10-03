import random

sms_companies = ['PayPal', 'Amazon', 'Bank of America', 'Netflix', 'Google']
sms_actions = ['update your information', 'confirm your transaction', 'reset your password',
               'verify your account', 'review your recent activity']

def generate_phishing_url():
    base_domains = ['banksecure', 'loginservice', 'apple-support', 'paypal-account', 'microsoft-support']
    keywords = ['secure', 'verify', 'update', 'login', 'reset', 'confirm']
    tlds = ['com', 'net', 'org', 'info', 'biz']
    return f"http://{random.choice(keywords)}-{random.choice(base_domains)}.{random.choice(tlds)}"

def generate_smishing_text():
    company = random.choice(sms_companies)
    action = random.choice(sms_actions)
    link = generate_phishing_url()
    return f"Dear Customer, Your {company} account requires attention. Please {action} at: {link}"

# Generate and print 10 smishing texts
for _ in range(10):
    print(generate_smishing_text())
