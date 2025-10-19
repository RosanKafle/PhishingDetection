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

import sys
import json

def main():
    # Accept JSON input from stdin or as a file argument
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            input_data = json.load(f)
    else:
        input_data = json.load(sys.stdin)

    # input_data should be a list of cases or a single dict
    if isinstance(input_data, dict):
        cases = [input_data]
    else:
        cases = input_data

    results = []
    for case in cases:
        url = case.get('url')
        sources_count = case.get('sources_count', 1)
        api_results = case.get('api_results', {})
        score = calculate_threat_score(url, sources_count, api_results)
        level = classify_threat_level(score)
        results.append({
            'url': url,
            'threat_score': score,
            'threat_level': level
        })
    print(json.dumps(results))

if __name__ == "__main__":
    main()
