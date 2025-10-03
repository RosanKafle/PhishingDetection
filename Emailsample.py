import random

email_subjects = [
    "Urgent: Verify Your Account Now",
    "Password Reset Required",
    "Unusual Activity Detected on Your Account",
    "Invoice Payment Overdue",
    "Congratulations! Claim Your Prize",
    "Account Suspension Warning",
    "Verify Your Payment Information"
]

email_bodies = [
    "We have noticed suspicious activity on your account. Please verify your details immediately by clicking the link below:",
    "Your account password needs to be reset due to a recent security breach. Click here to reset:",
    "An invoice is pending payment. Please review and pay immediately:",
    "Congratulations! You have been selected for a prize. Click below to claim:",
    "Unusual login attempt detected. Secure your account now by confirming your identity:",
    "Your account will be suspended unless you confirm your information:",
    "Please verify your recent payment to avoid service disruption:"
]

def generate_phishing_url():
    base_domains = ['banksecure', 'loginservice', 'apple-support', 'paypal-account', 'microsoft-support']
    keywords = ['secure', 'verify', 'update', 'login', 'reset', 'confirm']
    tlds = ['com', 'net', 'org', 'info', 'biz']
    return f"http://{random.choice(keywords)}-{random.choice(base_domains)}.{random.choice(tlds)}"

def create_phishing_email():
    recipient = "User"
    subject = random.choice(email_subjects)
    body = random.choice(email_bodies)
    link = generate_phishing_url()
    return f"Subject: {subject}\n\nDear {recipient},\n\n{body}\n{link}\n\nRegards,\nYour Security Team\n"

# Generate and print 10 phishing emails
for _ in range(10):
    print(create_phishing_email())
    print("="*50)
