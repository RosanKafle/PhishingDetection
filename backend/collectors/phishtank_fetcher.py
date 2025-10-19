#!/usr/bin/env python3
"""
PhishTank threat collector - fetches latest phishing URLs and saves to MongoDB
"""
import requests
import json
import csv
import os
import sys
from datetime import datetime
from pymongo import MongoClient
from urllib.parse import urlparse

# Configuration
PHISHTANK_URL = "http://data.phishtank.com/data/online-valid.csv"
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017/phishing')

def fetch_phishtank_data():
    """Fetch latest PhishTank data"""
    try:
        print(f"Fetching PhishTank data from {PHISHTANK_URL}")
        response = requests.get(PHISHTANK_URL, timeout=30)
        response.raise_for_status()
        
        # Parse CSV data
        lines = response.text.strip().split('\n')
        reader = csv.DictReader(lines)
        
        threats = []
        for row in reader:
            if row.get('url'):
                threats.append({
                    'url': row['url'],
                    'source': 'phishtank',
                    'timestamp': datetime.now(),
                    'status': 'new',
                    'features': {
                        'phish_id': row.get('phish_id'),
                        'submission_time': row.get('submission_time'),
                        'verified': row.get('verified'),
                        'verification_time': row.get('verification_time')
                    },
                    'score': 0.8  # High confidence for PhishTank verified URLs
                })
        
        return threats
    except Exception as e:
        print(f"Error fetching PhishTank data: {e}")
        return []

def save_to_mongodb(threats):
    """Save threats to MongoDB"""
    try:
        client = MongoClient(MONGO_URI)
        db = client.phishing
        collection = db.threats
        
        # Insert new threats (avoid duplicates by URL)
        inserted = 0
        for threat in threats:
            existing = collection.find_one({'url': threat['url']})
            if not existing:
                collection.insert_one(threat)
                inserted += 1
        
        print(f"Inserted {inserted} new threats from {len(threats)} total")
        client.close()
        return inserted
    except Exception as e:
        print(f"Error saving to MongoDB: {e}")
        return 0

def main():
    print(f"PhishTank collector started at {datetime.now()}")
    
    # Fetch data
    threats = fetch_phishtank_data()
    if not threats:
        print("No threats fetched")
        return
    
    # Save to database
    inserted = save_to_mongodb(threats)
    
    print(f"PhishTank collector completed. Processed {len(threats)} threats, inserted {inserted} new ones")

if __name__ == "__main__":
    main()