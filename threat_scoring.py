def analyze_url_patterns(url):
    """Simple heuristic URL pattern analysis returning a score 0-30"""
    score = 0
    
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq']
    brand_names = ['paypal', 'google', 'microsoft', 'apple']
    
    url_lower = url.lower()
    
    # Add points if URL uses suspicious TLDs
    if any(url_lower.endswith(tld) for tld in suspicious_tlds):
        score += 10
    
    # Add points if known brand names appear suspiciously
    if any(brand in url_lower for brand in brand_names):
        score += 15

    # Add points for presence of uncommon symbols or digits typical in phishing
    if any(char in url for char in ['@', '%', '?', '=']):
        score += 5

    return min(score, 30)

def calculate_threat_score(url, sources_count=1, api_results=None):
    """Calculate threat score 0-100"""
    if api_results is None:
        api_results = {'virustotal_malicious': 0, 'urlvoid_failed': False}
    
    score = 0
    
    # Source count weight (max 30 points)
    score += min(sources_count * 10, 30)
    
    # API validation weight (max 40 points)
    if api_results.get('virustotal_malicious', 0) > 0:
        score += 40
    elif api_results.get('urlvoid_failed', False):
        score += 25
    
    # URL pattern analysis (max 30 points)
    score += analyze_url_patterns(url)
    
    return min(score, 100)

def classify_threat_level(score):
    if score >= 80:
        return "CRITICAL"
    elif score >= 60:
        return "HIGH"
    elif score >= 40:
        return "MEDIUM"
    elif score >= 20:
        return "LOW"
    else:
        return "INFORMATIONAL"

if __name__ == "__main__":
    # Sample test cases
    
    test_cases = [
        {
            'url': 'http://paypal-secure.tk/login',
            'sources_count': 3,
            'api_results': {'virustotal_malicious': 5, 'urlvoid_failed': False}
        },
        {
            'url': 'http://google-support12345.ga/security',
            'sources_count': 1,
            'api_results': {'virustotal_malicious': 0, 'urlvoid_failed': True}
        },
        {
            'url': 'https://example.com/home',
            'sources_count': 0,
            'api_results': {'virustotal_malicious': 0, 'urlvoid_failed': False}
        }
    ]

    for case in test_cases:
        score = calculate_threat_score(case['url'], case['sources_count'], case['api_results'])
        level = classify_threat_level(score)
        print(f"URL: {case['url']}")
        print(f"Threat Score: {score} / 100")
        print(f"Threat Level: {level}\n")
