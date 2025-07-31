# Dependencies Documentation

This document provides detailed information about all dependencies used in the Google Calendar Photos MCP Server, their purposes, versions, and relationships.

## 📦 Core Dependencies

### Model Context Protocol (MCP)

#### `mcp>=1.0.0`
- **Purpose**: Core MCP (Model Context Protocol) framework for building MCP servers
- **Category**: Framework/Protocol
- **Usage**: Essential for implementing the MCP server interface, handling client communications, and defining tools
- **Key Components Used**:
  - `mcp.server.stdio`: Handles stdin/stdout communication with MCP clients
  - `mcp.types`: Type definitions for MCP protocol (Tool, TextContent, etc.)
  - `mcp.server`: Base server functionality and initialization options
- **Why Critical**: This is the foundation of the entire MCP server - without it, the server cannot communicate with MCP clients like Claude Desktop

## 🔐 Google API Authentication

### `google-auth>=2.15.0`
- **Purpose**: Core Google authentication library providing OAuth2 and service account authentication
- **Category**: Authentication
- **Usage**: Base authentication functionality for all Google APIs
- **Key Components Used**:
  - OAuth2 credential management
  - Token refresh mechanisms
  - Request signing for API calls
- **Dependencies**: Used by all other Google API libraries
- **Why Critical**: Required for any interaction with Google services

### `google-auth-oauthlib>=0.8.0`
- **Purpose**: OAuth2 flow implementation for Google APIs using the `oauthlib` library
- **Category**: Authentication/OAuth2
- **Usage**: Handles the OAuth2 consent flow for user authentication
- **Key Components Used**:
  - `InstalledAppFlow`: Manages desktop application OAuth2 flow
  - Browser-based user consent handling
  - Authorization code exchange for tokens
- **Relationship**: Extends `google-auth` with OAuth2-specific functionality
- **Why Critical**: Enables the initial authentication flow where users grant permissions

### `google-auth-httplib2>=0.1.0`
- **Purpose**: HTTP transport adapter for Google authentication using httplib2
- **Category**: HTTP Transport
- **Usage**: Provides HTTP transport layer for authenticated Google API requests
- **Key Components Used**:
  - HTTP request signing with authentication headers
  - Transport layer for `google-api-python-client`
- **Relationship**: Bridge between `google-auth` and HTTP requests
- **Why Critical**: Required for making authenticated API calls

## 🌐 Google API Client Libraries

### `google-api-python-client>=2.70.0`
- **Purpose**: Official Google API Python client library for multiple Google services
- **Category**: API Client
- **Usage**: Primary interface for Google Calendar and Photos API operations
- **Key Components Used**:
  - `googleapiclient.discovery.build()`: Creates service objects for APIs
  - Service object methods for CRUD operations
  - Error handling (`googleapiclient.errors.HttpError`)
- **APIs Supported**:
  - Google Calendar API v3
  - Google Photos Library API v1
- **Why Critical**: Main interface for all Google API interactions

### `google-api-core>=2.11.0`
- **Purpose**: Core functionality shared across Google Cloud client libraries
- **Category**: Core Library
- **Usage**: Provides common functionality used by Google API clients
- **Key Components Used**:
  - Request retry logic
  - Error handling and exception definitions
  - Common utilities for API interactions
- **Relationship**: Dependency of `google-api-python-client`
- **Why Critical**: Provides essential infrastructure for reliable API operations

## ⚡ Asynchronous I/O

### `aiofiles>=22.1.0`
- **Purpose**: Asynchronous file I/O operations for Python asyncio
- **Category**: Async I/O
- **Usage**: Enables non-blocking file operations in async contexts
- **Key Components Used**:
  - Async file reading/writing
  - Non-blocking file system operations
- **Why Used**: Ensures the MCP server remains responsive during file operations
- **Benefits**: Prevents blocking the event loop during file I/O operations

## 🛠️ Development and Configuration

### `python-dotenv>=0.19.0`
- **Purpose**: Load environment variables from `.env` files
- **Category**: Configuration Management
- **Usage**: Allows configuration through environment variables
- **Key Components Used**:
  - `load_dotenv()`: Loads variables from .env files
  - Environment variable management
- **Why Useful**: Enables easy configuration without modifying code
- **Use Cases**:
  - Custom credential paths
  - Debug settings
  - API configuration options

### `typing-extensions>=4.0.0`
- **Purpose**: Backport of newer typing features to older Python versions
- **Category**: Type Annotations
- **Usage**: Provides advanced type hinting capabilities
- **Key Components Used**:
  - Enhanced type annotations
  - Compatibility with older Python versions
  - Advanced generic types
- **Why Included**: Ensures type safety and better IDE support across Python versions

## 📊 Logging and Monitoring (Optional)

### `structlog>=22.1.0`
- **Purpose**: Structured logging library for Python
- **Category**: Logging/Monitoring
- **Usage**: Enhanced logging with structured data
- **Key Components Used**:
  - Structured log messages
  - Context preservation
  - Enhanced debugging capabilities
- **Status**: Optional enhancement
- **Benefits**: Better log analysis and debugging capabilities

### `rich>=12.0.0`
- **Purpose**: Rich text and beautiful formatting for terminal output
- **Category**: User Interface/Debugging
- **Usage**: Enhanced console output and error formatting
- **Key Components Used**:
  - Colored console output
  - Rich error tracebacks
  - Progress indicators
- **Status**: Optional enhancement
- **Benefits**: Improved developer experience and debugging

## 🔄 Dependency Relationships

### Critical Path Dependencies
```
MCP Server Core:
mcp >= 1.0.0
└── Server foundation

Google APIs Authentication Chain:
google-auth >= 2.15.0 (base)
├── google-auth-oauthlib >= 0.8.0 (OAuth2 flow)
├── google-auth-httplib2 >= 0.1.0 (HTTP transport)
└── google-api-python-client >= 2.70.0 (API client)
    └── google-api-core >= 2.11.0 (shared core)

Async Support:
aiofiles >= 22.1.0 (async file I/O)
```

### Optional Enhancement Dependencies
```
Development Tools:
├── python-dotenv >= 0.19.0 (configuration)
├── typing-extensions >= 4.0.0 (type hints)
├── structlog >= 22.1.0 (structured logging)
└── rich >= 12.0.0 (rich console output)
```

## 🎯 Version Constraints Explained

### Why Minimum Versions Matter

#### `mcp>=1.0.0`
- **Reason**: MCP protocol stability - earlier versions had breaking changes
- **Risk**: Compatibility issues with MCP clients

#### `google-auth>=2.15.0`
- **Reason**: Security improvements and OAuth2 flow stability
- **Risk**: Authentication failures with older versions

#### `google-auth-oauthlib>=0.8.0`
- **Reason**: Support for modern OAuth2 flows and security enhancements
- **Risk**: OAuth2 consent flow may not work properly

#### `google-api-python-client>=2.70.0`
- **Reason**: Support for latest Google API features and bug fixes
- **Risk**: Missing API methods or outdated service definitions

#### `google-api-core>=2.11.0`
- **Reason**: Improved error handling and retry logic
- **Risk**: Unreliable API operations under poor network conditions

#### `aiofiles>=22.1.0`
- **Reason**: Python 3.8+ compatibility and async improvements
- **Risk**: Async file operations may not work correctly

## 🚀 Installation Strategies

### Minimal Installation
For basic functionality:
```bash
pip install mcp google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client google-api-core aiofiles
```

### Development Installation
For development with enhanced features:
```bash
pip install -r requirements.txt
```

### Production Installation
For production deployments:
```bash
pip install --no-deps -r requirements.txt
pip check  # Verify no dependency conflicts
```

## 🔍 Dependency Analysis

### Security Considerations

#### Direct Dependencies
- All Google libraries are official and maintained by Google
- MCP library is maintained by Anthropic
- Regular security updates available

#### Transitive Dependencies
- Each dependency brings additional packages
- Monitor security advisories for the full dependency tree
- Use `pip-audit` to check for known vulnerabilities

### Performance Impact

#### Runtime Dependencies
- **Low Impact**: `mcp`, `typing-extensions`
- **Medium Impact**: `google-auth*` libraries, `aiofiles`
- **High Impact**: `google-api-python-client` (large service definitions)

#### Memory Usage
- Base dependencies: ~20MB
- Google API client libraries: ~30MB additional
- Optional libraries: ~10MB additional

### Update Strategy

#### Critical Updates (Immediate)
- Security patches in authentication libraries
- MCP protocol updates
- Major bug fixes in Google API clients

#### Regular Updates (Monthly)
- Minor version updates
- Performance improvements
- Feature additions

#### Breaking Changes (Planned)
- Major version updates requiring code changes
- Deprecated API version migrations
- Python version compatibility updates

## ⚠️ Common Issues

### Dependency Conflicts

#### `google-auth` Version Conflicts
**Problem**: Multiple Google libraries requiring different `google-auth` versions
**Solution**: Use `pip install --upgrade` to resolve to latest compatible versions

#### `typing-extensions` Compatibility
**Problem**: Older Python versions may have issues with newer typing features
**Solution**: Pin to specific version if compatibility issues arise

### Missing Dependencies

#### OAuth2 Flow Issues
**Symptoms**: Browser doesn't open, authentication fails
**Check**: Ensure `google-auth-oauthlib` is installed and up to date

#### API Call Failures
**Symptoms**: "Module not found" errors for Google APIs
**Check**: Verify `google-api-python-client` installation

### Performance Issues

#### Slow Import Times
**Cause**: Large Google API client library
**Mitigation**: Use lazy imports in production if needed

#### Memory Usage
**Cause**: Multiple Google API service objects
**Mitigation**: Create services only when needed

## 🔄 Upgrade Path

### From Earlier Versions

#### Upgrading MCP
```bash
pip install --upgrade mcp
# Check for breaking changes in MCP protocol
```

#### Upgrading Google APIs
```bash
pip install --upgrade google-api-python-client google-api-core
# Test authentication flow after upgrade
```

### Testing After Upgrades
```bash
# Test basic functionality
python test_mcp_server.py

# Test authentication
python -c "from google_api_client import GoogleAPIClient; import asyncio; asyncio.run(GoogleAPIClient().authenticate())"

# Test MCP protocol
python main.py --help
```

## 📚 Additional Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Google Auth Library Documentation](https://google-auth.readthedocs.io/)
- [Google API Python Client Documentation](https://googleapis.github.io/google-api-python-client/)
- [Python Async I/O Documentation](https://docs.python.org/3/library/asyncio.html)

---

**Note**: This dependency documentation is maintained alongside the main project. When adding new dependencies, update this document with their purpose, usage, and relationships.
