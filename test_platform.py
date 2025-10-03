#!/usr/bin/env python3
"""
Test script for the phishing detection platform
"""

import requests
import json
import os
import pandas as pd
from threat_scoring import calculate_threat_score, classify_threat_level

def test_files_exist():
    """Test that all required files are generated"""
    required_files = [
        'combined_threats.csv',
        'combined_threats_scored.csv', 
        'ml_features_dataset.csv',
        'threat_intelligence_dashboard.png'
    ]
    
    print("Testing file generation...")
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            print(f"❌ {file} missing")
    
def test_data_quality():
    """Test data quality and consistency"""
    print("\nTesting data quality...")
    
    try:
        df = pd.read_csv('combined_threats_scored.csv')
        
        print(f"✅ Dataset contains {len(df)} records")
        print(f"✅ Columns: {df.columns.tolist()}")
        
        # Check for required columns
        required_cols = ['url', 'source', 'threat_score', 'threat_level']
        for col in required_cols:
            if col in df.columns:
                print(f"✅ Column '{col}' exists")
            else:
                print(f"❌ Column '{col}' missing")
        
        # Check data ranges
        if df['threat_score'].min() >= 0 and df['threat_score'].max() <= 100:
            print("✅ Threat scores in valid range (0-100)")
        else:
            print("❌ Threat scores out of range")
            
    except Exception as e:
        print(f"❌ Error testing data quality: {e}")

def test_threat_scoring():
    """Test threat scoring functions"""
    print("\nTesting threat scoring...")
    
    test_urls = [
        "http://paypal-secure.tk/login",
        "https://google.com",
        "http://suspicious-site.ml"
    ]
    
    for url in test_urls:
        try:
            score = calculate_threat_score(url)
            level = classify_threat_level(score)
            print(f"✅ {url} -> Score: {score}, Level: {level}")
        except Exception as e:
            print(f"❌ Error scoring {url}: {e}")

def test_api_endpoints():
    """Test API endpoints if server is running"""
    print("\nTesting API endpoints...")
    
    base_url = "http://localhost:5001/api"
    
    # Test endpoints
    endpoints = [
        ("/threats/recent", "GET"),
        ("/threats/stats", "GET")
    ]
    
    for endpoint, method in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=5)
            
            if response.status_code == 200:
                print(f"✅ {method} {endpoint} -> {response.status_code}")
            else:
                print(f"⚠️ {method} {endpoint} -> {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"⚠️ {method} {endpoint} -> API server not running")
        except Exception as e:
            print(f"❌ {method} {endpoint} -> Error: {e}")

def main():
    """Run all tests"""
    print("🧪 Testing Phishing Detection Platform")
    print("="*50)
    
    test_files_exist()
    test_data_quality()
    test_threat_scoring()
    test_api_endpoints()
    
    print("\n" + "="*50)
    print("✅ Testing completed!")

if __name__ == "__main__":
    main()
