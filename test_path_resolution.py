#!/usr/bin/env python3
"""
Test script to verify path resolution for credentials file
"""

import os
import sys

def test_path_resolution():
    print("Testing path resolution...")
    print(f"Current working directory: {os.getcwd()}")
    
    # Get the directory where this script is located (same logic as main.py)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(script_dir, 'credentials.json')
    
    print(f"Script directory: {script_dir}")
    print(f"Script file: {__file__}")
    print(f"Script absolute path: {os.path.abspath(__file__)}")
    print(f"Credentials path: {credentials_path}")
    print(f"Credentials exists: {os.path.exists(credentials_path)}")
    
    print(f"\nFiles in script directory:")
    try:
        for file in os.listdir(script_dir):
            if file.endswith('.json') or file.endswith('.py'):
                print(f"   - {file}")
    except Exception as e:
        print(f"   Error listing directory: {e}")

if __name__ == "__main__":
    test_path_resolution()
