# Google Calendar Photos MCP Server

This is a Model Context Protocol (MCP) server that provides access to Google Calendar and Google Photos APIs through standardized tool interfaces that can be used by AI assistants like Claude.

## Features

### Calendar Tools
- **create_calendar_event**: Create new calendar events
- **get_calendar_events**: Retrieve upcoming events
- **update_calendar_event**: Modify existing events
- **delete_calendar_event**: Remove events

### Photos Tools
- **get_photos**: Retrieve recent photos from Google Photos
- **search_photos**: Search photos with date and type filters
- **get_photo_download_url**: Get download URLs for specific photos

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Google API Setup
1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API and Google Photos Library API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the credentials as `credentials.json` and place in this directory

### 3. Authentication
On first run, the server will open a browser for OAuth2 authentication. Grant the necessary permissions for Calendar and Photos access.

## Usage

### Running the Server
```bash
python main.py
```

### MCP Client Configuration
To use with Claude Desktop, add this to your MCP settings:

```json
{
  "mcpServers": {
    "google-calendar-photos": {
      "command": "python",
      "args": ["/path/to/your/main.py"],
      "cwd": "/path/to/your/google-calendar-photos-mcp"
    }
  }
}
```

### Testing the Server
```bash
# Get help
python main.py --help

# Run the server (for debugging)
python main.py
```

## File Structure
- `main.py`: Main MCP server implementation
- `mcp_tools.py`: Tool definitions and schemas
- `tool_handlers.py`: Tool execution handlers
- `google_api_client.py`: Google API client wrapper
- `config.py`: Configuration settings
- `credentials.json`: Google API credentials (you must create this)
- `token.json`: OAuth2 tokens (auto-generated)

## Troubleshooting

### Common Issues
1. **Missing credentials**: Ensure `credentials.json` exists
2. **API not enabled**: Enable Calendar and Photos APIs in Google Cloud Console
3. **Permissions**: Grant appropriate scopes during OAuth flow
4. **MCP client connection**: Check MCP client configuration

### Debugging
Enable debug logging by setting the log level to DEBUG in `main.py`.

## License
MIT License
