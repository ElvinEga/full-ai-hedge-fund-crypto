#!/usr/bin/env python3
"""
Test script to verify the API remains responsive during a backtest.
Run this while a backtest is in progress to confirm non-blocking behavior.
"""

import requests
import time

API_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test that health endpoint responds quickly."""
    start = time.time()
    try:
        response = requests.get(f"{API_URL}/api/health", timeout=2)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            print(f"✅ Health check passed in {elapsed:.3f}s")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print(f"❌ Health check timed out (>2s)")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_settings_endpoint():
    """Test that settings endpoint responds quickly."""
    start = time.time()
    try:
        response = requests.get(f"{API_URL}/api/settings", timeout=2)
        elapsed = time.time() - start
        
        if response.status_code == 200:
            print(f"✅ Settings endpoint passed in {elapsed:.3f}s")
            return True
        else:
            print(f"❌ Settings endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.Timeout:
        print(f"❌ Settings endpoint timed out (>2s)")
        return False
    except Exception as e:
        print(f"❌ Settings endpoint error: {e}")
        return False

def main():
    print("Testing API responsiveness...")
    print("=" * 50)
    print("Run this script WHILE a backtest is running to verify")
    print("that the API remains responsive and non-blocking.")
    print("=" * 50)
    print()
    
    # Run tests multiple times
    for i in range(5):
        print(f"\nTest iteration {i+1}/5:")
        test_health_endpoint()
        test_settings_endpoint()
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("Test complete!")
    print("If all tests passed quickly (<2s each), the API is non-blocking.")

if __name__ == "__main__":
    main()
