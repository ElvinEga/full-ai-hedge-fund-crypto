#!/usr/bin/env python3
"""
Simple script to test if the API is working correctly.
Run this after starting the API server with: uvicorn api:app --reload
"""

import requests
from datetime import datetime, timedelta

API_BASE_URL = "http://localhost:8000"

def test_root():
    """Test the root endpoint"""
    print("Testing root endpoint...")
    response = requests.get(f"{API_BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_backtest():
    """Test the backtest endpoint"""
    print("Testing backtest endpoint...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=15)
    
    payload = {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "initial_cash": 10000,
        "tickers": ["BTCUSDT"],
        "intervals": ["1h"],
        "strategies": ["MacdStrategy"]
    }
    
    print(f"Payload: {payload}")
    print("Running backtest (this may take a minute)...")
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/backtest", json=payload, timeout=300)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Performance Metrics: {data.get('performance_metrics')}")
            print(f"Portfolio History Points: {len(data.get('portfolio_history', []))}")
        else:
            print(f"Error: {response.text}")
    except requests.exceptions.Timeout:
        print("Request timed out - backtest may take longer than expected")
    except Exception as e:
        print(f"Error: {e}")
    print()

def test_live_signals():
    """Test the live signals endpoint"""
    print("Testing live signals endpoint...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/live-signals", timeout=120)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            signals = response.json()
            print(f"Signals received for {len(signals)} tickers:")
            for ticker, decision in signals.items():
                print(f"  {ticker}: {decision.get('action')} (confidence: {decision.get('confidence')}%)")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("AI Hedge Fund Crypto API Test")
    print("=" * 60)
    print()
    
    try:
        test_root()
        
        print("Choose a test to run:")
        print("1. Test backtest endpoint (may take 1-2 minutes)")
        print("2. Test live signals endpoint")
        print("3. Run all tests")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            test_backtest()
        elif choice == "2":
            test_live_signals()
        elif choice == "3":
            test_backtest()
            test_live_signals()
        elif choice == "4":
            print("Exiting...")
        else:
            print("Invalid choice")
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to API server.")
        print("Make sure the API is running with: uvicorn api:app --reload")
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
