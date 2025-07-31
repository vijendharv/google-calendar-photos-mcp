# Google Calendar Photos MCP Server

A comprehensive Model Context Protocol (MCP) server that provides seamless access to Google Calendar and Google Photos APIs through standardized tool interfaces. This server enables AI assistants like Claude to interact with your Google services in a structured, secure way.

## 🌟 Features

### 📅 Calendar Management
- **create_calendar_event**: Create new calendar events with full details (title, time, location, description)
- **get_calendar_events**: Retrieve upcoming events with customizable result limits
- **update_calendar_event**: Modify existing events (partial updates supported)
- **delete_calendar_event**: Remove events permanently from your calendar

### 📸 Photos Integration
- **get_photos**: Retrieve recent photos from your Google Photos library
- **search_photos**: Advanced photo search with date range and media type filters
- **get_photo_download_url**: Generate temporary download URLs for full-resolution photos

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google Cloud Console account
- Google Calendar API and Google Photos Library API enabled

### 1. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd google-calendar-photos-mcp

# Install dependencies
pip install -r requirements.txt
```

### 2. Google API Setup

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Note your project ID for reference

2. **Enable Required APIs**
   ```bash
   # Enable Google Calendar API
   gcloud services enable calendar-json.googleapis.com
   
   # Enable Google Photos Library API
   gcloud services enable photoslibrary.googleapis.com
   ```
   Or enable them manually in the Console:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Calendar API" and enable it
   - Search for "Photos Library API" and enable it

3. **Create OAuth2 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Choose "Desktop application" as application type
   - Download the JSON file and rename it to `credentials.json`
   - Place `credentials.json` in the project root directory

### 3. Authentication Setup

On first run, the server will automatically:
1. Open your default browser
2. Redirect to Google's OAuth consent screen
3. Request permissions for Calendar and Photos access
4. Save tokens locally for future use (in `token.pickle`)

**Required OAuth Scopes:**
- `https://www.googleapis.com/auth/calendar` - Full calendar access
- `https://www.googleapis.com/auth/photoslibrary` - Photos library access
- `https://www.googleapis.com/auth/photoslibrary.readonly` - Read-only photos access

## 🛠️ Usage

### Running the Server

```bash
# Start the MCP server
python3 main.py

# For help and available options
python3 main.py --help
```

The server communicates via stdin/stdout using the MCP protocol and is designed to be used with MCP clients.

### MCP Client Configuration

#### Claude Desktop Integration

Add this configuration to your Claude Desktop MCP settings file:

**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "google-calendar-photos": {
      "command": "python",
      "args": ["/absolute/path/to/your/main.py"],
      "cwd": "/absolute/path/to/your/google-calendar-photos-mcp",
      "env": {
        "PYTHONPATH": "/absolute/path/to/your/google-calendar-photos-mcp"
      }
    }
  }
}
```

#### Generic MCP Client Configuration

```json
{
  "name": "google-calendar-photos",
  "transport": {
    "type": "stdio",
    "command": "python",
    "args": ["/path/to/main.py"],
    "cwd": "/path/to/google-calendar-photos-mcp"
  }
}
```

### Testing the Server

```bash
# Run basic connectivity test
python3 test_mcp_server.py

# Run startup diagnostics
python3 startup_test.py

# Test path resolution
python3 test_path_resolution.py
```

## 📋 Tool Reference

### Calendar Tools

#### create_calendar_event
Create a new calendar event with detailed information.

**Parameters:**
- `summary` (required): Event title
- `start_time` (required): Start time in ISO 8601 format (e.g., "2024-01-15T14:00:00Z")
- `end_time` (required): End time in ISO 8601 format
- `description` (optional): Event description
- `location` (optional): Event location/address
- `calendar_id` (optional): Target calendar ID (default: "primary")

**Example:**
```json
{
  "summary": "Team Meeting",
  "start_time": "2024-01-15T14:00:00Z",
  "end_time": "2024-01-15T15:00:00Z",
  "description": "Weekly team sync meeting",
  "location": "Conference Room A"
}
```

#### get_calendar_events
Retrieve upcoming events from your calendar.

**Parameters:**
- `calendar_id` (optional): Calendar to query (default: "primary")
- `max_results` (optional): Maximum events to return (1-2500, default: 10)

#### update_calendar_event
Update an existing calendar event. Only specified fields are modified.

**Parameters:**
- `event_id` (required): Unique event identifier
- `summary` (optional): New event title
- `start_time` (optional): New start time
- `end_time` (optional): New end time
- `description` (optional): New description
- `location` (optional): New location
- `calendar_id` (optional): Calendar containing the event

#### delete_calendar_event
Permanently delete a calendar event.

**Parameters:**
- `event_id` (required): Unique event identifier
- `calendar_id` (optional): Calendar containing the event

### Photos Tools

#### get_photos
Retrieve recent photos from Google Photos library.

**Parameters:**
- `page_size` (optional): Number of photos to retrieve (1-100, default: 25)

#### search_photos
Search photos with advanced filtering options.

**Parameters:**
- `start_date` (optional): Start date in ISO 8601 format
- `end_date` (optional): End date in ISO 8601 format
- `media_type` (optional): Filter by "PHOTO" or "VIDEO"
- `page_size` (optional): Number of results (1-100, default: 25)

#### get_photo_download_url
Generate a temporary download URL for a specific photo.

**Parameters:**
- `photo_id` (required): Unique photo identifier

**Note:** Download URLs expire after approximately 1 hour for security.

## 🏗️ Architecture

### Project Structure

```
google-calendar-photos-mcp/
├── main.py                    # MCP server entry point and core logic
├── google_api_client.py       # Google APIs client wrapper
├── mcp_tools.py              # MCP tool definitions and schemas
├── tool_handlers.py          # Tool execution handlers
├── requirements.txt          # Python dependencies
├── credentials.json          # Google OAuth2 credentials (you create this)
├── token.pickle             # Stored OAuth2 tokens (auto-generated)
├── startup_test.py          # Server startup diagnostics
├── test_mcp_server.py       # MCP server functionality tests
├── test_path_resolution.py  # Path resolution testing
└── README.md               # This documentation
```

### Component Overview

#### GoogleCalendarPhotosMCPServer (`main.py`)
- Main MCP server class implementing the MCP protocol
- Handles client connections via stdin/stdout
- Manages tool discovery and execution
- Coordinates authentication and service initialization

#### GoogleAPIClient (`google_api_client.py`)
- Wrapper for Google Calendar and Photos APIs
- Handles OAuth2 authentication flow
- Manages token storage and refresh
- Provides high-level methods for API operations

#### Tool Definitions (`mcp_tools.py`)
- Defines all available MCP tools and their schemas
- Separated into calendar and photos tool groups
- Includes input validation and parameter documentation

#### Tool Handlers (`tool_handlers.py`)
- Implements the actual tool execution logic
- Handles parameter processing and validation
- Formats responses for MCP clients
- Provides comprehensive error handling

## 🔧 Configuration

### Logging Configuration

The server uses Python's standard logging module. You can adjust log levels in `main.py`:

```python
logging.basicConfig(
    level=logging.INFO,  # Change to DEBUG for verbose output
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## 🛡️ Security Considerations

### OAuth2 Token Storage
- Tokens are stored locally in `token.pickle`
- Ensure this file has appropriate permissions (600 recommended)
- Tokens are automatically refreshed when needed
- Never share token files or commit them to version control

### API Scopes
The server requests minimal necessary scopes:
- Calendar: Full access for CRUD operations
- Photos: Read access for viewing and downloading

### Network Security
- All API communications use HTTPS
- Download URLs are temporary (1 hour expiration)
- No sensitive data is logged by default

## 🐛 Troubleshooting

### Common Issues

#### "Credentials file not found"
**Problem:** `credentials.json` is missing or in wrong location.

**Solution:**
1. Download OAuth2 credentials from Google Cloud Console
2. Rename file to `credentials.json`
3. Place in project root directory
4. Verify file path with: `ls -la credentials.json`

#### "API not enabled"
**Problem:** Required APIs not enabled in Google Cloud Console.

**Solution:**
1. Go to Google Cloud Console
2. Navigate to "APIs & Services" > "Library"
3. Enable "Google Calendar API"
4. Enable "Photos Library API"

#### "Permission denied during OAuth flow"
**Problem:** Insufficient permissions granted during OAuth consent.

**Solution:**
1. Delete `token.pickle` file
2. Restart server to trigger new OAuth flow
3. Ensure you grant all requested permissions

#### "MCP client connection failed"
**Problem:** MCP client cannot connect to server.

**Solution:**
1. Verify Python path in client configuration
2. Check file permissions on `main.py`
3. Ensure all dependencies are installed
4. Test server standalone: `python3 main.py --help`

### Debug Mode

Enable detailed logging:

```bash
# Set environment variable
export MCP_LOG_LEVEL=DEBUG

# Or modify main.py directly
logging.basicConfig(level=logging.DEBUG)
```

### Testing Components

```bash
# Test Google API authentication
python3 -c "from google_api_client import GoogleAPIClient; import asyncio; asyncio.run(GoogleAPIClient().authenticate())"

# Test MCP tool definitions
python3 -c "from mcp_tools import get_all_tools; print(f'Found {len(get_all_tools())} tools')"

# Test tool handlers initialization
python3 -c "from tool_handlers import ToolHandlers; print('Tool handlers loaded successfully')"
```

## Rate Limits
- Google Calendar API: 1,000,000 requests per day
- Google Photos API: 10,000 requests per day

## 🤝 Contributing

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt
pip install black flake8 pytest

# Format code
black *.py

# Lint code
flake8 *.py
```

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Include docstrings for all public methods
- Add comprehensive logging for debugging

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Google Calendar API Documentation](https://developers.google.com/calendar/api)
- [Google Photos API Documentation](https://developers.google.com/photos)
- [Google API Python Client Documentation](https://googleapis.github.io/google-api-python-client/)

---

**Note:** This server is designed for personal use and development. For production deployments, consider additional security measures, monitoring, and error handling as appropriate for your use case.
