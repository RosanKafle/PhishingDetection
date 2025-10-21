#!/usr/bin/env python3
"""
Startup initialization script to ensure all components are ready
"""
import os
import sys
import subprocess
import json

def run_script(script_path, timeout=60):
    """Run a Python script and return success status"""
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, 
                              timeout=timeout, cwd=os.path.dirname(script_path))
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)

def main():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    # 1. Ensure phishing model exists
    model_path = os.path.join(project_root, 'phishing_model.pkl')
    if not os.path.exists(model_path):
        print("Training phishing model...")
        success, stdout, stderr = run_script(os.path.join(project_root, 'phishing_detection.py'), 120)
        if success:
            print("✓ Phishing model trained successfully")
        else:
            print(f"✗ Phishing model training failed: {stderr}")
    else:
        print("✓ Phishing model already exists")
    
    # 2. Generate ML dashboard
    print("Generating ML dashboard...")
    success, stdout, stderr = run_script(os.path.join(project_root, 'backend/scripts/run_ml_and_render.py'))
    if success:
        print("✓ ML dashboard generated successfully")
    else:
        print(f"✗ ML dashboard generation failed: {stderr}")
    
    # 3. Generate threat intelligence dashboard
    print("Generating threat intelligence dashboard...")
    success, stdout, stderr = run_script(os.path.join(project_root, 'demo_dashboard.py'))
    if success:
        print("✓ Threat intelligence dashboard generated successfully")
    else:
        print(f"✗ Threat intelligence dashboard generation failed: {stderr}")
    
    # 4. Test URL inference
    print("Testing URL inference...")
    test_url = "http://secure-login-bank.com"
    try:
        result = subprocess.run([sys.executable, 'backend/scripts/infer_phishing.py', test_url], 
                              capture_output=True, text=True, 
                              timeout=30, cwd=project_root)
        if result.returncode == 0:
            response = json.loads(result.stdout)
            print(f"✓ URL inference working - Test URL classified as: {response.get('prediction', 'Unknown')}")
        else:
            print(f"✗ URL inference failed: {result.stderr}")
    except Exception as e:
        print(f"✗ URL inference test failed: {e}")
    
    print("\nStartup initialization complete!")

if __name__ == '__main__':
    main()