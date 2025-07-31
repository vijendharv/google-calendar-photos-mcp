#!/usr/bin/env python3
"""
Google Calendar Photos MCP Server
Proper MCP implementation with Google APIs integration
"""

import asyncio
import logging
import sys
import os

# MCP imports
import mcp.server.stdio
import mcp.types as types
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions

# Local imports
from mcp_tools import get_all_tools
from tool_handlers import ToolHandlers
from google_api_client import GoogleAPIClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('google-calendar-photos-mcp')

class GoogleCalendarPhotosMCPServer:
    """
    MCP Server for Google Calendar and Photos integration
    
    This server implements the Model Context Protocol (MCP) to provide
    access to Google Calendar and Google Photos APIs through standardized
    tool interfaces that can be used by AI assistants like Claude.
    """
    
    def __init__(self):
        """Initialize the MCP server"""
        self.server = Server("google-calendar-photos-mcp")
        self.google_client = None
        self.tool_handlers = None
        
        # Set up MCP server handlers
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Set up MCP protocol handlers"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> list[types.Tool]:
            """
            Handle the list_tools request from MCP clients
            
            Returns:
                list[types.Tool]: All available tools (calendar + photos)
            """
            logger.info("📋 Client requested list of available tools")
            return get_all_tools()
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str, 
            arguments: dict | None
        ) -> list[types.TextContent]:
            """
            Handle tool execution requests from MCP clients
            
            Args:
                name: Name of the tool to execute
                arguments: Arguments passed to the tool
                
            Returns:
                list[types.TextContent]: Tool execution results
            """
            logger.info(f"🔧 Client requested tool execution: {name}")
            
            # Initialize Google client if not already done
            if not self.google_client:
                await self._initialize_google_client()
            
            # Ensure we have tool handlers
            if not self.tool_handlers:
                self.tool_handlers = ToolHandlers(self.google_client)
            
            # Execute the tool
            try:
                return await self.tool_handlers.handle_tool_call(
                    name, 
                    arguments or {}
                )
            except Exception as e:
                logger.error(f"❌ Tool execution failed: {e}")
                return [types.TextContent(
                    type="text",
                    text=f"❌ Tool execution failed: {str(e)}"
                )]
    
    async def _initialize_google_client(self):
        """Initialize Google API client with proper error handling"""
        try:
            logger.info("🔧 Initializing Google API client...")
            
            # Get the directory where this script is located
            # Use multiple approaches to ensure we get the correct path
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Alternative: try to resolve the actual script location
            try:
                import sys
                if hasattr(sys, '_getframe'):
                    frame = sys._getframe(0)
                    alt_script_dir = os.path.dirname(os.path.abspath(frame.f_code.co_filename))
                    if alt_script_dir != script_dir:
                        logger.info(f"📁 Alternative script directory: {alt_script_dir}")
            except:
                pass
            
            credentials_path = os.path.join(script_dir, 'credentials.json')
            token_path = os.path.join(script_dir, 'token.pickle')
            
            logger.info(f"📁 Script directory: {script_dir}")
            logger.info(f"📁 Using credentials file: {credentials_path}")
            logger.info(f"📁 Using token file: {token_path}")
            logger.info(f"📁 Current working directory: {os.getcwd()}")
            
            # Verify credentials file exists before proceeding
            if not os.path.exists(credentials_path):
                logger.error(f"❌ Credentials file not found at: {credentials_path}")
                logger.info(f"📁 Files in script directory:")
                try:
                    for file in os.listdir(script_dir):
                        logger.info(f"   - {file}")
                except Exception as e:
                    logger.error(f"❌ Could not list script directory: {e}")
                raise FileNotFoundError(
                    f"Credentials file not found: {credentials_path}\n"
                    f"Please ensure credentials.json is in: {script_dir}"
                )
            
            logger.info(f"✅ Credentials file found: {credentials_path}")
            
            self.google_client = GoogleAPIClient(
                credentials_file=credentials_path,
                token_file=token_path
            )
            await self.google_client.authenticate()
            await self.google_client.build_services()
            
            logger.info("✅ Google API client initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Google API client: {e}")
            # Create a minimal client that will handle errors gracefully
            script_dir = os.path.dirname(os.path.abspath(__file__))
            credentials_path = os.path.join(script_dir, 'credentials.json')
            token_path = os.path.join(script_dir, 'token.pickle')
            self.google_client = GoogleAPIClient(
                credentials_file=credentials_path,
                token_file=token_path
            )
    
    async def run(self):
        """
        Run the MCP server
        
        This method starts the server and handles MCP protocol communication
        via stdin/stdout as per MCP specification.
        """
        try:
            logger.info("🚀 Starting Google Calendar Photos MCP Server...")
            logger.info("📡 Server will communicate via stdin/stdout (MCP protocol)")
            
            # Run the MCP server with stdio transport
            async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="google-calendar-photos-mcp",
                        server_version="1.0.0",
                        capabilities=self.server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={},
                        ),
                    ),
                )
        except KeyboardInterrupt:
            logger.info("👋 Received shutdown signal")
        except Exception as e:
            logger.error(f"❌ Server error: {e}")
            raise
        finally:
            logger.info("🛑 Google Calendar Photos MCP Server stopped")

async def main():
    """Main entry point for the MCP server"""
    try:
        server = GoogleCalendarPhotosMCPServer()
        await server.run()
    except KeyboardInterrupt:
        logger.info("👋 Application interrupted")
    except Exception as e:
        logger.error(f"❌ Application failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure we're running in the correct environment
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("""
Google Calendar Photos MCP Server

This is an MCP (Model Context Protocol) server that provides access to 
Google Calendar and Google Photos APIs through standardized tool interfaces.

Usage:
    python main.py

The server communicates via stdin/stdout using the MCP protocol.
It should be registered with an MCP client (like Claude Desktop) to be used.

Available Tools:
- Calendar: create_calendar_event, get_calendar_events, update_calendar_event, delete_calendar_event
- Photos: get_photos, search_photos, get_photo_download_url

Configuration:
- Ensure credentials.json is present (Google API credentials)
- The server will handle OAuth2 flow on first run
- Tokens are saved for subsequent runs

For more information, see the MCP documentation at https://modelcontextprotocol.io/
        """)
        sys.exit(0)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Application interrupted")
    except Exception as e:
        logger.error(f"❌ Application startup failed: {e}")
        sys.exit(1)
