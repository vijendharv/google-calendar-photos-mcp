# Claude Desktop MCP Configuration Guide

## Issue: MCP Server Not Working with Claude Desktop

When your MCP server is "not working as expected" (no actions taken), it usually means Claude Desktop isn't successfully connecting to your MCP server. Here are the common issues and solutions:

## 1. Check Claude Desktop MCP Configuration

Claude Desktop looks for MCP configuration in:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Your configuration should look like this:

```json
{
  "mcpServers": {
    "google-calendar-photos": {
      "command": "python3",
      "args": ["/PathTo/google-calendar-photos-mcp/main.py"],
      "cwd": "/PathTo/google-calendar-photos-mcp"
    }
  }
}
```

## 2. Common Configuration Issues

### Wrong Python Path
- Use `python3` instead of `python` if you have multiple Python versions
- Or use full path: `/usr/bin/python3` or `/opt/homebrew/bin/python3`

### Wrong File Paths
- Use absolute paths, not relative paths
- Ensure the `main.py` path is correct
- Ensure the `cwd` (current working directory) is correct

### Wrong Python Environment
If you're using a virtual environment, activate it or use the full path:
```json
{
  "mcpServers": {
    "google-calendar-photos": {
      "command": "/PathTo/google-calendar-photos-mcp/google-calendar-photos-mcp/bin/python3",
      "args": ["/PathTo/google-calendar-photos-mcp/main.py"],
      "cwd": "/PathTo/google-calendar-photos-mcp"
    }
  }
}
```

## 3. Debugging Steps

### Step 1: Test Your MCP Server Independently
Run this in your terminal:
```bash
cd /PathTo/google-calendar-photos-mcp
python3 test_mcp_server.py
```

This will run diagnostic tests and tell you if there are any issues with your server code.

### Step 2: Test MCP Server Startup
```bash
cd /PathTo/google-calendar-photos-mcp
python3 main.py
```

The server should start and show log messages. If it crashes or shows errors, fix those first.

### Step 3: Check Claude Desktop Logs
Claude Desktop logs can help identify connection issues:
- **macOS**: `~/Library/Logs/Claude/`
- Look for error messages about MCP servers

### Step 4: Restart Claude Desktop
After changing MCP configuration:
1. Quit Claude Desktop completely
2. Wait a few seconds
3. Restart Claude Desktop
4. Try using calendar or photos commands

## 4. Testing Commands

Once everything is working, try these commands in Claude Desktop:

```
Can you show me my upcoming calendar events?
```

```
Can you create a calendar event for tomorrow at 2 PM called "Team Meeting"?
```

```
Can you show me recent photos from my Google Photos?
```

## 5. Permission Issues

Make sure your OAuth2 setup is correct:
1. `credentials.json` should contain your Google Cloud Console OAuth2 credentials
2. `token.json` should be created after first authentication
3. You should have granted Calendar and Photos permissions during OAuth flow

## 6. Virtual Environment Issues

If you created a virtual environment (which I see you have), make sure to:
1. Use the Python binary from inside the virtual environment in your MCP config
2. OR activate the environment before running
3. OR install all dependencies globally

## 7. Firewall/Security Issues

Some security software can block MCP communication:
- Check if any antivirus is blocking Python or Claude Desktop
- Check if firewall is blocking local process communication

## Quick Fix Checklist

- [ ] MCP config file exists and has correct JSON syntax
- [ ] Python path in config is correct (`which python3` to check)
- [ ] File paths in config are absolute and correct
- [ ] Dependencies are installed (`pip install -r requirements.txt`)
- [ ] Credentials files exist (`credentials.json`, `token.json`)
- [ ] MCP server starts without errors when run manually
- [ ] Claude Desktop has been restarted after config changes
- [ ] No firewall/antivirus blocking the connection

Run the test script first to identify specific issues!
