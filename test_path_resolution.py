#!/usr/bin/env python3
"""
Test script to verify path resolution for credentials file
"""

import os
import logging
import sys

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('test_path_resoltion.log')
    ]
)

logger = logging.getLogger('path-resolution-test')

def test_path_resolution():
    logger.info("Testing path resolution...")
    logger.info(f"Current working directory: {os.getcwd()}")
    
    # Get the directory where this script is located (same logic as main.py)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_path = os.path.join(script_dir, 'credentials.json')
    
    logger.info(f"Script directory: {script_dir}")
    logger.info(f"Script file: {__file__}")
    logger.info(f"Script absolute path: {os.path.abspath(__file__)}")
    logger.info(f"Credentials path: {credentials_path}")
    logger.info(f"Credentials exists: {os.path.exists(credentials_path)}")
    
    logger.info(f"\nFiles in script directory:")
    try:
        for file in os.listdir(script_dir):
            if file.endswith('.json') or file.endswith('.py'):
                logger.info(f"   - {file}")
    except Exception as e:
        logger.error(f"   Error listing directory: {e}")

if __name__ == "__main__":
    test_path_resolution()
