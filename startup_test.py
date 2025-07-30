#!/usr/bin/env python3
"""
Simple MCP Server Startup Test
This script tests if the MCP server can start properly and identifies startup issues.
"""

import sys
import os
import asyncio
import logging

# Set up logging to see all messages
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('startup_test.log')
    ]
)

logger = logging.getLogger('mcp-startup-test')

async def test_server_startup():
    """Test if the MCP server can start up properly"""
    logger.info("🚀 Testing MCP Server Startup...")
    
    try:
        # Test imports first
        logger.info("📦 Testing imports...")
        
        import mcp.server.stdio
        import mcp.types as types
        from mcp.server import NotificationOptions, Server
        from mcp.server.models import InitializationOptions
        logger.info("✅ MCP library imports successful")
        
        # Import our server
        from main import GoogleCalendarPhotosMCPServer
        logger.info("✅ Server class import successful")
        
        # Try to create server instance
        logger.info("🏗️  Creating server instance...")
        server = GoogleCalendarPhotosMCPServer()
        logger.info("✅ Server instance created successfully")
        
        # Test tool listing
        logger.info("📋 Testing tool listing...")
        from mcp_tools import get_all_tools
        tools = get_all_tools()
        logger.info(f"✅ Found {len(tools)} tools")
        
        for tool in tools:
            logger.info(f"   - {tool.name}")
        
        logger.info("🎉 Server startup test completed successfully!")
        logger.info("\n" + "="*50)
        logger.info("CONCLUSION: Your MCP server code is working fine.")
        logger.info("The issue is likely with Claude Desktop configuration.")
        logger.info("Check the DEBUG_GUIDE.md file for configuration help.")
        logger.info("="*50)
        
        return True
        
    except ImportError as e:
        logger.error(f"❌ Import error: {e}")
        logger.error("💡 This suggests missing dependencies. Try:")
        logger.error("   pip install -r requirements.txt")
        return False
        
    except Exception as e:
        logger.error(f"❌ Startup test failed: {e}")
        logger.error("💡 Check the error above and fix the issue.")
        return False

def check_environment():
    """Check Python environment and paths"""
    logger.info("🐍 Python Environment Check")
    logger.info("-" * 30)
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Python executable: {sys.executable}")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"Python path: {sys.path[:3]}...")  # Show first 3 entries
    
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        logger.info("✅ Running in virtual environment")
        venv_path = sys.prefix
        logger.info(f"Virtual environment path: {venv_path}")
    else:
        logger.warning("⚠️  Not running in virtual environment")
        logger.warning("This might be okay, but ensure all dependencies are installed")

if __name__ == "__main__":
    logger.info("🧪 MCP Server Startup Test")
    logger.info("=" * 50)
    
    check_environment()
    
    try:
        success = asyncio.run(test_server_startup())
        
        if success:
            logger.info("\n🎯 NEXT STEPS:")
            logger.info("1. Check your Claude Desktop MCP configuration")
            logger.info("2. Make sure you're using the correct Python path")
            logger.info("3. Restart Claude Desktop after config changes")
            logger.info("4. Read DEBUG_GUIDE.md for detailed instructions")
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.info("👋 Test interrupted")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        sys.exit(1)
