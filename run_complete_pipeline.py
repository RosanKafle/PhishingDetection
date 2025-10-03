#!/usr/bin/env python3
"""
Complete Phishing Detection Platform Pipeline
Runs all components in the correct order
"""

import subprocess
import sys
import os
from datetime import datetime

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stderr:
            print(f"Stderr: {e.stderr}")
        return False

def main():
    """Run the complete pipeline"""
    print(f"Starting Complete Phishing Detection Platform Pipeline")
    print(f"Timestamp: {datetime.now()}")
    
    # Step 1: Collect threat data
    if not run_command("python3 automated_threat_collector.py", "Collecting threat data from OpenPhish and URLHaus"):
        print("Failed at data collection step")
        return False
    
    # Step 2: Add threat scoring
    if not run_command("python3 score_combined_threats.py", "Adding threat scores to dataset"):
        print("Failed at threat scoring step")
        return False
    
    # Step 3: Extract ML features
    if not run_command("python3 ml_data_pipeline.py", "Extracting ML features"):
        print("Failed at ML feature extraction step")
        return False
    
    # Step 4: Create dashboard
    if not run_command("python3 demo_dashboard.py", "Creating threat intelligence dashboard"):
        print("Failed at dashboard creation step")
        return False
    
    print(f"\n{'='*60}")
    print("✅ PIPELINE COMPLETED SUCCESSFULLY!")
    print(f"{'='*60}")
    print("Generated files:")
    print("  - combined_threats.csv (raw combined data)")
    print("  - combined_threats_scored.csv (with threat scores)")
    print("  - ml_features_dataset.csv (ML-ready features)")
    print("  - threat_intelligence_dashboard.png (visualization)")
    print("\nTo start the API server, run: python3 threat_api.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
