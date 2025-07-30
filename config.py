"""
Configuration settings for Google APIs MCP Server
"""

import os
from typing import List

# Server Configuration
SERVER_NAME = "google-apis-mcp-server"
SERVER_VERSION = "1.0.0"
LOG_LEVEL = "INFO"

# Google API Configuration
GOOGLE_SCOPES: List[str] = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/photoslibrary.readonly', 
    'https://www.googleapis.com/auth/drive.readonly',
]

# File paths - use absolute paths relative to this config file
_CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(_CONFIG_DIR, "credentials.json")
TOKEN_FILE = os.path.join(_CONFIG_DIR, "token.json")

# API Settings
GOOGLE_API_CACHE_DISCOVERY = False  # Prevents oauth2client warnings
DEFAULT_PAGE_SIZE = 10
MAX_RETRY_ATTEMPTS = 3

# MCP Server Settings
MCP_SERVER_HOST = "localhost"
MCP_SERVER_PORT = 8080
HEALTH_CHECK_INTERVAL = 30  # seconds

# Environment-specific overrides
if os.getenv('DEVELOPMENT'):
    LOG_LEVEL = "DEBUG"
    HEALTH_CHECK_INTERVAL = 10

# Validation
def validate_config():
    """Validate configuration settings"""
    errors = []
    
    if not os.path.exists(CREDENTIALS_FILE):
        errors.append(f"Credentials file not found: {CREDENTIALS_FILE}")
    
    if not GOOGLE_SCOPES:
        errors.append("No Google API scopes defined")
    
    return errors