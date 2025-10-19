#!/usr/bin/env python3
"""
URLHaus threat collector - fetches malicious URLs and saves to MongoDB
"""
import requests
import json
import csv
import os
from datetime import datetime
from pymongo import MongoClient

# Configuration
URLHAUS_URL = "https://urlhaus.abuse.ch/downloads/csv_recent/"
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://127.0.0.1:27017/phishing')

def fetch_urlhaus_data():
    """Fetch latest URLHaus data"""
    try:
        print(f"Fetching URLHaus data from {URLHAUS_URL}")
        response = requests.get(URLHAUS_URL, timeout=30)
        response.raise_for_status()
        
        # Parse CSV data (skip comment lines starting with #)
        lines = [line for line in response.text.strip().split('\n') if not line.startswith('#')]
        reader = csv.reader(lines)
        
        # Skip header
        next(reader, None)
        
        threats = []
        for row in reader:
            if len(row) >= 8 and row[2]:  # Check if URL exists
                threats.append({
                    'url': row[2],
                    'source': 'urlhaus',
                    'timestamp': datetime.now(),
                    'status': 'new',
                    'features': {
                        'id': row[0],
                        'dateadded': row[1],
                        'url_status': row[3],
                        'threat': row[4],
                        'tags': row[5],
                        'urlhaus_link': row[6],
                        'reporter': row[7]
                    },
                    'score': 0.7  # Medium-high confidence for URLHaus
                })
        
        return threats
    except Exception as e:
        print(f"Error fetching URLHaus data: {e}")
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
    print(f"URLHaus collector started at {datetime.now()}")
    
    # Fetch data
    threats = fetch_urlhaus_data()
    if not threats:
        print("No threats fetched")
        return
    
    # Save to database
    inserted = save_to_mongodb(threats)
    
    print(f"URLHaus collector completed. Processed {len(threats)} threats, inserted {inserted} new ones")

if __name__ == "__main__":
    main()