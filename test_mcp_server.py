#!/usr/bin/env python3
"""
Test script for Google Calendar Photos MCP Server
This script helps diagnose issues with the MCP server setup
"""

import asyncio
import logging
import sys
import os
import json
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mcp-test')

async def test_google_api_client():
    """Test Google API client initialization"""
    logger.info("🧪 Testing Google API Client...")
    
    try:
        from google_api_client import GoogleAPIClient
        
        client = GoogleAPIClient()
        logger.info("✅ GoogleAPIClient instance created")
        
        # Test authentication
        await client.authenticate()
        logger.info("✅ Authentication successful")
        
        # Test service building
        await client.build_services()
        logger.info("✅ Google API services built successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Google API Client test failed: {e}")
        return False

async def test_mcp_tools():
    """Test MCP tools definitions"""
    logger.info("🧪 Testing MCP Tools...")
    
    try:
        from mcp_tools import get_all_tools
        
        tools = get_all_tools()
        logger.info(f"✅ Found {len(tools)} MCP tools:")
        
        for tool in tools:
            logger.info(f"  - {tool.name}: {tool.description}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ MCP Tools test failed: {e}")
        return False

async def test_tool_handlers():
    """Test tool handlers"""
    logger.info("🧪 Testing Tool Handlers...")
    
    try:
        from google_api_client import GoogleAPIClient
        from tool_handlers import ToolHandlers
        
        # Create a client and handlers
        client = GoogleAPIClient()
        await client.authenticate()
        await client.build_services()
        
        handlers = ToolHandlers(client)
        logger.info("✅ ToolHandlers instance created")
        
        # Test a simple tool call (get calendar events)
        result = await handlers.handle_tool_call("get_calendar_events", {})
        logger.info(f"✅ Tool call test successful, got {len(result)} result(s)")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Tool Handlers test failed: {e}")
        return False

def test_mcp_imports():
    """Test MCP library imports"""
    logger.info("🧪 Testing MCP imports...")
    
    try:
        import mcp.server.stdio
        import mcp.types as types
        from mcp.server import NotificationOptions, Server
        from mcp.server.models import InitializationOptions
        
        logger.info("✅ MCP library imports successful")
        return True
        
    except Exception as e:
        logger.error(f"❌ MCP imports failed: {e}")
        return False

def check_file_permissions():
    """Check file permissions and existence"""
    logger.info("🧪 Checking file permissions...")
    
    files_to_check = [
        'credentials.json',
        'token.json', 
        'main.py',
        'mcp_tools.py',
        'tool_handlers.py',
        'google_api_client.py'
    ]
    
    all_good = True
    
    for filename in files_to_check:
        path = Path(filename)
        if path.exists():
            stat = path.stat()
            logger.info(f"✅ {filename}: exists, size={stat.st_size}, mode={oct(stat.st_mode)[-3:]}")
        else:
            logger.error(f"❌ {filename}: missing")
            all_good = False
    
    return all_good

def test_mcp_server_class():
    """Test MCP server class creation"""
    logger.info("🧪 Testing MCP Server class...")
    
    try:
        from main import GoogleCalendarPhotosMCPServer
        
        server = GoogleCalendarPhotosMCPServer()
        logger.info("✅ GoogleCalendarPhotosMCPServer instance created")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ MCP Server class test failed: {e}")
        return False

async def run_all_tests():
    """Run all diagnostic tests"""
    logger.info("🚀 Starting MCP Server Diagnostic Tests")
    logger.info("=" * 50)
    
    tests = [
        ("File Permissions", check_file_permissions),
        ("MCP Imports", test_mcp_imports),
        ("MCP Server Class", test_mcp_server_class),
        ("MCP Tools", test_mcp_tools),
        ("Google API Client", test_google_api_client),
        ("Tool Handlers", test_tool_handlers),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running: {test_name}")
        logger.info("-" * 30)
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    logger.info("\n" + "=" * 50)
    logger.info("📊 Test Results Summary")
    logger.info("=" * 50)
    
    passed = 0
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {test_name}")
        if result:
            passed += 1
    
    logger.info(f"\n🎯 Tests passed: {passed}/{len(results)}")
    
    if passed == len(results):
        logger.info("🎉 All tests passed! Your MCP server should work.")
        logger.info("\n💡 If Claude Desktop still isn't working, check:")
        logger.info("  1. Claude Desktop MCP configuration")
        logger.info("  2. Python path in MCP config")
        logger.info("  3. Claude Desktop logs/restart")
    else:
        logger.info("⚠️  Some tests failed. Fix these issues first.")
    
    return passed == len(results)

if __name__ == "__main__":
    try:
        success = asyncio.run(run_all_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("👋 Tests interrupted")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ Test suite failed: {e}")
        sys.exit(1)
