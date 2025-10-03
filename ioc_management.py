import pandas as pd
import re
import json
from urllib.parse import urlparse
from datetime import datetime

def extract_iocs(df):
    """Extract Indicators of Compromise from threat data"""
    print("Debug: Starting IOC extraction...")
    iocs = {
        'domains': [],
        'ips': [],
        'urls': [],
        'file_hashes': [],  
        'suspicious_patterns': []  
    }
    
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    
    for idx, url in enumerate(df['url']):
        if not isinstance(url, str):
            print(f"Warning: Skipping non-string URL at index {idx}: {url}")
            continue
        
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.strip()
            if domain:
                iocs['domains'].append(domain)
                print(f"Debug: Extracted domain '{domain}' from URL '{url}'")
        except Exception as e:
            print(f"Error parsing URL '{url}': {e}")
            continue
        
        
        try:
            ips = re.findall(ip_pattern, url)
            if ips:
                iocs['ips'].extend(ips)
                print(f"Debug: Found IPs {ips} in URL '{url}'")
        except Exception as e:
            print(f"Error finding IPs in URL '{url}': {e}")
        
        # Store full URL
        iocs['urls'].append(url)
    
    # Deduplicate IOC lists
    for key in iocs:
        before = len(iocs[key])
        iocs[key] = list(set(iocs[key]))
        after = len(iocs[key])
        print(f"Debug: Deduplicated '{key}', {before} -> {after} unique entries")
    
    return iocs

def generate_ioc_feed():
    print("Debug: Loading combined_threats_scored.csv for IOC generation...")
    try:
        df = pd.read_csv('combined_threats_scored.csv')
    except FileNotFoundError:
        print("Error: combined_threats_scored.csv not found. Run scoring script first.")
        return
    except Exception as e:
        print(f"Unexpected error loading CSV: {e}")
        return
    
    iocs = extract_iocs(df)
    
    # Save CSV format for domains (top 1000)
    try:
        ioc_df = pd.DataFrame([
            {'type': 'domain', 'value': domain, 'confidence': 'high'}
            for domain in iocs['domains'][:1000]
        ])
        ioc_df.to_csv('threat_iocs.csv', index=False)
        print("Debug: Saved threat_iocs.csv")
    except Exception as e:
        print(f"Error saving threat_iocs.csv: {e}")
    
    # Save simplified STIX JSON (top 100)
    try:
        stix_iocs = []
        for domain in iocs['domains'][:100]:
            stix_iocs.append({
                'type': 'domain-name',
                'value': domain,
                'labels': ['malicious-activity'],
                'created': datetime.now().isoformat()
            })
        with open('threat_iocs.json', 'w') as f:
            json.dump(stix_iocs, f, indent=2)
        print("Debug: Saved threat_iocs.json in STIX format")
    except Exception as e:
        print(f"Error saving threat_iocs.json: {e}")
    
    print(f"Generated IOCs summary: {len(iocs['domains'])} unique domains, {len(iocs['ips'])} unique IPs")
    
if __name__ == "__main__":
    generate_ioc_feed()
