import pandas as pd
import re

def extract_domain(url):
    """Extract domain from URL"""
    try:
        if '//' in url:
            domain = url.split('//')[1].split('/')[0]
            print(f"Debug: Extracted domain '{domain}' from URL '{url}'")
            return domain
        domain = url.split('/')[0]
        print(f"Debug: Extracted domain '{domain}' from URL '{url}'")
        return domain
    except Exception as e:
        print(f"Error extracting domain from URL '{url}': {e}")
        return ''

def count_subdomains(url):
    try:
        domain = extract_domain(url)
        subdomain_count = domain.count('.')
        print(f"Debug: Subdomain count {subdomain_count} for domain '{domain}'")
        return subdomain_count
    except Exception as e:
        print(f"Error counting subdomains for URL '{url}': {e}")
        return 0

def count_path_depth(url):
    try:
        if '//' in url:
            parts = url.split('//')[1].split('/', 1)
            if len(parts) > 1:
                path_depth = parts[1].count('/') + 1
                print(f"Debug: Path depth {path_depth} for URL '{url}'")
                return path_depth
        print(f"Debug: Path depth 0 for URL '{url}'")
        return 0
    except Exception as e:
        print(f"Error counting path depth for URL '{url}': {e}")
        return 0

def prepare_ml_features():
    """Extract features for ML team"""
    try:
        df = pd.read_csv('combined_threats_scored.csv')
        print(f"Loading {len(df)} URLs for feature extraction...")

        # Basic URL features
        df['url_length'] = df['url'].str.len()
        df['has_https'] = df['url'].str.contains('https', case=False)
        df['has_ip_address'] = df['url'].str.contains(r'\d+\.\d+\.\d+\.\d+')

        # Suspicious patterns
        df['suspicious_tld'] = df['url'].str.contains(r'\.tk|\.ml|\.ga|\.cf|\.gq', case=False)
        df['brand_spoofing'] = df['url'].str.contains('paypal|google|microsoft|apple|amazon|facebook', case=False)

        # URL structure analysis
        df['subdomain_count'] = df['url'].apply(count_subdomains)
        df['path_depth'] = df['url'].apply(count_path_depth)
        df['special_chars'] = df['url'].str.count(r'[^a-zA-Z0-9._/\-]')
        df['digit_count'] = df['url'].str.count(r'\d')

        # Domain features
        df['domain'] = df['url'].apply(extract_domain)
        df['domain_length'] = df['domain'].str.len()

        # Save ML-ready dataset
        df.to_csv('ml_features_dataset.csv', index=False)

        # Print data info and sample for confirmation
        print(f"Prepared ML features dataset with {len(df)} records")
        print(f"Features extracted: {df.columns.tolist()}")
        print("\nSample features:")
        print(df[['url', 'url_length', 'has_https', 'suspicious_tld', 'brand_spoofing', 'threat_score']].head())

        return df

    except FileNotFoundError:
        print("Error: combined_threats_scored.csv not found. Please run the scoring script first.")
        return None
    except Exception as e:
        print(f"Error in feature extraction: {e}")
        return None

if __name__ == "__main__":
    prepare_ml_features()
