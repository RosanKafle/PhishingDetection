import pandas as pd
import re
from collections import defaultdict
from datetime import datetime
from urllib.parse import urlparse

def hunt_apt_indicators():
    print("Debug: Starting hunt_apt_indicators()", flush=True)
    df = pd.read_csv('combined_threats_scored.csv')
    
    apt_indicators = {
        'suspicious_domains': [],
        'c2_patterns': [],
        'campaign_clusters': [],
        'ttp_analysis': []
    }
    
    for url in df['url']:
        domain = extract_domain(url)
        
        if is_dga_domain(domain):
            apt_indicators['suspicious_domains'].append({
                'domain': domain,
                'url': url,
                'indicator': 'Possible DGA domain',
                'confidence': 'medium'
            })
        
        if has_c2_patterns(url):
            apt_indicators['c2_patterns'].append({
                'url': url,
                'pattern': identify_c2_pattern(url),
                'confidence': 'high'
            })
    print(f"Debug: Found {len(apt_indicators['suspicious_domains'])} suspicious domains and {len(apt_indicators['c2_patterns'])} C2 patterns", flush=True)
    return apt_indicators

def hunt_campaign_clusters():
    print("Debug: Starting hunt_campaign_clusters()", flush=True)
    df = pd.read_csv('combined_threats_scored.csv')
    
    campaigns = defaultdict(list)
    
    for _, row in df.iterrows():
        url = row['url']
        domain = extract_domain(url)
        domain_key = get_domain_pattern(domain)
        campaigns[domain_key].append({
            'url': url,
            'domain': domain,
            'threat_score': row['threat_score'],
            'source': row['source']
        })
    
    significant_campaigns = {k: v for k, v in campaigns.items() if len(v) >= 5}
    print(f"Debug: Identified {len(significant_campaigns)} significant campaigns", flush=True)
    return significant_campaigns

def hunt_ttp_patterns():
    print("Debug: Starting hunt_ttp_patterns()", flush=True)
    df = pd.read_csv('combined_threats_scored.csv')
    
    ttp_patterns = {
        'phishing_kits': [],
        'malware_families': [],
        'evasion_techniques': []
    }
    
    for url in df['url']:
        if '/wp-admin/' in url or '/admin/' in url:
            ttp_patterns['phishing_kits'].append({
                'url': url,
                'technique': 'Admin panel abuse',
                'mitre_id': 'T1190'
            })
        if is_url_shortener(url):
            ttp_patterns['evasion_techniques'].append({
                'url': url,
                'technique': 'URL shortening evasion',
                'mitre_id': 'T1027'
            })
    print(f"Debug: Found {len(ttp_patterns['phishing_kits'])} phishing kits and {len(ttp_patterns['evasion_techniques'])} evasion techniques", flush=True)
    return ttp_patterns

def generate_threat_hunt_report():
    print("Debug: Generating threat hunting report...", flush=True)
    apt_indicators = hunt_apt_indicators()
    campaigns = hunt_campaign_clusters()
    ttp_patterns = hunt_ttp_patterns()
    
    report = f"""
# THREAT HUNTING REPORT
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## APT INDICATORS DISCOVERED
- Suspicious Domains: {len(apt_indicators['suspicious_domains'])}
- C2 Patterns: {len(apt_indicators['c2_patterns'])}

## CAMPAIGN CLUSTERS IDENTIFIED
- Active Campaigns: {len(campaigns)}
- Total URLs in Campaigns: {sum(len(v) for v in campaigns.values())}

## TTP ANALYSIS
- Phishing Kits: {len(ttp_patterns['phishing_kits'])}
- Evasion Techniques: {len(ttp_patterns['evasion_techniques'])}

## DETAILED FINDINGS
"""

    for campaign_id, urls in list(campaigns.items())[:5]:
        report += f"\n### Campaign: {campaign_id}\n"
        report += f"- URLs: {len(urls)}\n"
        report += f"- Avg Score: {sum(u['threat_score'] for u in urls)/len(urls):.1f}\n"
        report += f"- Sources: {set(u['source'] for u in urls)}\n"
    
    filename = f'threat_hunt_report_{datetime.now().strftime("%Y%m%d")}.md'
    with open(filename, 'w') as f:
        f.write(report)
    print(f"Debug: Threat hunt report saved to {filename}", flush=True)
    
    return report

# Helper functions
def extract_domain(url):
    try:
        return urlparse(url).netloc
    except Exception:
        return ''

def is_dga_domain(domain):
    if not domain:
        return False
    consonant_ratio = sum(1 for c in domain if c in 'bcdfghjklmnpqrstvwxyz') / len(domain)
    has_numbers = any(c.isdigit() for c in domain)
    return consonant_ratio > 0.6 and has_numbers

def has_c2_patterns(url):
    c2_patterns = [
        r'/[a-f0-9]{32}',
        r'/\d{10,}',
        r'\.php\?[a-z]=\d+'
    ]
    return any(re.search(pattern, url) for pattern in c2_patterns)

def identify_c2_pattern(url):
    if re.search(r'/[a-f0-9]{32}', url):
        return 'Hex ID communication'
    elif re.search(r'/\d{10,}', url):
        return 'Timestamp-based communication'
    else:
        return 'Suspicious parameters'

def get_domain_pattern(domain):
    if not domain:
        return 'unknown'
    parts = domain.split('.')
    if len(parts) >= 2:
        return '.'.join(parts[-2:])
    return domain

def is_url_shortener(url):
    shorteners = ['bit.ly', 'tinyurl.com', 't.co', 'goo.gl', 'ow.ly']
    return any(short in url for short in shorteners)

if __name__ == "__main__":
    report = generate_threat_hunt_report()
    print("Threat hunting report generated!", flush=True)
    print(report[:500] + "...", flush=True)
    input("Press Enter to exit...")
